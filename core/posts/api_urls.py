from django.urls import path
from . import api_view 

urlpatterns = [
    path("posts/", api_view.post_list_api, name="post_list_api"),
    path("feed/", api_view.feed_api, name="feed_api"),
    path("posts/<int:post_id>/like/", api_view.toggle_like_api, name="toggle_like_api"),
    path("posts/<int:post_id>/comment/", api_view.add_comment_api, name="add_comment_api"),
]
