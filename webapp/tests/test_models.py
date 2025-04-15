from django.db.models import Max
from django.test import TestCase

from users.models import User
from webapp.models import Post, Image, Tag, Text, Space, ContentType, Block, Comment


USER_EMAIL = "test_user@test.com"
USER_PASSWORD = "test_dffhsf232iife87"

SUPERUSER_EMAIL = "test_superuser@test.com"
SUPERUSER_PASSWORD = "test_sdff3987r3uifss"


class TestModels(TestCase):

    def setUp(self):
        """Create reusable objects for testing."""
        self.post = Post.objects.create(
            position=1,
            cover_title="Test Title",
            cover_description="Test Description",
            cover_image="test_image.jpg",
        )
        self.image = Image.objects.create(
            image="test_image.jpg",
            image_size=75,
            image_alignment="center",
            post=self.post,
        )
        self.text = Text.objects.create(
            text="Test Text",
            text_type="normal",
            text_alignment="center",
        )
        self.space = Space.objects.create(space_number=1)

    def test_create_post(self):
        """Test creating a Post instance."""
        self.assertEqual(self.post.position, 1)
        self.assertEqual(self.post.cover_title, "Test Title")
        self.assertEqual(self.post.cover_description, "Test Description")
        self.assertEqual(self.post.cover_image, "test_image.jpg")
        self.assertIsInstance(self.post, Post)

    def test_post_str(self):
        """Test the string representation of Post."""
        expected_str = (
            f"Title: {self.post.cover_title} | Position: {self.post.position}"
        )
        self.assertEqual(str(self.post), expected_str)

    def test_create_tag(self):
        """Test creating a Tag instance."""
        tag = Tag.objects.create(tag_name="Test Tag", post=self.post)
        self.assertEqual(tag.tag_name, "Test Tag")
        self.assertEqual(tag.post, self.post)
        self.assertIsInstance(tag, Tag)

    def test_tag_str(self):
        """Test the string representation of Tag."""
        tag = Tag.objects.create(tag_name="Test Tag", post=self.post)
        expected_str = tag.tag_name
        self.assertEqual(str(tag), expected_str)

    def test_create_image(self):
        """Test creating an Image instance linked to a Post."""
        image = Image.objects.create(
            image="test_image.jpg",
            image_size=75,
            image_alignment="center",
            post=self.post,
        )

        self.assertEqual(image.image, "test_image.jpg")
        self.assertEqual(image.image_size, 75)
        self.assertEqual(image.image_alignment, "center")
        self.assertEqual(image.post, self.post)
        self.assertIsInstance(image, Image)

    def test_image_str(self):
        """Test the string representation of Image."""
        image = Image.objects.create(
            image="test_image.jpg",
            image_size=75,
            image_alignment="center",
            post=self.post,
        )
        expected_str = (
            f"Image: {image.image} | Size: {image.image_size} "
            f"| Alignment: {image.image_alignment}"
        )
        self.assertEqual(str(image), expected_str)

    def test_create_text(self):
        """Test creating a Text instance linked to a Post."""
        text = Text.objects.create(
            text="Test Text",
            text_type="normal",
            text_alignment="center",
        )
        self.assertEqual(text.text, "Test Text")
        self.assertEqual(text.text_type, "normal")
        self.assertEqual(text.text_alignment, "center")
        self.assertIsInstance(text, Text)

    def test_text_str(self):
        """Test the string representation of Text."""
        text = Text.objects.create(
            text="Test Text",
            text_type="normal",
            text_alignment="center",
        )
        expected_str = text.text
        self.assertEqual(str(text), expected_str)

    def test_create_space(self):
        """Test creating a Space instance linked to a Post."""
        space = Space.objects.create(space_number=1)
        self.assertEqual(space.space_number, 1)
        self.assertIsInstance(space, Space)

    def test_space_str(self):
        """Test the string representation of Space."""
        space = Space.objects.create(space_number=1)
        expected_str = f"Space Number: {space.space_number}"
        self.assertEqual(str(space), expected_str)

    def test_post_content(self):
        """Test creating PostContent instances for different content types."""

        for content in [self.image, self.text, self.space]:
            object_type = ContentType.objects.get_for_model(content)
            max_position = Block.objects.filter(post=self.post).aggregate(
                Max("block_position")
            )
            position = (
                max_position["block_position__max"] + 1
                if max_position["block_position__max"]
                else 1
            )
            Block.objects.create(
                post=self.post,
                object_type=object_type,
                object_id=content.id,
                block_position=position,
            )

        # Check if PostContent instances are created correctly
        post_contents = Block.objects.filter(post=self.post)
        self.assertEqual(post_contents.count(), 3)
        self.assertEqual(post_contents[0].content_object, self.image)
        self.assertEqual(post_contents[1].content_object, self.text)
        self.assertEqual(post_contents[2].content_object, self.space)

    def test_comment_creation(self):
        """Test creating a comment instance."""
        user = User.objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )

        comment = Comment.objects.create(
            post=self.post,
            author=user,
            content="Test Content",
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, user)
        self.assertEqual(comment.content, "Test Content")
        self.assertIsInstance(comment, Comment)

    def test_comment_str(self):
        """Test the string representation of Comment."""

        user = User.objects.create_user(
            email=USER_EMAIL,
            password=USER_PASSWORD,
        )

        comment = Comment.objects.create(
            post=self.post,
            author=user,
            content="Test Content",
        )
        expected_str = f"{USER_EMAIL}: Test Content"
        self.assertEqual(str(comment), expected_str)
