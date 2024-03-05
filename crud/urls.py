from django.urls import path
from crud.views import ArticleViewSets,AuthorView,StudentDetailView 


urlpatterns = [ 
<<<<<<< HEAD
    path('list_articles/',ArticleViewSets.as_view({'post':'create'})),
    path('author/',AuthorView.as_view()),
    path('stuinfo/',StudentDetailView)
=======
    path('list_articles/',ArticleViewSets.as_view({'post':'create','get':'retrieve'})),
    path('author/',AuthorView.as_view())
>>>>>>> parent of 1e5195cf (modelviewset (replaced, self with super to work perform_create))
]