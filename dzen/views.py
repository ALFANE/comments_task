from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from dzen.forms import CommentForm
from dzen.models import Comment


# Create your views here.

class Hello(View):

    def get(self, request):

        return HttpResponse('Hello')

class CommentsView(View):

    def get(self, request):

        comment_form = CommentForm()
        comments = Comment.objects.filter(main_comment__isnull=True).prefetch_related('replies')
        context = {
            'comment_form': comment_form,
            'comments': comments,
        }

        return render(
            request = request,
            template_name = 'index.html',
            context = context
        )

    def post(self, request):

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()

        return redirect(reverse('comments_list'))