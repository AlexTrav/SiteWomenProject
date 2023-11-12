from django.urls import path, register_converter
from women import views, converters


register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.WomenHome.as_view(), name='home'),

    path('about/', views.about, name='about'),

    path('categories/<int:category_id>/', views.categories, name='categories'),
    path('categories/<slug:category_slug>/', views.categories_by_slug, name='categories_by_slug'),
    path('archive/<year4:year>/', views.archive, name='archive'),

    # path('post/<int:post_id>', views.show_post, name='post'),
    # path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),

    # path('addpage/', views.addpage, name='add_page'),

    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),

    # path('category/<int:cat_id>/', views.show_category, name='category'),

    # path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),

    # path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('tag/<slug:tag_slug>/', views.WomenTags.as_view(), name='tag'),
]

