from django.contrib.contenttypes.models import ContentType
from django.db.models import Max
from django.test import TestCase
from django.urls import reverse

from users.models import User
from webapp.forms import MessageForm
from webapp.models import Post, Message, Block, Text, Space, Comment

USER_EMAIL = "test_user@test.com"
USER_PASSWORD = "test_dffhsf232iife87"

ANOTHER_USER_EMAIL = "test_another_user@test.com"
ANOTHER_USER_PASSWORD = "test_ophsferger4iife87"

SUPERUSER_EMAIL = "test_superuser@test.com"
SUPERUSER_PASSWORD = "test_sdff3987r3uifss"

ANOTHER_SUPERUSER_EMAIL = "test_another_superuser@test.com"
ANOTHER_SUPERUSER_PASSWORD = "test_3r4uifss"


class TestPostViewsAnonymous(TestCase):
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
        response = self.client.get(reverse("webapp:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "webapp/index.html")

    def test_post_create_view_post_method_anonymous(self):
        posts_count_before = Post.objects.count()
        response = self.client.post(
            reverse("webapp:post_create"),
            data=self.post_data,
        )
        posts_count_after = Post.objects.count()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(posts_count_after, posts_count_before)

    def test_post_update_view_post_method_anonymous(self):
        post_id = self.post_1.id
        response = self.client.post(
            reverse("webapp:post_update", args=[post_id]),
            data=self.post_data_update,
        )

        self.assertEqual(response.status_code, 403)

    def test_post_delete_view_post_method_anonymous(self):
        response = self.client.post(
            reverse("webapp:post_delete", args=[self.post_1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_post_change_position_view_post_method_anonymous(self):
        response = self.client.post(
            reverse("webapp:post_change_position"),
            {"post_position": 1, "position": "left"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.content.decode(),
            "Forbidden: You do not have permission to access this page.",
        )


class TestPostViewsUserLoggedIn(TestCase):
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

        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

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

    def test_post_list_view_regular_user_cannot_see_superuser_buttons(self):
        response = self.client.get(reverse("webapp:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "webapp/index.html")
        self.assertIn("object_list", response.context)
        self.assertQuerySetEqual(
            response.context["object_list"],
            Post.objects.all().order_by("-position"),
            ordered=True,
        )

        # Check if the regular user can see the plus icon (new post creation button)
        self.assertNotIn(
            "<i class='bi bi-plus-square-fill h4'></i>", response.content.decode()
        )

        # Check if the regular user can see the post editing panel
        for editing_button in [
            '<i class="bi bi-caret-left"></i>',
            '<i class="bi bi-pen"></i>',
            '<i class="bi bi-trash"></i>',
            '<i class="bi bi-caret-right"></i>',
        ]:
            self.assertNotIn(editing_button, response.content.decode())

    def test_post_create_view_post_method_user_logged_in(self):
        posts_count_before = Post.objects.count()
        response = self.client.post(
            reverse("webapp:post_create"),
            data=self.post_data,
        )
        posts_count_after = Post.objects.count()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(posts_count_after, posts_count_before)

    def test_post_update_view_post_method_user_logged_in(self):
        post_id = self.post_1.id
        response = self.client.post(
            reverse("webapp:post_update", args=[post_id]),
            data=self.post_data_update,
        )

        self.assertEqual(response.status_code, 403)

    def test_post_delete_view_post_method_user_logged_in(self):
        response = self.client.post(
            reverse("webapp:post_delete", args=[self.post_1.id]),
        )

        self.assertEqual(response.status_code, 403)

    def test_post_change_position_view_post_method_user_logged_in(self):
        response = self.client.post(
            reverse("webapp:post_change_position"),
            {"post_position": 1, "position": "left"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.content.decode(),
            "Forbidden: You do not have permission to access this page.",
        )


class TestPostViewsSuperUserLoggedIn(TestCase):
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

        self.superuser = User.objects.create_superuser(
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD,
        )

        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

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

    def test_post_list_view_get_method_superuser_logged_in(self):
        response = self.client.get(reverse("webapp:index"))

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

    def test_post_create_view_post_method_superuser_logged_in(self):
        posts_count_before = Post.objects.count()
        response = self.client.post(
            reverse("webapp:post_create"),
            data=self.post_data,
        )
        posts_count_after = Post.objects.count()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:index"))
        self.assertEqual(posts_count_after, posts_count_before + 1)

    def test_post_update_view_post_method_superuser_logged_in(self):
        post_id = self.post_1.id
        response = self.client.post(
            reverse("webapp:post_update", args=[post_id]),
            data=self.post_data_update,
        )
        updated_post = Post.objects.get(id=post_id)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:index"))

        self.assertEqual(updated_post.cover_title, self.post_data_update["cover_title"])
        self.assertEqual(
            updated_post.cover_description, self.post_data_update["cover_description"]
        )

    def test_post_delete_view_post_method_superuser_logged_in(self):
        response = self.client.post(
            reverse("webapp:post_delete", args=[self.post_1.id]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:index"))

        # Check if the post has been deleted
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post_1.id)

    def test_post_change_position_view_post_method_superuser_logged_in(self):
        response = self.client.post(
            reverse("webapp:post_change_position"),
            {"post_position": 1, "position_direction": "left"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:index"))

        # Check if the post positions have been swapped
        post_1_old_position = self.post_1.position
        post_2_old_position = self.post_2.position
        self.post_1.refresh_from_db()
        self.post_2.refresh_from_db()
        self.assertEqual(self.post_1.position, post_2_old_position)
        self.assertEqual(self.post_2.position, post_1_old_position)


class TestBlockViewsAnonymous(TestCase):
    def setUp(self):

        self.post_1 = Post.objects.create(
            position=1,
            cover_title="Post 1 Title",
            cover_description="Post 1 Description",
            cover_image="post_1_image.jpg",
        )

    def test_block_create_view_post_method_anonymous(self):
        response = self.client.post(
            reverse("webapp:block_create", args=[self.post_1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_block_delete_view_post_method_anonymous(self):
        response = self.client.post(
            reverse("webapp:block_delete", args=[self.post_1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_block_change_position_view_post_method_anonymous(self):
        response = self.client.post(
            reverse("webapp:block_change_position", args=[self.post_1.id])
        )
        self.assertEqual(response.status_code, 403)


class TestBlockViewsUserLoggedIn(TestCase):
    def setUp(self):

        self.post_1 = Post.objects.create(
            position=1,
            cover_title="Post 1 Title",
            cover_description="Post 1 Description",
            cover_image="post_1_image.jpg",
        )

        self.user = User.objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

    def test_block_create_view_post_method_user_logged_in(self):
        response = self.client.post(
            reverse("webapp:block_create", args=[self.post_1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_block_delete_view_post_method_user_logged_in(self):
        response = self.client.delete(
            reverse("webapp:block_delete", args=[self.post_1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_block_change_position_view_post_method_user_logged_in(self):
        response = self.client.post(
            reverse("webapp:block_change_position", args=[self.post_1.id])
        )
        self.assertEqual(response.status_code, 403)


class TestBlockViewsSuperUserLoggedIn(TestCase):
    def setUp(self):

        self.post_1 = Post.objects.create(
            position=1,
            cover_title="Post 1 Title",
            cover_description="Post 1 Description",
            cover_image="post_1_image.jpg",
        )

        text = Text.objects.create(
            text="Test Block Text",
            text_type="normal",
            text_alignment="center",
        )

        space = Space.objects.create(
            space_number=10,
        )

        object_type_1 = ContentType.objects.get_for_model(text)
        max_position = Block.objects.filter(post=self.post_1).aggregate(Max("block_position"))
        block_position = (
            max_position["block_position__max"] + 1
            if max_position["block_position__max"]
            else 1
        )

        self.block_1 = Block.objects.create(
            post=self.post_1,
            object_type=object_type_1,
            object_id=text.id,
            block_position=block_position,
        )

        object_type_2 = ContentType.objects.get_for_model(space)
        max_position = Block.objects.filter(post=self.post_1).aggregate(Max("block_position"))
        block_position = (
            max_position["block_position__max"] + 1
            if max_position["block_position__max"]
            else 1
        )

        self.block_2 = Block.objects.create(
            post=self.post_1,
            object_type=object_type_2,
            object_id=space.id,
            block_position=block_position,
        )

        self.superuser = User.objects.create_superuser(
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD,
        )
        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)


    def test_block_create_view_post_method_super_user_logged_in(self):
        blocks_count_before = self.post_1.blocks.count()

        response = self.client.post(
            reverse("webapp:block_create", args=[self.post_1.id]),
            data={
                "text": "Test Block Text",
                "text_type": "normal",
                "text_alignment": "center",
            }
        )

        blocks_count_after = self.post_1.blocks.count()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:post_detail", args=[self.post_1.id]))
        self.assertEqual(blocks_count_after, blocks_count_before + 1)


    def test_block_delete_view_post_method_super_user_logged_in(self):
        response = self.client.post(
            reverse("webapp:block_delete", args=[self.post_1.id]),
            data={"block_id": self.block_1.id},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:post_detail", args=[self.post_1.id]))

        # Check if the block has been deleted
        with self.assertRaises(Block.DoesNotExist):
            Block.objects.get(id=self.block_1.id)


    def test_block_change_position_view_post_method_super_user_logged_in(self):
        response = self.client.post(
            reverse("webapp:block_change_position", args=[self.post_1.id]),
            data={"block_id": self.block_1.id, "block_direction": "down"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:post_detail", args=[self.post_1.id]))

        # Check if the block positions have been swapped
        block_1_old_position = self.block_1.block_position
        block_2_old_position = self.block_2.block_position
        self.block_1.refresh_from_db()
        self.block_2.refresh_from_db()
        self.assertEqual(self.block_1.block_position, block_2_old_position)
        self.assertEqual(self.block_2.block_position, block_1_old_position)


class TestCommentViewsAnonymous(TestCase):
    def setUp(self):

        self.post_1 = Post.objects.create(
            position=1,
            cover_title="Post 1 Title",
            cover_description="Post 1 Description",
            cover_image="post_1_image.jpg",
        )

    def test_comment_create_view_post_method_anonymous(self):
        response = self.client.post(
            reverse("webapp:comment_create", args=[self.post_1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_comment_delete_view_post_method_anonymous(self):
        response = self.client.post(
            reverse("webapp:comment_delete", args=[self.post_1.id]),
        )
        self.assertEqual(response.status_code, 403)


class TestCommentViewsUserLoggedIn(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )

        self.another_user = User.objects.create_user(
            email=ANOTHER_USER_EMAIL,
            password=ANOTHER_USER_PASSWORD,
        )

        self.post_1 = Post.objects.create(
            position=1,
            cover_title="Post 1 Title",
            cover_description="Post 1 Description",
            cover_image="post_1_image.jpg",
        )

        self.comment = Comment.objects.create(
            post=self.post_1,
            author=self.user,
            content="Test Comment Content",
        )

    def test_comment_create_view_post_method_user_logged_in(self):
        """
        Test that a logged-in user can create a comment.
        """
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        comments_count_before = self.post_1.comments.count()

        response = self.client.post(
            reverse("webapp:comment_create", args=[self.post_1.id]),
            data={
                "comment_content": "Test Comment Content",
            }
        )

        comments_count_after = self.post_1.comments.count()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:post_detail", args=[self.post_1.id]))
        self.assertEqual(comments_count_after, comments_count_before + 1)


    def test_comment_delete_view_post_method_user_logged_in(self):
        """
        Test that a logged-in user can delete their own comment.
        """
        self.client.login(email=USER_EMAIL, password=USER_PASSWORD)

        response = self.client.post(
            reverse("webapp:comment_delete", args=[self.post_1.id]),
            data={"comment_id": self.comment.id},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:post_detail", args=[self.post_1.id]))
        # Check if the comment has been deleted
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=self.comment.id)


    def test_comment_delete_view_post_method_another_user_logged_in(self):
        """
        Test that another logged-in user cannot delete the comment.
        """
        self.client.login(email=ANOTHER_USER_EMAIL, password=ANOTHER_USER_PASSWORD)

        response = self.client.post(
            reverse("webapp:comment_delete", args=[self.post_1.id]),
            data={"comment_id": self.comment.id},
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())


class TestCommentViewsSuperUserLoggedIn(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD,
        )

        self.another_superuser = User.objects.create_superuser(
            email=ANOTHER_SUPERUSER_EMAIL,
            password=ANOTHER_SUPERUSER_PASSWORD,
        )

        self.post_1 = Post.objects.create(
            position=1,
            cover_title="Post 1 Title",
            cover_description="Post 1 Description",
            cover_image="post_1_image.jpg",
        )

        self.comment = Comment.objects.create(
            post=self.post_1,
            author=self.superuser,
            content="Test Comment Content",
        )

    def test_comment_create_view_post_method_superuser_logged_in(self):
        """
        Test that a superuser can create a comment.
        """
        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

        comments_count_before = self.post_1.comments.count()

        response = self.client.post(
            reverse("webapp:comment_create", args=[self.post_1.id]),
            data={
                "comment_content": "Test Comment Content",
            }
        )

        comments_count_after = self.post_1.comments.count()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:post_detail", args=[self.post_1.id]))
        self.assertEqual(comments_count_after, comments_count_before + 1)


    def test_comment_delete_view_post_method_superuser_logged_in(self):
        """
        Test that a superuser can delete the comment.
        """
        self.client.login(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

        response = self.client.post(
            reverse("webapp:comment_delete", args=[self.post_1.id]),
            data={"comment_id": self.comment.id},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:post_detail", args=[self.post_1.id]))
        # Check if the comment has been deleted
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=self.comment.id)


    def test_comment_delete_view_post_method_another_superuser_logged_in(self):
        """
        Test that another superuser can delete the comment.
        """
        self.client.login(email=ANOTHER_SUPERUSER_EMAIL, password=ANOTHER_SUPERUSER_PASSWORD)

        response = self.client.post(
            reverse("webapp:comment_delete", args=[self.post_1.id]),
            data={"comment_id": self.comment.id},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("webapp:post_detail", args=[self.post_1.id]))
        # Check if the comment has been deleted
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=self.comment.id)


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
