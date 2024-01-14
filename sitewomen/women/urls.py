from django.urls import path, register_converter
from . import views, converters
from django.views.decorators.cache import cache_page


register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    # path('', cache_page(20)(views.WomenHome.as_view()), name='home'),  # -> Для кэширования отдельного представления
    path('about/', views.WomenAbout.as_view(), name='about'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    # path('contact/', views.WomenContact.as_view(), name='contact'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    # path('login/', views.login, name='login'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.WomenTags.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', views.DeletePage.as_view(), name='delete_page'),
]

