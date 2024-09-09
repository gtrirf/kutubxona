from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, DeleteView, UpdateView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.utils import timezone
from .models import Book, CommentBook, Queue, Rental, Category, Tili, Yozuvi, Author
from .forms import CommentBookForm, RentalForm
from django.http import JsonResponse    
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Rental

class BookListView(ListView):
    model = Book
    template_name = 'books_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        languages = self.request.GET.getlist('language')
        writing = self.request.GET.get('writing')
        author = self.request.GET.get('author')

        if category:
            if category.isdigit():
                queryset = queryset.filter(category_id=category)
        
        if languages:
            languages = [lang for lang in languages if lang.isdigit()]
            if languages:
                queryset = queryset.filter(tili_id__in=languages)

        if writing:
            if writing.isdigit():
                queryset = queryset.filter(yozuvi_id=writing)

        if author and author.isdigit():
            queryset = queryset.filter(author_id=author)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['languages'] = Tili.objects.all()
        context['writings'] = Yozuvi.objects.all()
        context['authors'] = Author.objects.all()
        context['selected_languages'] = self.request.GET.getlist('language')
        context['selected_category'] = self.request.GET.get('category')
        context['selected_writing'] = self.request.GET.get('writing')
        context['selected_author'] = self.request.GET.get('author')
        return context
    

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentBookForm()
        context['comments'] = CommentBook.objects.filter(book=self.object)
        context['has_rented'] = Rental.objects.filter(book=self.object, user=self.request.user).exists()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(CommentBook, id=comment_id, user=request.user)
            comment.delete()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            
            return redirect('book_detail', pk=self.object.pk)

        form = CommentBookForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = self.object
            comment.user = request.user
            comment.save()
            return redirect('book_detail', pk=self.object.pk)
        
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return render(request, self.template_name, context)



class BookPdfDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        if book.book_pdf:
            response = FileResponse(book.book_pdf, as_attachment=True)
            response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
            return response
        else:
            raise Http404("PDF file not available")


# def rent_book(request, book_id):
#     book = Book.objects.get(id=book_id)
#     if request.method == 'POST':
#         return_due_date = request.POST.get('return_due_date')
#         rental = Rental.objects.create(
#             book=book,
#             user=request.user,
#             return_due_date=return_due_date
#         )
#         return redirect('rental_confirmation', rental_id=rental.id)
#     return render(request, 'rent_book.html', {'book': book})


# def queue_book(request, book_id):
#     book = get_object_or_404(Book, id=book_id)

#     existing_queue = Queue.objects.filter(book=book, user=request.user).exists()
#     if existing_queue:
#         messages.error(request, 'You have already joined the queue for this book.')
#         return redirect('book_detail', pk=book_id)

#     queue_entry = Queue.objects.create(book=book, user=request.user)
    
#     return redirect('queue_status', queue_id=queue_entry.id)



# class QueueStatusView(View):
#     def get(self, request, queue_id):
#         queue = get_object_or_404(Queue, id=queue_id)
#         position = Queue.objects.filter(book=queue.book, request_date__lte=queue.request_date).count()
#         return render(request, 'queue_status.html', {'queue': queue, 'book': queue.book, 'position': position})

    

# class RentalCreateView(CreateView):
#     model = Rental
#     form_class = RentalForm
#     template_name = 'rental_form.html'

#     def form_valid(self, form):
#         return_due_date = form.cleaned_data['return_due_date']
#         if return_due_date > (datetime.now() + timedelta(days=15)).date():
#             form.add_error('return_due_date', 'The return date cannot exceed 15 days.')
#             return self.form_invalid(form)
#         return super().form_valid(form)




# class RentalCreateView(CreateView):
#     model = Rental
#     form_class = RentalForm
#     template_name = 'rental_form.html'

#     def form_valid(self, form):
#         book = get_object_or_404(Book, pk=self.kwargs['pk'])
#         return_due_date = form.cleaned_data['return_due_date']
#         max_rental_period = timezone.now() + timezone.timedelta(days=15)

#         if return_due_date > max_rental_period:
#             form.add_error('return_due_date', 'The maximum rental period is 15 days.')
#             return self.form_invalid(form)

#         if book.quantity <= 0:
#             return redirect('queue_book', book_id=book.pk)

#         rental = form.save(commit=False)
#         rental.book = book
#         rental.user = self.request.user
#         rental.save()
#         book.quantity -= 1
#         book.save()

#         return redirect('rental_confirmation', rental_id=rental.id)


# def rental_confirmation(request, rental_id):
#     rental = get_object_or_404(Rental, id=rental_id)
#     return render(request, 'rental_confirmation.html', {'rental': rental})