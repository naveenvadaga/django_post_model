from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('posts/', views.post_list),
    path('users/', views.person_list),
    path('comments/', views.comment_list),
    path('reacts/', views.react_list),
    path('posts/<int:pk>', views.get_post_),
    path('comments/<int:post_id>/replies', views.get_replies_for_comment_view),
    path('post', views.create_post_view),
    path('commenttopost/', views.add_comment_to_post),
    path('replytocomment/', views.reply_to_comment_view),
    path('reacttopost/', views.react_to_post_view),
    path('reacttocomment/', views.react_to_comment_view),
    path('getuserpost/<int:pk>', views.get_post_user_view),
    path('positiveposts/', views.get_posts_with_more_positive_reactions_view),
    path('postsreactedbyuser/<int:user_id>', views.get_posts_reacted_by_user_view),
    path('reactionstopost/<int:post_id>', views.get_reactions_to_post_view),
    path('reactionsmetricstopost/<int:post_id>', views.get_reaction_metrics_view),
    path('reactcount', views.get_total_reaction_count_view),
    path('post/<int:post_id>/delete', views.delete_post)
]

urlpatterns = format_suffix_patterns(urlpatterns)
