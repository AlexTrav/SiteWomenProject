from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
]


class DataMixin:
    title_page = None
    cat_selected = None
    extra_context = {}
    paginate_by = 5

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    # На будущее, если много параметров, чтобы не делать много if-ов.
    # def __init__(self) -> None:
    #     for k in dir(self)[::-1]:
    #         if k.startswith('__'):
    #             break
    #         if (v := getattr(self, k)) is not None and k != 'extra_context':
    #             self.extra_context[k] = v

    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context


class PaginatorFromWomen(Paginator):

    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                return self.num_pages
            elif int(number) < 1:
                return 1
            else:
                raise
