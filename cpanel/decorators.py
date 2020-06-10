from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render


def allowed_users(allowed_roles=[]):
    def decorator(view):
        def wrapper(request, *args, **kwargs):

            group = request.user.groups.filter(name__in=allowed_roles).exists()

            if group:
                return view(request, *args, **kwargs)
            else:
                return render(request, 'cpanel/Error/unauthorized-Error.html')
        return wrapper
    return decorator
