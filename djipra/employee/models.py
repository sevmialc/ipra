from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, Group


class Employee(AbstractUser):
    """Пользователь"""
    job_title = models.CharField(max_length=30, blank=True, null=True, verbose_name="Должность")

    def full_name(self):
        return " ".join([self.last_name, self.first_name])

    full_name.short_description = 'ФИО'

    class Meta:
        verbose_name_plural = 'Сотрудники'
        verbose_name = 'Сотрудник'

    def __str__(self):
        return self.full_name()


class GroupProxy(Group):
    """Прокси-модель для групп пользователей"""

    class Meta:
        proxy = True
        verbose_name_plural = 'Группы'
        verbose_name = 'Группа'
