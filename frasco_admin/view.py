from frasco import Blueprint, current_context, pass_feature, ActionsView, ActionsFunctionViewMixin
import inflection


class AdminView(ActionsView):
    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop("admin_title", None)
        self.description = kwargs.pop("admin_desc", None)
        self.sidebar_menu = kwargs.pop("admin_menu", None)
        self.sidebar_menu_icon = kwargs.pop("admin_menu_icon", None)
        super(AdminView, self).__init__(*args, **kwargs)

    def register(self, app, bp=None):
        if self.sidebar_menu:
            endpoint = (bp.name + "." if bp else "") + self.name
            app.features.menu["admin"].add_child(endpoint, self.sidebar_menu,
                endpoint, icon=self.sidebar_menu_icon)
        super(AdminView, self).register(app, bp)

    def dispatch_request(self, *args, **kwargs):
        current_context["admin_section_title"] = self.title or inflection.humanize(self.name)
        current_context["admin_section_desc"] = self.description
        return super(AdminView, self).dispatch_request(*args, **kwargs)


class AdminFunctionView(ActionsFunctionViewMixin, AdminView):
    pass


class AdminBlueprint(Blueprint):
    view_class = AdminFunctionView

    def __init__(self, *args, **kwargs):
        self.roles = kwargs.pop("roles", [])
        super(AdminBlueprint, self).__init__(*args, **kwargs)
        self.before_request(self.init_admin)

    @pass_feature("admin", "users", "users_acl")
    def init_admin(self, admin, users, users_acl):
        users.login_required()
        if not users_acl.check_user_role(admin.options["superadmin_role"]):
            if not users_acl.check_user_role([admin.options["admin_role"]] + self.roles):
                username = getattr(users.current, users.options["username_column"], None)
                if username in admin.options["superadmins"]:
                    admin.make_superadmin(users.current)
                else:
                    current_context.exit(users_acl.unauthorized())
