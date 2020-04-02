



from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (TemplateView,DetailView,
                                  ListView,UpdateView,
                                  CreateView,DeleteView)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comment
from django.urls import reverse_lazy
from blog.forms import PostForm,Comment
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date_isnull = True).order_by('created_date')

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk = pk)
    post.publish
    return redirect('post_detail')


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk = pk)
    if request.method == 'Post':
        form = CommentForm(request.Post)
        if form.is_valid():
            comment = form.save(comment=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
        else:
            form = CommentForm()
        return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post.pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post.pk)




