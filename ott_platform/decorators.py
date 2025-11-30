from django.shortcuts import redirect

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('logged_in'):
            return redirect('/admin-panel/login/')
        return view_func(request, *args, **kwargs)
    return wrapper
