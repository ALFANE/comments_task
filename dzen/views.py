from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.viewsets import ModelViewSet

from dzen.emails import send_email
from dzen.forms import CommentForm
from dzen.models import Comment
from dzen.serializers import CommentSerializer


# Класс CommentsView отвечает за отображение и обработку запросов, связанных с комментариями.
# Включает методы для отображения списка комментариев и обработки формы добавления нового комментария.


class CommentsView(View):
    def get(self, request):
        # Обрабатывает GET-запросы для получения списка комментариев.
        # Извлекает параметры запроса, такие как порядок сортировки и номер страницы для пагинации.
        # Создает и передает форму для добавления новых комментариев в контекст шаблона.
        # Выполняет пагинацию для управления отображением большого количества комментариев.
        # Передает контекст в шаблон для рендеринга страницы с комментариями.

        sort_by = request.GET.get("sort", "created_at_desc")
        allowed_sort_fields = {
            "created_at": "created_at",
            "created_at_desc": "-created_at",
            "username": "username",
            "email": "email",
        }
        sort_by = allowed_sort_fields.get(sort_by, "-created_at")
        comment_form = CommentForm()
        comments_list = (
            Comment.objects.filter(main_comment__isnull=True)
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

    def post(self, request):
        # Обрабатывает POST-запросы для добавления нового комментария.
        # Валидирует данные формы и, в случае успешной валидации, сохраняет новый комментарий в базе данных.
        # Отправляет подтверждающее письмо на указанный в форме email-адрес.
        # После сохранения комментария перенаправляет пользователя на страницу со списком комментариев.

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            send_email(
                recipient_list=[
                    # comment_form.cleaned_data["email"],
                    #раскоментировать в случае рассылки на email
                ]
            )
            comment_form.save()

        return redirect(reverse("comments_list"))


# Класс CommentsViewSet реализует REST API для работы с комментариями.
# Позволяет выполнять операции создания, чтения, обновления и удаления (CRUD) через API-интерфейс.
# Использует сериализацию данных для преобразования объектов модели в формат JSON и обратно.


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = (
        "id",
        "username",
        "email",
        "created_at",
        "updated_at",
    )
