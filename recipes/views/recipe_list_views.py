
import os

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         JsonResponse)
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView

from recipes.models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = ''

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        qs = qs.select_related('author', 'category', 'author__profile')
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('recipes'), PER_PAGE
        )
        html_language = translation.get_language()
        ctx.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'html_language': html_language,
        })
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeAPI(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        self.get_context_data()['recipes']
        recipes_dict = self.get_context_data()['recipes'].object_list.values()
        return JsonResponse(
            list(recipes_dict),
            safe=False,
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        category_translation = _('Category')
        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - '
                     f'{category_translation}',
        })
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True,
        ).order_by('-id')
        return qs

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        if not search_term:
            raise Http404()
        ctx = super().get_context_data(*args, **kwargs)
        search_translation = _('Search for')
        ctx.update({
            'page_title': f'{search_translation} "{search_term}"',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })
        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })
        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        if not qs:
            raise Http404
        return qs


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''
        del recipe_dict['is_published']
        del recipe_dict['prep_steps_is_html']
        return JsonResponse(
            recipe_dict,
            safe=False,
        )


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()
        if not page_title:
            page_title = _('No recipes found')
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'page_title': f'"{page_title}"',
        })
        return ctx


def media(request, file_path=None):
    from django.conf import settings as cfg
    media_root = getattr(cfg, 'MEDIA_ROOT', None)

    if not media_root:
        return HttpResponseBadRequest('Invalid Media Root Configuration')
    if not file_path:
        return HttpResponseBadRequest('Invalid File Path')

    with open(os.path.join(media_root, file_path), 'rb') as doc:
        response = HttpResponse(doc.read(), content_type='application/doc')
        response['Content-Disposition'] = 'filename=%s' % (
            file_path.split('/')[-1])
        return response
