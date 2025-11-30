from django.shortcuts import render, redirect

def login_page(request):
    if request.method == "POST":
        request.session['logged_in'] = True
        return redirect('/movies/')
    return render(request, 'accounts/login.html')

def logout_page(request):
    request.session.flush()
    return redirect('/accounts/')
