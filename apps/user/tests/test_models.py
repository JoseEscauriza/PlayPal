import unittest
from django.test import TestCase
from apps.user.models import *
from django.db.utils import DataError
from django.contrib.auth import get_user_model

User = get_user_model()

class TestCustomUserManagerModel(TestCase):
    def test_create_user(self):
        # Test creating a regular user
        user = User.objects.create_user(email="user@example.com", password="password")
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        # Test creating a superuser
        superuser = User.objects.create_superuser(email="superuser@example.com", password="password")
        self.assertIsInstance(superuser, User)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_staff_flag(self):
        # Attempt to create a superuser without is_staff=True
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="superuser@example.com", password="password", is_staff=False)

    def test_create_superuser_without_superuser_flag(self):
        # Attempt to create a superuser without is_superuser=True
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="superuser@example.com", password="password", is_superuser=False)

        
class TestMaritalStatusModel(TestCase):
    def setUp(self) -> None:
        self.marital_status_name = "Its Complicated"
        self.marital_status = MaritalStatus(marital_status=self.marital_status_name)
        
    def test_create_marital_status_success(self):
        # check to see that the status was created successfully
        self.assertIsInstance(self.marital_status, MaritalStatus)
        
    def test_create_marital_status_failure(self):
        # Attempt to create a MaritalStatus object where marital_status field exceeds max length(max_length=30)
        with self.assertRaises(DataError):
            MaritalStatus.objects.create(marital_status="A" * 31)
            
    def test_str_method(self):
        # Testing str dunder method
        expected_str = "Its Complicated"
        actual_str = str(self.marital_status)
        self.assertEqual(expected_str, actual_str)


class TestGenderModel(TestCase):
    def setUp(self) -> None:
        self.gender = "Non-Binary"
        self.gender_name = Gender(gender_name=self.gender)
        
    def test_create_gender_success(self):
        # Check if instance was created successfully
        self.assertIsInstance(self.gender_name, Gender)
        
    def test_create_gender_failure(self):
        # Attempt to create a Gender object where gender_name field exceeds max length (max_length=10)
        with self.assertRaises(DataError):
            Gender.objects.create(gender_name="A" * 11)
            
    def test_str_method(self):
        # Testing str dunder method
        expected_str = "Non-Binary"
        actual_str = str(self.gender)
        self.assertEqual(expected_str, actual_str)
            

class TestInterestCategoryModel(TestCase):
    def setUp(self) -> None:
        self.category = "Sports"
        self.category_name = InterestCategory(category_name=self.category)
        
    def test_create_category_success(self):
        # Check if instance was created successfully
        self.assertIsInstance(self.category_name, InterestCategory)
        
    def test_create_category_failure(self):
        # Attempt to create an InterestCategory object where category_name field exceeds max length (max_length=50)
        with self.assertRaises(DataError):
            InterestCategory.objects.create(category_name="A" * 51)
            
    def test_str_method(self):
        # Testing str dunder method
        expected_str = "Sports"
        actual_str = str(self.category)
        self.assertEqual(expected_str, actual_str)


class TestInterestModel(TestCase):
    def setUp(self):
        # Create an InterestCategory for testing
        self.category = InterestCategory.objects.create(category_name="Sports")

        # Create an Interest instance
        self.interest = Interest.objects.create(category_id=self.category, interest_name="Football")

    
    def test_category_relationship(self):
        # Test the relationship with InterestCategory
        self.assertEqual(self.interest.category_id, self.category)


    def test_create_interest_failure(self):
        # Attempt to create an Interest object where interest_name field exceeds max length (max_length=50)
        with self.assertRaises(DataError):
            Interest.objects.create(interest_name="A" * 51)
            
            
    def test_str_method(self):
        # Testing str dunder method
        expected_str = "Football"
        actual_str = str(self.interest)
        self.assertEqual(expected_str, actual_str)        

        
class UserPreferenceModelTest(TestCase):
    def setUp(self):
        # Create instances of related models for testing
        self.user = CustomUser.objects.create(email="user@example.com", password="password")
        self.gender = Gender.objects.create(gender_name="Male")
        self.marital_status = MaritalStatus.objects.create(marital_status="Married")

        # Create an InterestCategory for testing
        self.category = InterestCategory.objects.create(category_name="Test Category")

        # Create an Interest instance with the related InterestCategory
        self.interest = Interest.objects.create(category_id=self.category, interest_name="Test Interest")

        # Create a UserPreference instance for testing
        self.preference = UserPreference.objects.create(
            user_id=self.user,
            parent_lower_age_range=30,
            parent_upper_age_range=40,
            child_lower_age_range=5,
            child_upper_age_range=10,
        )

        # Assign values to the ManyToManyFields using the set() method
        self.preference.parent_gender.set([self.gender])
        self.preference.marital_id.set([self.marital_status])
        self.preference.child_gender.set([self.gender])
        self.preference.child_interest.set([self.interest])


    def test_str_method(self):
        # Test the __str__ method
        expected_str = f"ID: {self.preference.id}"
        actual_str = str(self.preference)
        self.assertEqual(expected_str, actual_str)

    def test_user_relationship(self):
        # Test the relationship with CustomUser
        self.assertEqual(self.preference.user_id, self.user)

    def test_gender_relationship(self):
        # Test the relationship with Gender
        self.assertEqual(list(self.preference.parent_gender.all()), [self.gender])

    def test_marital_status_relationship(self):
        # Test the relationship with MaritalStatus
        self.assertEqual(list(self.preference.marital_id.all()), [self.marital_status])

    def test_child_interest_relationship(self):
        # Test the relationship with Interest
        self.assertEqual(list(self.preference.child_interest.all()), [self.interest])

    def test_age_ranges(self):
        # Test the age range fields
        self.assertEqual(self.preference.parent_lower_age_range, 30)
        self.assertEqual(self.preference.parent_upper_age_range, 40)
        self.assertEqual(self.preference.child_lower_age_range, 5)
        self.assertEqual(self.preference.child_upper_age_range, 10)


class TestCustomUSerModel(TestCase):
    def setUp(self) -> None:
        # Create instances of related models for testing
        self.gender = Gender.objects.create(gender_name="Male")
        self.marital_status = MaritalStatus.objects.create(marital_status="Married")

        # Create a CustomUser instance for testing
        self.user = CustomUser.objects.create(
            email="user@example.com",
            gender=self.gender,
            verified_status=True,
            bio="Test bio",
            location="Germany",
            birthdate="1990-01-01",
            marital_status=self.marital_status,
            avatar="avatars/test_avatar.jpg"
        )

    def test_str_method(self):
        # Test the __str__ method
        expected_str = "user@example.com"
        actual_str = str(self.user)
        self.assertEqual(expected_str, actual_str)

    def test_email_field(self):
        # Test the email field
        self.assertEqual(self.user.email, "user@example.com")

    def test_gender_field(self):
        # Test the gender field
        self.assertEqual(self.user.gender, self.gender)

    def test_verified_status_field(self):
        # Test the verified_status field
        self.assertTrue(self.user.verified_status)

    def test_bio_field(self):
        # Test the bio field
        self.assertEqual(self.user.bio, "Test bio")

    def test_location_field(self):
        # Test the location field
        self.assertEqual(self.user.location, "Germany")

    def test_birthdate_field(self):
        # Test the birthdate field
        self.assertEqual(str(self.user.birthdate), "1990-01-01")

    def test_marital_status_field(self):
        # Test the marital_status field
        self.assertEqual(self.user.marital_status, self.marital_status)

    def test_avatar_field(self):
        # Test the avatar field
        self.assertEqual(self.user.avatar, "avatars/test_avatar.jpg")

    def test_has_perm_method(self):
        # Test the has_perm method (it's currently set to always return True)
        self.assertTrue(self.user.has_perm("some_permission"))
    
    
class TestUserPhotoModel(TestCase):
    def setUp(self) -> None:
        # Create a CustomUser instance for testing
        self.user = CustomUser.objects.create(email="user@example.com", password="password")

        # Create a UserPhoto instance for testing
        self.user_photo = UserPhoto.objects.create(
            user_id=self.user,
            photos="user_photos/test_photo.jpg"
        )

    def test_user_relationship(self):
        # Test the relationship with CustomUser
        self.assertEqual(self.user_photo.user_id, self.user)

    def test_photos_field(self):
        # Test the photos field
        self.assertEqual(self.user_photo.photos, "user_photos/test_photo.jpg")

    def test_id_field(self):
        # Test the id field (UUID)
        self.assertIsNotNone(self.user_photo.id)

    def test_id_is_uuid(self):
        # Test that the id field is a valid UUID
        self.assertTrue(self.user_photo.id.__class__ is uuid.UUID)

    def test_id_is_unique(self):
        # Test that the id field is unique among UserPhoto instances
        user_photo_2 = UserPhoto.objects.create(
            user_id=self.user,
            photos="user_photos/another_photo.jpg"
        )
        self.assertNotEqual(self.user_photo.id, user_photo_2.id)


class TestGradeModel(TestCase):
    def setUp(self):
        # Create instances of CustomUser for testing
        self.user_given = CustomUser.objects.create(email="user_given@example.com", password="password1")
        self.user_received = CustomUser.objects.create(email="user_received@example.com", password="password2")

        # Create a Grade instance for testing
        self.grade = Grade.objects.create(
            grade=5
        )

        # Assign CustomUser instances to user_id_given and user_id_received using the set() method
        self.grade.user_id_given.set([self.user_given])
        self.grade.user_id_received.set([self.user_received])

    def test_user_id_given_relationship(self):
        # Test the relationship with CustomUser for user_id_given
        users_given = list(self.grade.user_id_given.all())
        self.assertEqual(users_given, [self.user_given])

    def test_user_id_received_relationship(self):
        # Test the relationship with CustomUser for user_id_received
        users_received = list(self.grade.user_id_received.all())
        self.assertEqual(users_received, [self.user_received])

    def test_grade_field(self):
        # Test the grade field
        self.assertEqual(self.grade.grade, 5)

    def test_id_field(self):
        # Test the id field (UUID)
        self.assertIsNotNone(self.grade.id)

    def test_id_is_uuid(self):
        # Test that the id field is a valid UUID
        self.assertTrue(self.grade.id.__class__ is uuid.UUID)
        
        
class TestChildModel(TestCase):
    def setUp(self):
        # Create instances of related models for testing
        self.parent = CustomUser.objects.create(email="parent@example.com", password="password")
        self.gender = Gender.objects.create(gender_name="Male")       
        self.interest_category = InterestCategory.objects.create(category_name="Test Category")
        # Create an Interest instance related to the InterestCategory
        self.interest = Interest.objects.create(category_id=self.interest_category, interest_name="Test Interest")

        # Create a Child instance for testing
        self.child = Child.objects.create(
            parent_id=self.parent,
            birthdate="2020-01-01",
            gender_id=self.gender,
            bio="Test child bio",
            avatar="avatars/test_avatar.jpg"
        )

        # Assign an Interest instance to interest_id using the set() method
        self.child.interest_id.set([self.interest])

    def test_parent_id_relationship(self):
        # Test the relationship with CustomUser for parent_id
        self.assertEqual(self.child.parent_id, self.parent)

    def test_birthdate_field(self):
        # Test the birthdate field
        self.assertEqual(str(self.child.birthdate), "2020-01-01")

    def test_gender_id_relationship(self):
        # Test the relationship with Gender for gender_id
        self.assertEqual(self.child.gender_id, self.gender)

    def test_bio_field(self):
        # Test the bio field
        self.assertEqual(self.child.bio, "Test child bio")

    def test_avatar_field(self):
        # Test the avatar field
        self.assertEqual(self.child.avatar, "avatars/test_avatar.jpg")

    def test_interest_id_relationship(self):
        # Test the relationship with Interest for interest_id
        interests = list(self.child.interest_id.all())
        self.assertEqual(interests, [self.interest])

    def test_id_field(self):
        # Test the id field (UUID)
        self.assertIsNotNone(self.child.id)

    def test_id_is_uuid(self):
        # Test that the id field is a valid UUID
        self.assertTrue(self.child.id.__class__ is uuid.UUID)

    def test_verbose_name_plural(self):
        # Test the verbose name in the model's Meta class
        self.assertEqual(Child._meta.verbose_name_plural, "Children")  
        
        
        
        
if __name__ == "__main__":
    unittest.main()