import time

import ldap
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import redirect, render

from .utils import execute_report, find_best_report

# ----- Chatbot view -----
@login_required(login_url='login')
def chatbot_view(request):
    response = None
    search_time = None
    execution_time = None
    total_time = None
    from_cache = False

    if request.method == "POST":
        user_prompt = request.POST.get("prompt")

        start_search = time.time()
        report = find_best_report(user_prompt)
        end_search = time.time()
        search_time = round(end_search - start_search, 3)

        if report:
            report_id = report.get("id", "unknown")
            essential_params = {k: request.POST[k] for k in request.POST if k != "csrfmiddlewaretoken" and k != "prompt"}
            params_hash = hash(frozenset(essential_params.items()))
            cache_key = f"report_{report_id}_{params_hash}"

            start_cache = time.time()
            cached_result = cache.get(cache_key)
            end_cache = time.time()

            if cached_result:
                response = cached_result
                execution_time = round(end_cache - start_cache, 3)
                from_cache = True
            else:
                start_exec = time.time()
                response = execute_report(report, request.POST)
                end_exec = time.time()
                execution_time = round(end_exec - start_exec, 3)
                from_cache = False
                cache.set(cache_key, response, timeout=None)

        if search_time is not None and execution_time is not None:
            total_time = round(search_time + execution_time, 3)

    return render(request, "chatbot.html", {
        "response": response,
        "search_time": search_time,
        "execution_time": execution_time,
        "total_time": total_time,
        "from_cache": from_cache,
    })


# ----- Login via Active Directory -----
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Veuillez saisir le nom d'utilisateur et le mot de passe.")
            return render(request, 'login.html')

        try:
            ldap_server = settings.LDAP_SERVER
            base_dn = settings.LDAP_BASE_DN
            service_user = settings.LDAP_SERVICE_USER
            service_password = settings.LDAP_SERVICE_PASSWORD

            if not service_user or not service_password:
                messages.error(request, "Configuration LDAP incomplète (.env).")
                return render(request, "login.html")

            # Connexion avec le compte service
            conn = ldap.initialize(ldap_server)
            conn.set_option(ldap.OPT_REFERRALS, 0)
            conn.simple_bind_s(service_user, service_password)

            # Recherche de l'utilisateur
            search_filter = f"(sAMAccountName={username})"
            result = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)

            if not result:
                messages.error(request, "Utilisateur introuvable dans Active Directory.")
                return render(request, 'login.html')

            user_dn = result[0][0]  # DN complet

            # Bind final avec le mot de passe de l'utilisateur
            conn.simple_bind_s(user_dn, password)

            # Authentification Django
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()
                user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Bienvenue {username} !")
            return redirect('chatbot')

        except ldap.INVALID_CREDENTIALS:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        except Exception as e:
            messages.error(request, f"Erreur de connexion AD : {e}")

    return render(request, 'login.html')


# ----- Logout -----
def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect('login')


# ----- Signup -----
def signup_view(request):
    messages.error(request, "La création de compte est désactivée car Active Directory est utilisé.")
    return redirect('login')
