from django.shortcuts import redirect
from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view):
        def wrapper(request, *args, **kwargs):

            group = request.user.groups.filter(name__in=allowed_roles).exists()

            if group:
                return view(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper
    return decorator
