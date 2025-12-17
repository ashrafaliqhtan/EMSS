from django.http import HttpResponseForbidden

def committee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.userprofile.role != 'COMMITTEE':
            return HttpResponseForbidden("Access Denied")
        return view_func(request, *args, **kwargs)
    return wrapper