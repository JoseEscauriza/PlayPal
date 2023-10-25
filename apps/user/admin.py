from django.contrib import admin
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "bio", "location", "birthdate", "avatar")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "bio", "location", "birthdate", "marital_status", "preferences_id", "avatar", "gender", "marital_status")


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "bio", "location", "birthdate", "avatar", "gender")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')  # Fields to display.


    ordering = ("email",)


class CustomInterest(admin.ModelAdmin):
    list_display = [
        "interest_name",
        "get_categories",
    ]

    @admin.display(description="Categories")
    def get_categories(self, obj):
        return obj.category_id.category_name


class CustomUserPreference(admin.ModelAdmin):
    list_display = [
        "id",
        "get_parent_gender_pref",
        "get_parent_age_range",
        "get_marital_status",
        "get_child_age_range",
        "get_child_gender_pref",
        "get_childs_interests",
    ]

    @admin.display(description="Marital Status")
    def get_marital_status(self, obj):
        return ", ".join([ms.marital_status for ms in obj.marital_id.all()])

    @admin.display(description="Parent age range")
    def get_parent_age_range(self, obj):
        return f"{obj.parent_lower_age_range} - {obj.parent_upper_age_range}"

    @admin.display(description="Parent gender preference")
    def get_parent_gender_pref(self, obj):
        return ", ".join([gender.gender_name for gender in obj.parent_gender.all()])

    @admin.display(description="Child age range")
    def get_child_age_range(self, obj):
        return f"{obj.child_lower_age_range} - {obj.child_upper_age_range}"

    @admin.display(description="Child gender preference")
    def get_child_gender_pref(self, obj):
        return ", ".join([gender.gender_name for gender in obj.child_gender.all()])

    @admin.display(description="Child's interests")
    def get_childs_interests(self, obj):
        return ", ".join([obj.interest_name for obj in obj.child_interest.all()])

    # TODO: CREATE METHODS FOR MANY TO MANY FIELDS AND CONTINUE TESTING RELATIONS ONE BY ONE


# Register your models here.
admin.site.register(MaritalStatus)
admin.site.register(Gender)
admin.site.register(InterestCategory)
admin.site.register(Interest, CustomInterest)
admin.site.register(UserPreference, CustomUserPreference)
admin.site.register(CustomUser, CustomUserAdmin)