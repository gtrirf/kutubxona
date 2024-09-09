from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.urls import reverse_lazy
from .models import Post, Comment, LibraryImages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, CommentForm
from django.views.generic import DeleteView, DetailView, ListView
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin
from django.db.models import Q
from kitoblar.models import Book


class BlogListView(View):
    def get(self, request):
        blogs = Post.objects.all().order_by('-id')
        images = LibraryImages.objects.all()
        paginator = Paginator(blogs, 4  ) 
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'blogs': blogs,
            'images': images
        }
        return render(request, 'main-pages/home.html', context=context)


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get(self, request):
        create_form = PostForm()
        context = {'create_form': create_form}
        return render(request, 'blogs/blogs_create.html', context=context)

    def post(self, request):
        create_form = PostForm(request.POST, request.FILES)
        if create_form.is_valid():
            new_post = create_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('home:home')
        else:
            context = {'create_form': create_form}
            return render(request, 'blogs/blogs_create.html', context=context)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        blog = self.get_object()
        return (blog.author == self.request.user) or self.request.user.is_staff or self.request.user.is_superuser

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        blog = self.get_object()
        update_form = PostForm(instance=blog)
        context = {'update_form': update_form}
        return render(request, 'blogs/blog_update.html', context=context)

    def post(self, request, pk):
        blog = self.get_object()
        update_form = PostForm(request.POST, request.FILES, instance=blog)
        if update_form.is_valid():
            update_form.save()
            return redirect('home:home')
        else:
            context = {'update_form': update_form}
            return render(request, 'blogs/blog_update.html', context=context)


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blogs/blog_delete.html'
    success_url = reverse_lazy('home:home')

    def test_func(self):
        blog = self.get_object()
        return (blog.author == self.request.user) or self.request.user.is_staff or self.request.user.is_superuser


class BlogDetailView(LoginRequiredMixin, DetailView, FormMixin):
    model = Post
    template_name = 'blogs/blogs_detail.html'
    context_object_name = 'blog'
    form_class = CommentForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['recommended_blogs'] = Post.objects.exclude(pk=self.object.pk).order_by('-id')[:5]
        return context


    def post(self, request, *args, **kwargs):
        if 'edit_comment' in request.POST:
            return self.edit_comment(request, *args, **kwargs)
        elif 'delete_comment' in request.POST:
            return self.delete_comment(request, *args, **kwargs)
        else:
            return self.create_comment(request, *args, **kwargs)


    def create_comment(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.user = request.user
            comment.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('blogs/comment.html', {'comment': comment}, request=request)
                return JsonResponse({'status': 'success', 'html': html})

            return redirect(request.path)


        context = self.get_context_data(object=self.object, form=form)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)

        return render(request, self.template_name, context)


    def delete_comment(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})

        return redirect(request.path)


class SearchResultsView(ListView):
    template_name = 'main-pages/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get("q")
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        # book_list = Book.objects.filter(
        #     Q(title__icontains=query) | Q(author__full_name__icontains=query)
        # )
        combined_list = list(post_list) # Combine the querysets
        return combined_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        context['query'] = query  # To keep track of the search term
        return context