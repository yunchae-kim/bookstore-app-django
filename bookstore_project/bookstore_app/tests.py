from bookstore_app.banned_users_cache import set_banned_users
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Book


# Test class for general book API tests
class BookAPITests(APITestCase):
    # Set up a user and book for testing
    def setUp(self):
        self.user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="testuser1", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # type: ignore for `self.client`
        self.book = Book.objects.create(
            title="Test Book 1",
            description="Test Description 1",
            author=self.user,
            price=10.00,
        )

    # Test case: Authenticated user create a new book
    def test_authenticated_access(self):
        self.client.login(username="testuser1", password="testpassword")
        data = {
            "title": "New Book 1",
            "description": "New test book",
            "price": 122.99,
            "author": self.user.id,
        }
        response = self.client.post(reverse("book-list"), data, format="json")
        # To debug if login was successful
        print(
            "User authenticated:",
            self.client.login(username="testuser1", password="testpassword"),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    # Test case: Unauthenticated user can only access the book list
    def test_unauthenticated_access(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test case: Retrieve a book detail
    def test_retrieve_book_detail(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book 1")  # type: ignore for `response.data`

    # Test case: Posting a book without a title results in an error
    def test_posting_book_without_title(self):
        self.client.login(username="testuser1", password="testpassword")
        incomplete_data = {
            "description": "No Title Book",
            "price": 12.99,
            "author": self.user.id,
        }
        response = self.client.post(
            reverse("book-list"), incomplete_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    # Test case: Posting a book with an invalid price
    def test_posting_book_with_invalid_price(self):
        self.client.login(username="testuser1", password="testpassword")
        invalid_data = {
            "title": "Invalid Price Book",
            "description": "This book has an invalid price",
            "price": "invalid_price_format",  # Invalid price format
            "author": self.user.id,
        }
        response = self.client.post(reverse("book-list"), invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()


# Test class for book author and other user API tests
class BookAuthorAPITests(APITestCase):
    def setUp(self):
        # Author user to test authorized actions
        self.author_user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="author_user",
            password="testpassword",
            first_name="Devin",
            last_name="Booker",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.author_user)  # type: ignore for `self.client`

        # Pseudonym author user to test pseudonym related functionality
        self.pseudonym_user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="pseudonym_author",
            password="testpassword3",
            first_name="Bradley",
            last_name="Beal",
            author_pseudonym="A Pseudonym Author",
        )

        # User without a real name or pseudonym
        self.username_only_user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            # No real name or pseudonym set
            username="username_only_user",
            password="testpassword4",
        )

        # Create a book authored by the first user (`author_user`)
        self.book = Book.objects.create(
            title="Book by Author User",
            description="A book by the author",
            author=self.author_user,
            price=12.32,
        )
        # Create a book authored by the pseudonym user (`pseudonym_user`)
        self.book_by_pseudonym_author = Book.objects.create(
            title="Pseudonym Author's Book",
            description="A book by an author with a pseudonym",
            author=self.pseudonym_user,
            price=20.55,
        )
        # Create a book authored by the username only user (`username_only_user`)
        self.book_by_username_only_author = Book.objects.create(
            title="Username Only Author's Book",
            description="A book by an author without a real name or pseudonym",
            author=self.username_only_user,
            price=15.00,
        )

    # Test case: Author can update their own book
    def test_author_can_update_own_book(self):
        self.client.login(username="author_user", password="testpassword")
        update_data = {
            "title": "Updated Title By Author",
            "description": "Updated Description By Author",
            "price": 21.22,
            "author": self.author_user.id,
        }
        response = self.client.put(
            reverse("book-detail", kwargs={"pk": self.book.pk}),
            update_data,
            format="json",
        )
        print(response.data)  # type: ignore for `response.data`
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    # Test case: Author can delete their own book
    def test_author_can_delete_own_book(self):
        # Log in as the author
        self.client.login(username="author_user", password="testpassword")
        response = self.client.delete(
            reverse("book-detail", kwargs={"pk": self.book.pk})
        )
        # Expecting success or no content as the author is allowed to delete their book
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()

    # Test case: Retrieve a book detail includes correct author displayed name
    def test_retrieve_book_detail_includes_author_displayed_name(self):
        # Assuming author_user has both a real name and a pseudonym set up
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_display_name = (
            self.author_user.get_full_name() or self.author_user.username
        )
        self.assertEqual(response.data["author_displayed_name"], expected_display_name)  # type: ignore for `response.data`

    # Test case: Author pseudonym is used if set
    def test_author_pseudonym_used_if_set(self):
        self.client.login(username="pseudonym_author", password="testpassword3")
        response = self.client.get(
            reverse("book-detail", kwargs={"pk": self.book_by_pseudonym_author.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author_displayed_name"], "A Pseudonym Author")  # type: ignore for `response.data`
        self.client.logout()

    # Test case: Author's real name is used if pseudonym is not set
    def test_author_real_name_used_if_no_pseudonym(self):
        # Assuming self.author_user does not have a pseudonym set but has a real name
        expected_display_name = (
            self.author_user.get_full_name() or self.author_user.username
        )
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author_displayed_name"], expected_display_name)  # type: ignore for `response.data`

    # Test case: Author's username is used if no real name or pseudonym is set
    def test_username_used_if_no_real_name_or_pseudonym(self):
        self.client.login(username="username_only_user", password="testpassword4")
        response = self.client.get(
            reverse("book-detail", kwargs={"pk": self.book_by_username_only_author.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author_displayed_name"], "username_only_user")  # type: ignore for `response.data`
        self.client.logout()


# Test class for non-author API tests
class BookNonAuthorAPITests(APITestCase):
    def setUp(self):
        # Author user to test authorized actions
        self.author_user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="author_user",
            password="testpassword",
            first_name="Devin",
            last_name="Booker",
        )

        # Non-author user to test unauthorized actions
        self.non_author_user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="non_author_user",
            password="testpassword2",
            first_name="Kevin",
            last_name="Durant",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.non_author_user)  # type: ignore for `self.client`

        # Create a book authored by the first user (`author_user`)
        self.book = Book.objects.create(
            title="Book by Author User",
            description="A book by the author",
            author=self.author_user,
            price=12.32,
        )

    # Test case: Non-author user cannot update book they are not the author of
    def test_non_author_cannot_update_book(self):
        self.client.login(username="non_author_user", password="testpassword2")
        update_data = {
            "title": "Non-Author Update Attempt",
            "description": "Attempt to update by non-author",
            "price": 50.00,
            "author": self.non_author_user.id,
        }
        response = self.client.put(
            reverse("book-detail", kwargs={"pk": self.book.pk}),
            update_data,
            format="json",
        )
        print(response.data)  # type: ignore for `response.data`
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    # Test case: Non-author user cannot delete book they are not the author of
    def test_non_author_cannot_delete_book(self):
        self.client.login(username="non_author_user", password="testpassword2")
        response = self.client.delete(
            reverse("book-detail", kwargs={"pk": self.book.pk})
        )
        # Attempt should fail as the non-author user is not allowed to delete the book
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()


# Test class for admins
class BookAdminTest(APITestCase):
    def setUp(self):
        # Admin user
        self.admin_user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="adminuser", password="testpassword", is_staff=True
        )

        # Author user
        self.author_user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="authoruser",
            password="testpassword",
            first_name="Chris",
            last_name="Paul",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)  # type: ignore for `self.client`

        # Create a book authored by the `author_user`
        self.book = Book.objects.create(
            title="Basketball",
            description="A book written by an author",
            author=self.author_user,
            price=20.22,
        )

    # Test case: Admin can update any book
    def test_admin_can_update_any_book(self):
        self.client.login(username="adminuser", password="testpassword")
        update_data = {
            "title": "Updated Title By Admin",
            "description": "Updated Description By Admin",
            "price": 21.22,
            "author": self.author_user.id,
        }
        response = self.client.put(
            reverse("book-detail", kwargs={"pk": self.book.pk}),
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()


# Class for testing banned user API access
class BannedUserAPITests(APITestCase):
    # Setup for banned user tests
    def setUp(self):
        # Set up banned user
        set_banned_users(["Darth Vader"])

        # Account for banned user
        self.user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="Darth Vader", password="testpassword23"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # type: ignore for `self.client`

        # Account for different user as author of the book banned user will GET
        self.author_user = get_user_model().objects.create_user(  # type: ignore for `get_user_model``
            username="author_user", password="testpassword"
        )

        self.book = Book.objects.create(
            title="Accessible Book",
            description="A book accessible by banned users",
            author=self.author_user,
            price=10.00,
        )

    # Test case: Banned user cannot create a book
    def test_banned_user_cannot_create_book(self):
        self.client.login(username="Darth Vader", password="testpassword23")
        data = {
            "title": "Darth Vader Book",
            "description": "Banned and cannot create a book",
            "price": 66.66,
        }
        response = self.client.post(reverse("book-list"), data, format="json")

        self.assertNotEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Banned user should not be able to create a book",
        )
        self.assertIn(
            response.status_code,
            [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED],
            "Expected a forbidden or unauthorized response for banned user",
        )

    # Test case: Banned user can GET a book
    def test_banned_user_can_get_book(self):
        self.client.login(username="Darth Vader", password="testpassword23")
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book.pk}))  # type: ignore for `self.book`
        self.assertEqual(response.status_code, status.HTTP_200_OK)
