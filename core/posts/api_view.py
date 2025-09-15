from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

# Feed API مع privacy logic
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed_api(request):
    posts = Post.objects.filter(privacy__in=["public", "friends"]) | Post.objects.filter(author=request.user)
    posts = posts.order_by("-created_at")
    serializer = PostSerializer(posts, many=True, context={"request": request})
    return Response(serializer.data)

# Post list API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list_api(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# Toggle Like API
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_like_api(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        return Response({"liked": False, "likes_count": post.likes.count()})
    return Response({"liked": True, "likes_count": post.likes.count()})

# Add Comment API
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_comment_api(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.data.get("text")
    if not text:
        return Response({"error": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)
    comment = Comment.objects.create(user=request.user, post=post, text=text)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
