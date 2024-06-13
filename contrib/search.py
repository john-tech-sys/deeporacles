from ast import Add
from contrib.models import SearchTerm
from home.models import Post
from django.db.models import Q
from . import stats
import django

from profiles.models import Profile

STRIP_WORDS = ['a','an','and','by','for','from','in','no','not',
 'of','on','or','that','the','to','with', 'is', 'at']
# store the search text in the database
def store(request, q):
    # if search term is at least three chars long, store in db
    if len(q) > 2:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.tracking_id = stats.tracking_id(request)
        term.user = None
        if request.user.is_authenticated:
            term.user = request.user
        term.save()


# strip out common words, limit to 5 words
def _prepare_words(search_text):
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]


# get products matching the search text
def all_models(search_text):
    words = _prepare_words(search_text)
    search_models = [Post, Profile] # Add your models here, in any way you find best.
    search_results = []
    for model in search_models:
        fields = [x for x in model._meta.fields if isinstance(x, django.db.models.CharField)]
        search_queries = (Q(**{x.name + "__contains" : search_query}) for x in fields |
        Q(**{x.description + "__contains" : search_query}) for x in fields |
        Q(**{x.location + "__contains" : search_query}) for x in fields |
        Q(**{x.content + "__contains" : search_query}) for x in fields)
        q_object = Q()
        for query in search_queries:
            q_object = q_object | query

        results = model.objects.filter(q_object)
        all_results.append(results)
    return all_results
