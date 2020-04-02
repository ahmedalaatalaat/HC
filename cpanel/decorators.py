from django.shortcuts import redirect
from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view):
        def wrapper(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            print(group)
            if group in allowed_roles:
                return view(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper
    return decorator
