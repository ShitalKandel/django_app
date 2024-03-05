from django.urls import path,include
from snippets.views import api_root,SnippetViewSets,UserViewSets
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register(r'snippets',SnippetViewSets,basename='snippet')
routers.register(r'users',UserViewSets,basename='users')


urlpatterns = [
    path('',include(routers.urls)),
]



# urlpatterns= format_suffix_patterns([
#     path('snippets/', views.SnippetList.as_view(),name='snippet-list'),
#     path('snippet/<int:pk>/',views.SnippetDetail.as_view(),name='snippet-detail'),
#     path('user/', views.UserList.as_view(),name='user-list'),
#     path('user/<int:pk>/',views.UserDetail.as_view()),
#     path('',views.api_root,name='user-detail'),
#     path('snippet/<int:pk>/highlight',views.SnippetHighlights.as_view(),name='snippet-highlight')

# ])


# snippet_list = SnippetViewSets.as_view({
#     "get":"list",
#     "post":"create"
# })
# snippet_detail = SnippetViewSets.as_view({
#     "get":"retrieve",
#     "put":"update",
#     "patch":"partial_update",
#     "delete":"destroy"
# })
# snippet_highlight = SnippetViewSets.as_view({
#     "get":"highlight"
# },renderer_classes = [renderers.StaticHTMLRenderer])
# user_list = UserViewSets.as_view({
#     "get":"list"
# })
# user_detail = UserViewSets.as_view({
#     "get":"retrieve"
# })