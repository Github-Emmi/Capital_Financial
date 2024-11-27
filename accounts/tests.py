from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from accounts.models import User
from venexapp.models import AdminUser, Clients


class UserModelTest(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User",
            user_type=1,  # Admin
        )

        # Create a client user
        self.client_user = User.objects.create_user(
            email="client@example.com",
            password="clientpassword",
            first_name="Client",
            last_name="User",
            user_type=2,  # Client
        )

    def test_user_creation(self):
        """Test that users are created correctly."""
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(self.admin_user.email, "admin@example.com")
        self.assertEqual(self.client_user.email, "client@example.com")

    def test_admin_user_creation(self):
        """Test that AdminUser profile is created correctly."""
        admin_profile = AdminUser.objects.get(admin=self.admin_user)
        self.assertEqual(admin_profile.admin, self.admin_user)
        self.assertEqual(admin_profile.address, "")  # Default value

    def test_client_user_creation(self):
        """Test that Client profile is created correctly."""
        client_profile = Clients.objects.get(admin=self.client_user)
        self.assertEqual(client_profile.admin, self.client_user)
        self.assertEqual(client_profile.address, "")  # Default value

    def test_signal_creates_profiles(self):
        """Test that signals create AdminUser and Clients profiles automatically."""
        self.assertTrue(AdminUser.objects.filter(admin=self.admin_user).exists())
        self.assertTrue(Clients.objects.filter(admin=self.client_user).exists())

    def test_user_roles(self):
        """Test user roles and type-specific behavior."""
        self.assertEqual(self.admin_user.user_type, 1)
        self.assertEqual(self.client_user.user_type, 2)

    def test_user_password_check(self):
        """Test password hashing and authentication."""
        self.assertTrue(self.admin_user.check_password("adminpassword"))
        self.assertTrue(self.client_user.check_password("clientpassword"))

    def test_full_name(self):
        """Test full name generation."""
        self.assertEqual(self.admin_user.get_full_name(), "Admin User")
        self.assertEqual(self.client_user.get_full_name(), "Client User")

    def test_short_name(self):
        """Test short name generation."""
        self.assertEqual(self.admin_user.get_short_name(), "A U")
        self.assertEqual(self.client_user.get_short_name(), "C U")

    def test_formatted_balance(self):
        """Test formatted balance output."""
        self.admin_user.bal = 12345.67
        self.admin_user.save()
        self.assertEqual(self.admin_user.formatted_balance, "12,345.67")
