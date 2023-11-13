from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound  # , Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
# from django.urls import reverse
# from django.template.loader import render_to_string
from django.urls import reverse_lazy
# from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView

from .forms import *

from .models import *

# import uuid


menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]


# def index(request):
#     # t = render_to_string('women/index.html')
#     # return HttpResponse('<h1>Главная страница</h1>')
#     # return HttpResponse(t)
#     # posts = Women.objects.filter(is_published=1)
#
#     posts = Women.published.all().select_related('cat')
#     context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


# class WomenHome(TemplateView):
#     template_name = 'women/index.html'
#     posts = Women.published.all().select_related('cat')
#     extra_context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Главная страница'
#         context['menu'] = menu
#         context['posts'] = Women.published.all().select_related('cat')
#         context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
#         return context


class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related('cat')


# def handle_uploaded_file(f):
#     """
#     Функция обработки загруженного файла.
#
#     :param f: Файл.
#     """
#     # Генерируем уникальное имя файла
#     unique_filename = str(uuid.uuid4())
#     with open(f'uploads/{unique_filename}_{f.name}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    # if request.method == 'POST':
    #     # handle_uploaded_file(request.FILES['file_upload'])
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # Если без модели
    #         # handle_uploaded_file(form.cleaned_data['file'])
    #         # handle_uploaded_file(form.cleaned_data['photo'])
    #
    #         # Если с моделью
    #         fp = UploadFiles(file=form.cleaned_data['file'])
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    context = {
        'title': 'О сайте',
        'menu': menu,
        # 'form': form,
    }
    return render(request, 'women/about.html', context=context)


def categories(request, category_id):
    return HttpResponse(f'<h1>Категория | id:{category_id}</h1>')


def categories_by_slug(request, category_slug):
    return HttpResponse(f'<h1>Категория | slug: {category_slug}</h1>')


def archive(request, year):
    if year > 2023:
        # raise Http404()

        # return redirect('home')

        # return redirect('categories_by_slug', 'music')

        uri = reverse('categories_by_slug', args=('music', ))
        return redirect(uri)

        # return HttpResponseRedirect(uri)  # С кодом 302
        # return HttpResponsePermanentRedirect(uri)  # С кодом 301

    return HttpResponse(f'<h1>Архив по годам | год: {year}</h1>')


# Обработчик исключений запросов
def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Страница не найдена</h1>')


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'women/post.html', context=context)


class ShowPost(DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['cat_selected'] = context['post'].cat.pk
        context['menu'] = menu
        return context


# def addpage(request):
#     """Функция представления для отображения страницы добавления поста."""
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except Exception as e:
#             #     form.add_error(None, f'Ошибка добавления поста: {e}')
#
#             # Метод save только у класса формы связанной с моделью -> Сохраняет переданные данные в таблицу (модель)
#             form.save()
#             # Перенаправление
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     context = {
#         'title': 'Добавление статьи',
#         'menu': menu,
#         'form': form,
#     }
#     return render(request, 'women/addpage.html', context=context)


# class AddPage(View):
#     """Класс представления для отображения страницы добавления поста. Наследованный от View."""
#
#     @staticmethod
#     def get(request):
#         form = AddPostForm()
#         context = {
#             'title': 'Добавление статьи',
#             'menu': menu,
#             'form': form,
#         }
#         return render(request, 'women/addpage.html', context=context)
#
#     @staticmethod
#     def post(request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Метод save только у класса формы связанной с моделью -> Сохраняет переданные данные в таблицу (модель)
#             form.save()
#             return redirect('home')
#         context = {
#             'title': 'Добавление статьи',
#             'menu': menu,            'form': form,
#         }
#         return render(request, 'women/addpage.html', context=context)


class AddPage(FormView):
    """Класс представления для отображения страницы добавления поста. Наследованный от FormView."""
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Добавление статьи', 'menu': menu}

    def form_valid(self, form):
        form.save()
        print(type(form.cleaned_data))
        return super().form_valid(form)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#     context = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', context=context)


class WomenCategory(ListView):
    model = Category
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = f'Категория - {cat.name}'
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#     context = {
#         'title': f'Тэг: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#     return render(request, 'women/index.html', context=context)


class WomenTags(ListView):
    model = TagPost
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        context['title'] = f'Тэг - {tag.tag}'
        context['menu'] = menu
        context['cat_selected'] = None
        return context
