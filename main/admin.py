from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.translation import activate
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import User, Group


admin.site.site_header = "BlueCare System"
admin.site.site_title = "BlueCare"
admin.site.site_url = None


class HC_AdminSite(AdminSite):
    site_header = "BlueCare System"
    site_title = "BlueCare"
    site_url = None

    def each_context(self, request):
        if '/ar/' in request.get_full_path():
            activate('ar')
        else:
            activate('en')
        return super().each_context(request)


class LogEntry_admin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    readonly_fields = [f.name for f in LogEntry._meta.get_fields()]
    list_display = [
        'id',
        'done_by_id',
        'done_by_username',
        'content_type',
        'action_flag_',
        'done_on_id',
        'action',
        'change_message',
        'action_time',
    ]

    list_filter = [
        'content_type',
        'action_flag',
        'action_time'
    ]

    # search_fields = ('user', 'user__first_name', )
    search_fields = [
        'user__id',
        'user__username'
    ]

    ordering = ['action_time', 'change_message']

    def action(self, obj):
        return obj.get_change_message()

    def done_by_id(self, obj):
        return obj.user_id

    def done_on_id(self, obj):
        return obj.object_id

    def done_by_username(self, obj):
        if obj.user.first_name:
            return obj.user.first_name
        return None

    def action_flag_(self, obj):
        flags = {
            1: "Addition",
            2: "Changed",
            3: "Deleted",
        }
        return flags[obj.action_flag]


my_admin_site = HC_AdminSite()

my_admin_site.register(LogEntry, LogEntry_admin)
my_admin_site.register(User, UserAdmin)
my_admin_site.register(Group, GroupAdmin)
