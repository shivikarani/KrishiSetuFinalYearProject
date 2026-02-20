from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role != role:
                return redirect('/')  # Redirect if role doesn't match
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator