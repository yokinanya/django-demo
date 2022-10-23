from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

# user_groups = ['logs', 'api', 'download_data']

user_groups = ['api', '销售', '跟单员', '售后', '财务']


def check_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied("You do not have permission to access this Page")


def check_user_group(user, group_name):
    user_group = user.groups.all().values_list('name', flat=True)
    if group_name not in user_group:
        raise PermissionDenied("You do not have permission to access this Page")


def allowed_groups(group_name=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in group_name:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("You do not have permission to access this Page")

        return wrapper_func

    return decorator


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser
