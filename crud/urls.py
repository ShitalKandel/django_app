from django.urls import path
from crud.views import ArticleViewSets,AuthorView

urlpatterns = [ 
    path('list_articles/',ArticleViewSets.as_view({'post':'create','get':'retrieve'})),
    path('author/',AuthorView.as_view())
]