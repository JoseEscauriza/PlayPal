from django.test import TestCase
from apps.user.models import *


class TestCustomUserModel(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(email="user@example.com", password="pass")
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("pass"))

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(email="admin@example.com", password="pass")
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class TestMaritalStatusModel(TestCase):
    def test_marital_status_str(self):
        marital_status = MaritalStatus.objects.create(marital_status="Single")
        self.assertEqual(str(marital_status), "Single")


class TestGenderModel(TestCase):
    def test_gender_str(self):
        gender = Gender.objects.create(gender_name="Male")
        self.assertEqual(str(gender), "Male")


class TestInterestCategoryModel(TestCase):
    def test_interest_category_creation(self):
        category = InterestCategory.objects.create(category_name="hobbies")
        self.assertEqual(category.category_name, "hobbies")

    def test_interest_category_str(self):
        category = InterestCategory.objects.create(category_name="hobbies")
        self.assertEqual(str(category), "hobbies")


class TestInterestModel(TestCase):
    def test_interest_creation(self):
        category = InterestCategory.objects.create(category_name="hobbies")
        interest = Interest.objects.create(category_id=category, interest_name="photography")
        self.assertEqual(interest.interest_name, "photography")

    def test_interest_str(self):
        category = InterestCategory.objects.create(category_name="hobbies")
        interest = Interest.objects.create(category_id=category, interest_name="photography")
        self.assertEqual(str(interest), "photography")


