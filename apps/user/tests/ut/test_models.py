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


class TestCustomUserModel(TestCase):
    def test_create_custom_user(self):
        user = CustomUser.objects.create(email="test@example.com", password="pass")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("pass"))


class TestUserPhotoModel(TestCase):
    def test_user_photo_creation(self):
        user = CustomUser.objects.create(email="user@example.com", password="pass")
        photo = UserPhoto.objects.create(user_id=user, photos="path/to/photo.jpg")
        self.assertEqual(photo.user_id, user)
        self.assertEqual(photo.photos, "path/to/photo.jpg")


class TestGradeModel(TestCase):
    def test_create_grade(self):
        user1 = CustomUser.objects.create(email="user1@example.com", password="password")
        user2 = CustomUser.objects.create(email="user2@example.com", password="password")
        grade = Grade.objects.create(grade=5)
        grade.user_id_given.add(user1)
        grade.user_id_received.add(user2)
        self.assertEqual(grade.grade, 5)
        self.assertIn(user1, grade.user_id_given.all())
        self.assertIn(user2, grade.user_id_received.all())


class TestChildModel(TestCase):
    def test_create_child(self):
        user = CustomUser.objects.create(email="parent@example.com", password="pass")
        child = Child.objects.create(parent_id=user, birthdate="2022-01-01", bio="Child bio")
        self.assertEqual(child.parent_id, user)
        self.assertEqual(child.birthdate, "2022-01-01")
        self.assertEqual(child.bio, "Child bio")
