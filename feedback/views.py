from django.shortcuts import render, redirect
from .forms import FeedbackForm

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            new_feedback = form.save(commit=False)
            if request.user.is_authenticated:
                new_feedback.user = request.user
            else:
                new_feedback.user = None
            new_feedback.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})

def thank_you_view(request):
    return render(request, 'thank_you.html')
