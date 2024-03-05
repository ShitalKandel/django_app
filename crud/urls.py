from django.urls import path
from crud.views import ArticleViewSets,AuthorView,StudentDetailView 


urlpatterns = [ 
    path('list_articles/',ArticleViewSets.as_view({'post':'create'})),
    path('author/',AuthorView.as_view()),
    path('stuinfo/',StudentDetailView)
]