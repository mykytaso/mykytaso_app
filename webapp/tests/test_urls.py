from django.test import TestCase
from django.urls import reverse

from users.models import User
from webapp.models import Post


USER_EMAIL = "test_user@test.com"
USER_PASSWORD = "test_dffhsf232iife87"


class TestUrls(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            position=1,
            cover_title="Post 1 Title",
            cover_description="Post 1 Description",
            cover_image="post_1_image.jpg",
        )

        self.superuser = User.objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )

    def check_response(self, url_name: str, args=None, methods_expected: dict = {}):
        """
        Check the response status for a given URL and HTTP method.
        """
        for method, expected_status in methods_expected.items():

            # subTest shows exactly which method failed
            with self.subTest(url=url_name, method=method):
                url = reverse(url_name, args=args) if args else reverse(url_name)
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, expected_status)

    def test_public_urls_anonymous(self):
        self.check_response(
            "webapp:index",
            methods_expected={"get": 200, "post": 405, "put": 405, "delete": 405},
        )
        self.check_response(
            "webapp:about_me",
            methods_expected={"get": 200, "post": 405, "put": 405, "delete": 405},
        )
        self.check_response(
            "webapp:resume",
            methods_expected={"get": 302, "post": 302, "put": 302, "delete": 302},
        )
        self.check_response(
            "webapp:send_message",
            methods_expected={"get": 200, "post": 200, "put": 200, "delete": 405},
        )
        self.check_response(
            "webapp:post_detail",
            args=[self.post.id],
            methods_expected={"get": 200, "post": 405, "put": 405, "delete": 405},
        )

    def test_protected_urls_anonymous(self):
        self.check_response(
            "webapp:post_create",
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:post_update",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:post_delete",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:post_change_position",
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:block_create",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:block_delete",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:block_change_position",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:tag_create",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:tag_delete",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )

    def test_public_urls_user_logged_in(self):
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        self.check_response(
            "webapp:index",
            methods_expected={"get": 200, "post": 405, "put": 405, "delete": 405},
        )
        self.check_response(
            "webapp:about_me",
            methods_expected={"get": 200, "post": 405, "put": 405, "delete": 405},
        )
        self.check_response(
            "webapp:resume",
            methods_expected={"get": 302, "post": 302, "put": 302, "delete": 302},
        )
        self.check_response(
            "webapp:send_message",
            methods_expected={"get": 200, "post": 200, "put": 200, "delete": 405},
        )
        self.check_response(
            "webapp:post_detail",
            args=[self.post.id],
            methods_expected={"get": 200, "post": 405, "put": 405, "delete": 405},
        )

    def test_protected_urls_user_logged_in(self):
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        self.check_response(
            "webapp:post_create",
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:post_update",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:post_delete",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:post_change_position",
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:block_create",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:block_delete",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:block_change_position",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:tag_create",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
        self.check_response(
            "webapp:tag_delete",
            args=[self.post.id],
            methods_expected={"get": 403, "post": 403, "put": 403, "delete": 403},
        )
