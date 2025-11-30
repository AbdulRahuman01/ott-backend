from django.shortcuts import render
from ott_platform.decorators import login_required

#login_required
def reports_page(request):
    return render(request, 'reports/reports.html')
