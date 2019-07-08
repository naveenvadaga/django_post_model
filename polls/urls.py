from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('posts/', views.post_list),
    path('users/',views.person_list),
    path('comments/',views.comment_list),
    path('reacts/',views.react_list),
    path('posts/<int:pk>',views.get_post)

]

urlpatterns = format_suffix_patterns(urlpatterns)
