# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, \
    JsonResponse  # , Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
# from django.urls import reverse
# from django.template.loader import render_to_string
from django.urls import reverse_lazy
# from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import *

from .models import *

# import uuid
from .utils import DataMixin, PaginatorFromWomen, CustomPermissionRequiredMixin

# <!-- Кэширование на уровне API -->
# from django.core.cache import cache


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    paginator_class = PaginatorFromWomen

    def get_queryset(self):
        # <!-- Кэширование на уровне API -->
        # w_lst = cache.get('women_posts')
        # if not w_lst:
        #     w_lst = Women.published.all().select_related('cat')
        #     cache.set('women_posts', w_lst, 20)
        return Women.published.all().select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        paginator = self.paginator_class(self.get_queryset(), self.paginate_by)
        paginator.page(page)
        return self.get_mixin_context(context)


class WomenAbout(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = None
        return self.get_mixin_context(context, title='О нас')


# Обработчик исключений запросов
def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)


class AddPage(CustomPermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    """Класс представления для отображения страницы добавления поста. Наследованный от CreateView."""
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'
    extra_context = {'cat_selected': None}
    # login_url = '/admin/'
    permission_required = 'women.add_women'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    """Класс представления для отображения страницы редактирования поста. Наследованный от CreateView."""
    model = Women
    fields = '__all__'
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'women.change_women'


class DeletePage(DataMixin, DeleteView):
    model = Women
    template_name = 'women/delete_page.html'
    success_url = reverse_lazy('home')
    context_object_name = 'post'

    # def get_object(self, queryset=None):
    #     return Women.objects.get(slug=self.kwargs['slug'])

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return self.get_mixin_context(context, title='Удаление статьи')


class ContactFormView(DataMixin, FormView):
    template_name = 'women/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = None
        return self.get_mixin_context(context, title='Контакты')


# class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
#     form_class = ContactForm
#     template_name = 'women/contact.html'
#     success_url = reverse_lazy('home')
#     title_page = 'Обратная связь'
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['cat_selected'] = None
#         return self.get_mixin_context(context, title='Контакты')


class WomenCategory(DataMixin, ListView):
    model = Category
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = True
    paginator_class = PaginatorFromWomen

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        page = self.request.GET.get('page', 1)
        paginator = self.paginator_class(self.get_queryset(), self.paginate_by)
        paginator.page(page)

        return self.get_mixin_context(context, title=f'Категория - {cat.name}', cat_selected=cat.pk)


class WomenTags(DataMixin, ListView):
    model = TagPost
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Тэг - {tag.tag}', cat_selected=None)
