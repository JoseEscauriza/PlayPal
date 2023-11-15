from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_child_first_name_childpicture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="first_name",
            field=models.CharField(default="Kiddo", max_length=30),
        ),
    ]
