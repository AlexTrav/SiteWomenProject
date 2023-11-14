from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse

from transliterate import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг',
                            validators=[
                               MinLengthValidator(5, message='Минимум 5 символов'),
                               MaxLengthValidator(100, message='Максимум 100 символов')
                            ])
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=Status.DRAFT, choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), verbose_name='Статус')

    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фото')

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='husband', verbose_name='Муж')

    objects = models
    published = PublishedManager()

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'

        ordering = ['time_create']
        indexes = [
            models.Index(fields=['time_create'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.title))
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Катиегории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name='Тэг поста')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')

    objects = models.Manager()

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя мужа')
    age = models.IntegerField(null=True, verbose_name='Возраст мужа')
    m_count = models.IntegerField(blank=True, default=0, verbose_name='Количество женидьб')

    objects = models.Manager()

    def __str__(self):
        return self.name


# class UploadFiles(models.Model):
#     """Модель загрузки файла"""
#     file = models.FileField(upload_to='uploads_model')


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Почта')
    message = models.TextField(verbose_name='Сообщение')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Сообщения пользователей'
        verbose_name_plural = 'Сообщений пользователей'

    def __str__(self):
        return f"{self.name} - {self.email}"
