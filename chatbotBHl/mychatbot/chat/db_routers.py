# chat/db_routers.py
class AuthRouter:
    """
    Router pour stocker les modèles auth dans la base 'default'
    et tout le reste dans 'oracle'.
    """
    route_app_labels = {'auth', 'contenttypes', 'sessions', 'admin', 'messages'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return 'oracle'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return 'oracle'

    def allow_relation(self, obj1, obj2, **hints):
        # Autoriser les relations si les deux objets sont sur la même base
        db_set = {'default', 'oracle'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'default'
        return db == 'oracle'
