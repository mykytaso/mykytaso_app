from django.test import TestCase
from django.urls import reverse

from users.models import User
from webapp.forms import MessageForm
from webapp.models import Post, Message

USER_EMAIL = "test_user@test.com"
USER_PASSWORD = "test_dffhsf232iife87"

SUPERUSER_EMAIL = "test_superuser@test.com"
SUPERUSER_PASSWORD = "test_sdff3987r3uifss"


class TestPostViews(TestCase):
    def setUp(self):

        self.post_1 = Post.objects.create(
            position=1,
            cover_title="Post 1 Title",
            cover_description="Post 1 Description",
            cover_image="post_1_image.jpg",
        )

        self.post_2 = Post.objects.create(
            position=2,
            cover_title="Post 2 Title",
            cover_description="Post 2 Description",
            cover_image="post_2_image.jpg",
        )

        self.user = User.objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )

        self.superuser = User.objects.create_superuser(
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD,
        )

        self.post_list_url = reverse("webapp:index")
        self.post_create_url = reverse("webapp:post_create")
        # self.post_update_url = reverse("webapp:post_update", args=[self.post_1.id])
        self.post_delete_url = reverse("webapp:post_delete", args=[self.post_1.id])
        self.post_change_position_url = reverse("webapp:post_change_position")


        self.post_data = {
            "cover_title": "New Post",
            "cover_description": "New Post Description",
            "cover_image": "cover_image.jpg",
        }

        self.post_data_update = {
            "cover_title": "Updated Post",
            "cover_description": "Updated Post Description",
            "cover_image": "updated_cover_image.jpg",
        }


    def test_post_list_view_get_method_anonymous(self):
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "webapp/index.html")

    def test_post_list_view_get_method_user_logged_in(self):
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        response = self.client.get(self.post_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "webapp/index.html")
        self.assertIn("object_list", response.context)
        self.assertQuerySetEqual(
            response.context["object_list"],
            Post.objects.all().order_by("-position"),
            ordered=True,
        )

        # Check if the user can see the plus icon (new post creation button)
        self.assertNotIn(
            "<i class='bi bi-plus-square-fill h4'></i>", response.content.decode()
        )

        # Check if the superuser can see the post editing panel
        for editing_button in [
            '<i class="bi bi-caret-left"></i>',
            '<i class="bi bi-pen"></i>',
            '<i class="bi bi-trash"></i>',
            '<i class="bi bi-caret-right"></i>',
        ]:
            self.assertNotIn(editing_button, response.content.decode())

    def test_post_list_view_get_method_superuser_logged_in(self):
        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

        response = self.client.get(self.post_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "webapp/index.html")
        self.assertIn("object_list", response.context)
        self.assertQuerySetEqual(
            response.context["object_list"],
            Post.objects.all().order_by("-position"),
            ordered=True,
        )
        # Check if the superuser can see the plus icon (new post creation button)
        self.assertIn(
            '<i class="bi bi-plus-square-fill h4"></i>', response.content.decode()
        )

        # Check if the superuser can see the post editing panel
        for editing_button in [
            '<i class="bi bi-caret-left"></i>',
            '<i class="bi bi-pen"></i>',
            '<i class="bi bi-trash"></i>',
            '<i class="bi bi-caret-right"></i>',
        ]:
            self.assertIn(editing_button, response.content.decode())

    def test_post_create_view_post_method_anonymous(self):
        posts_count_before = Post.objects.count()
        response = self.client.post(
            self.post_create_url,
            data=self.post_data,
        )
        posts_count_after = Post.objects.count()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(posts_count_after, posts_count_before)


    def test_post_create_view_post_method_user_logged_in(self):
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        posts_count_before = Post.objects.count()
        response = self.client.post(
            self.post_create_url,
            data=self.post_data,
        )
        posts_count_after = Post.objects.count()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(posts_count_after, posts_count_before)


    def test_post_create_view_post_method_superuser_logged_in(self):
        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

        posts_count_before = Post.objects.count()
        response = self.client.post(
            self.post_create_url,
            data=self.post_data,
        )
        posts_count_after = Post.objects.count()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.post_list_url)
        self.assertEqual(posts_count_after, posts_count_before + 1)



    def test_post_update_view_post_method_anonymous(self):
        post_id = self.post_1.id
        response = self.client.post(
            reverse("webapp:post_update", args=[post_id]),
            data=self.post_data_update,
        )

        self.assertEqual(response.status_code, 403)

    def test_post_update_view_post_method_user_logged_in(self):
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        post_id = self.post_1.id
        response = self.client.post(
            reverse("webapp:post_update", args=[post_id]),
            data=self.post_data_update,
        )

        self.assertEqual(response.status_code, 403)

    def test_post_update_view_post_method_superuser_logged_in(self):
        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

        post_id = self.post_1.id
        response = self.client.post(
            reverse("webapp:post_update", args=[post_id]),
            data=self.post_data_update,
        )
        updated_post = Post.objects.get(id=post_id)


        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.post_list_url)

        self.assertEqual(updated_post.cover_title, self.post_data_update["cover_title"])
        self.assertEqual(
            updated_post.cover_description, self.post_data_update["cover_description"]
        )

    def test_post_delete_view_post_method_anonymous(self):
        response = self.client.post(
            reverse("webapp:post_delete", args=[self.post_1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_post_delete_view_post_method_user_logged_in(self):
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        response = self.client.post(
            reverse("webapp:post_delete", args=[self.post_1.id]),
        )

        self.assertEqual(response.status_code, 403)

    def test_post_delete_view_post_method_superuser_logged_in(self):
        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

        response = self.client.post(
            reverse("webapp:post_delete", args=[self.post_1.id]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.post_list_url)

        # Check if the post has been deleted
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post_1.id)

    def test_post_change_position_view_post_method_anonymous(self):
        response = self.client.post(
            self.post_change_position_url,
            {"post_position": 1, "position": "left"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.content.decode(),
            "Forbidden: You do not have permission to access this page.",
        )

    def test_post_change_position_view_post_method_user_logged_in(self):
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        response = self.client.post(
            self.post_change_position_url,
            {"post_position": 1, "position": "left"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.content.decode(),
            "Forbidden: You do not have permission to access this page.",
        )

    def test_post_change_position_view_post_method_superuser_logged_in(self):
        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

        response = self.client.post(
            self.post_change_position_url,
            {"post_position": 1, "position_direction": "left"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.post_list_url)

        # Check if the post positions have been swapped
        post_1_old_position = self.post_1.position
        post_2_old_position = self.post_2.position
        self.post_1.refresh_from_db()
        self.post_2.refresh_from_db()
        self.assertEqual(self.post_1.position, post_2_old_position)
        self.assertEqual(self.post_2.position, post_1_old_position)



class TestAboutMeView(TestCase):
    def setUp(self):
        self.about_me_url = reverse("webapp:about_me")

    def test_about_me_view_get_method_anonymous(self):
        response = self.client.get(self.about_me_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "webapp/about_me.html")


class TestResumeView(TestCase):
    def setUp(self):
        self.resume_url = reverse("webapp:resume")

    def test_resume_view_get_method_anonymous(self):
        response = self.client.get(self.resume_url)
        self.assertEqual(response.status_code, 302)


class TestMessageCreateView(TestCase):
    def setUp(self):
        self.message_create_url = reverse("webapp:send_message")

        self.message_data = {
            "email": "test@test.com",
            "content": "Test message content",
        }

    def test_message_create_view_get_method_anonymous(self):
        response = self.client.get(self.message_create_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "webapp/message_form.html")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], MessageForm)

    def test_message_create_view_post_method_anonymous(self):
        response = self.client.post(
            self.message_create_url,
            data=self.message_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.message_create_url)

        # Check if the message was created
        message = Message.objects.get(email=self.message_data["email"])
        self.assertEqual(message.content, self.message_data["content"])
