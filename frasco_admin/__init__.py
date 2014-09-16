from frasco import Feature, action, Blueprint, current_app, hook
from frasco.utils import import_string
from .view import AdminView, AdminBlueprint
from blueprint import admin_bp
import os


class AdminFeature(Feature):
    name = "admin"
    requires = ["users", "users_acl", "bootstrap"]
    blueprints = [admin_bp]
    view_files = [("admin/*", AdminView)]
    defaults = {"admin_role": "admin",
                "superadmin_role": "superadmin",
                "superadmins": [],
                "url_prefix": "/admin",
                "subdomain": None}

    def init_app(self, app):
        self.app = app
        app.features.menu.ensure("admin")
        
        app.assets.register({
            "admin": [
                "@jquery-bootstrap-all-cdn",
                "@font-awesome-cdn",
                "admin/layout.css",
                "admin/admin.js"]})

        app.jinja_env.macros.register_file(
            os.path.join(os.path.dirname(__file__), "macros.html"), "admin.html")

    def init_blueprints(self, app):
        self.register_blueprint(admin_bp)
        for feature in app.features:
            if hasattr(feature, "init_admin"):
                feature.init_admin(self)

    def make_superadmin(self, user):
        user.roles.append(self.options["superadmin_role"])
        self.app.features.models.save(user)

    def register_blueprint(self, bp):
        if isinstance(bp, str):
            bp = import_string(bp)
        self.app.register_blueprint(bp, **self.get_blueprint_options(bp))

    def get_blueprint_options(self, bp=None):
        url_prefix = self.options["url_prefix"]
        if bp and bp.url_prefix:
            url_prefix = (url_prefix + "/" + bp.url_prefix.lstrip("/")).rstrip("/")
        return dict(url_prefix=url_prefix, subdomain=self.options["subdomain"])

    @hook("template_global", _force_call=True)
    def is_admin(self, user=None):
        if not current_app.features.users.logged_in():
            return False
        return current_app.features.users_acl.check_user_role(self.options["superadmin_role"], user)\
            or current_app.features.users_acl.check_user_role(self.options["admin_role"], user)