from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LeadForm

def landing_page(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('core:landing_page')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LeadForm()

    return render(request, 'core/index.html', {'form': form})

def properties_page(request):
    return render(request, 'core/properties.html')
