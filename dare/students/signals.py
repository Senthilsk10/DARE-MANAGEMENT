from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Student, Guide

User = get_user_model()

# ---------- STUDENT ----------
@receiver(post_save, sender=Student)
def sync_student_user(sender, instance, created, **kwargs):
    username = instance.mail
    password = str(instance.roll)

    if created:
        # Create user on student creation
        User.objects.create_user(
            username=username,
            password=password,
            role='student',
            first_name=instance.name
        )
    else:
        # Update user on student update
        try:
            user = User.objects.get(role='student', username=username)
            user.first_name = instance.name
            user.set_password(password)  # If roll number changes, update password
            user.save()
        except User.DoesNotExist:
            # In case user wasn't created before
            User.objects.create_user(
                username=username,
                password=password,
                role='student',
                first_name=instance.name
            )

@receiver(post_delete, sender=Student)
def delete_student_user(sender, instance, **kwargs):
    User.objects.filter(username=instance.mail, role='student').delete()


# ---------- GUIDE ----------
@receiver(post_save, sender=Guide)
def sync_guide_user(sender, instance, created, **kwargs):
    username = instance.email
    password = instance.phone

    if created:
        # Create user on guide creation
        User.objects.create_user(
            username=username,
            password=password,
            role='guide',
            first_name=instance.name
        )
    else:
        # Update user on guide update
        try:
            user = User.objects.get(role='guide', username=username)
            user.first_name = instance.name
            user.set_password(password)  # If phone changes, update password
            user.save()
        except User.DoesNotExist:
            # In case user wasn't created before
            User.objects.create_user(
                username=username,
                password=password,
                role='guide',
                first_name=instance.name
            )

@receiver(post_delete, sender=Guide)
def delete_guide_user(sender, instance, **kwargs):
    User.objects.filter(username=instance.email, role='guide').delete()
