from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like
from .forms import PostForm

# ----------------------------
# HTML Views
# ----------------------------
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "posts/post_list.html", {"posts": posts})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("feed")  # Redirect to feed after creation
    else:
        form = PostForm()
    return render(request, "posts/post_create.html", {"form": form})


# ----------------------------
# API Views (DRF)
# ----------------------------
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, CommentSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feed_api(request):
    posts = Post.objects.filter(privacy__in=["public", "friends"]) | Post.objects.filter(author=request.user)
    posts = posts.order_by("-created_at")
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_like_api(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        return Response({"liked": False, "likes_count": post.likes.count()})
    return Response({"liked": True, "likes_count": post.likes.count()})


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


# ----------------------------
# Feed View (HTML)
# ----------------------------
@login_required
def feed_view(request):
    posts = Post.objects.all().order_by("-created_at")
    for post in posts:
        post.liked = post.likes.filter(user=request.user).exists()
    return render(request, "posts/feed.html", {"posts": posts})


# ----------------------------
# Delete Post
# ----------------------------
@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    # Ensure only the author can delete
    if post.author == request.user:
        post.delete()
    return redirect('feed')
