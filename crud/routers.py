from rest_framework import routers
from crud import views


router = routers.SimpleRouter()
router.register = (r'articles' , views.ArticleViewSets().as_view())
router.register = (r'author',views.AuthorView().as_view())
urlpatterns = router.urls