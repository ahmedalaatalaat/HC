from importlib import import_module
try:
    from django.core.urlresolvers import reverse
except ImportError:  # Django 1.11
    from django.urls import reverse

from django.template.loader import render_to_string
from jet.dashboard import modules
from jet.dashboard.models import UserDashboardModule
from django.utils.translation import ugettext_lazy as _
from jet.ordered_set import OrderedSet
from jet.utils import get_admin_site_name, context_to_dict
from django.utils.translation import activate

try:
    from django.template.context_processors import csrf
except ImportError:
    from django.core.context_processors import csrf
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class DefaultIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)

        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                ['English version', '/en/admin/'],
                ['النسخة العربية', '/ar/admin/'],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ],
            column=1,
            order=0
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('admin.*', 'auth.*'),
            column=1,
            order=1
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('admin.*', 'auth.*'),
            column=0,
            order=1
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            10,
            column=2,
            order=0
        ))