from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.viewsets import ModelViewSet

from dzen.emails import send_email
from dzen.forms import CommentForm
from dzen.models import Comment
from dzen.serializers import CommentSerializer


class CommentsView(View):
    def get(self, request):
        """
        Обрабатывает GET-запросы для отображения списка комментариев.
        Поддерживает сортировку и пагинацию комментариев.
        Создает форму для добавления нового комментария и передает ее в контекст шаблона.
        """
        # Определение порядка сортировки и параметры пагинации
        sort_by = request.GET.get("sort", "created_at_desc")
        allowed_sort_fields = {
            "created_at": "created_at",
            "created_at_desc": "-created_at",
            "username": "username",
            "email": "email",
        }
        sort_by = allowed_sort_fields.get(sort_by, "-created_at")

        # Получение формы для добавления комментария
        comment_form = CommentForm()

        # Получение и сортировка комментариев
        comments_list = (
            Comment.objects.filter(main_comment=None)
            .prefetch_related("replies")
            .order_by(sort_by)
        )
        paginator = Paginator(comments_list, 25)
        page = request.GET.get("page")

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        context = {
            "comment_form": comment_form,
            "comments": comments,
        }

        return render(request=request, template_name="index.html", context=context)

    def get_comment_tree(self, comments):
        """
        Построение древовидной структуры комментариев для отображения ответов на комментарии.
        """
        comment_tree = []
        for comment in comments:
            node = {
                'id': comment.id,
                'username': comment.username,
                'message': comment.message,
                'replies': self.get_comment_tree(comment.replies.all())
            }
            comment_tree.append(node)
        return comment_tree

    def post(self, request):
        """
        Обрабатывает POST-запросы для добавления нового комментария.
        В случае успешной валидации данных формы, сохраняет комментарий и отправляет подтверждающее письмо.
        Перенаправляет на страницу со списком комментариев.
        """
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            send_email(
                recipient_list=[
                    # Раскомментировать в случае рассылки на email
                    # comment_form.cleaned_data["email"],
                ]
            )
            comment_form.save()

        return redirect(reverse("comments_list"))


class CommentsViewSet(ModelViewSet):
    """
    Реализует REST API для комментариев.
    Позволяет выполнять CRUD-операции через API-интерфейс.
    Использует сериализацию данных для преобразования объектов модели в формат JSON и обратно.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = (
        "id",
        "username",
        "email",
        "created_at",
        "updated_at",
    )
