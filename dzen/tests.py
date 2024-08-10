
import freezegun
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from dzen.models import Comment

# Тесты для проверки CRUD операций над моделью Comment
@freezegun.freeze_time("2024-08-09 00:00:00")
class CommentApiTests(APITestCase):
    def setUp(self):
        # Инициализация тестовых данных с использованием библиотеки Faker
        self.faker = Faker()
        self.comment = Comment.objects.create(
            username=self.faker.user_name(),
            email=self.faker.email(),
            home_page=self.faker.url(),
            message=self.faker.text(),
        )
        self.comment_id = self.comment.id

    def test_create_comment(self):
        # Тест создания нового комментария через API
        response = self.client.post(
            reverse("comments_api_viewset-list"),
            data={
                "username": self.faker.user_name(),
                "email": self.faker.email(),
                "home_page": self.faker.url(),
                "message": self.faker.text(),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data["username"], response.data["username"])

    def test_read_comment(self):
        # Тест получения списка комментариев через API
        response = self.client.get(reverse("comments_api_viewset-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertNotEqual(response_data, {"count": 0, "next": None, "previous": None, "results": []})
        self.assertEqual(response_data["count"], 1)
        comment_data = response_data["results"][0]
        self.assertEqual(comment_data["id"], self.comment_id)
        self.assertEqual(comment_data["username"], Comment.objects.get(id=self.comment_id).username)

    def test_update_comment(self):
        # Тест обновления комментария через API
        new_username = self.faker.user_name()
        response = self.client.put(
            reverse("comments_api_viewset-detail", args=[self.comment_id]),
            data={
                "username": new_username,
                "email": self.comment.email,
                "home_page": self.comment.home_page,
                "message": self.comment.message,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(id=self.comment_id).username, new_username)

    def test_delete_comment(self):
        # Тест удаления комментария через API
        response = self.client.delete(
            reverse("comments_api_viewset-detail", args=[self.comment_id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
