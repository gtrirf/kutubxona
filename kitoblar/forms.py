from django import forms
from .models import CommentBook, Queue, Rental

class CommentBookForm(forms.ModelForm):
    class Meta:
        model = CommentBook
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'comment': 'Comment',
        }

class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = []

class RentalForm(forms.ModelForm):
    return_due_date = forms.DateField(widget=forms.SelectDateWidget)
    
    class Meta:
        model = Rental
        fields = ['return_due_date']
