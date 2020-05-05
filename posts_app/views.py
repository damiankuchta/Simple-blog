import datetime
import calendar

from django.db.models import Count
from django.shortcuts import render, redirect, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from comments_app.forms import CommentForm
from comments_app.models import Comment
from . import models
from hashtags_app import models as hash_tags_models

# Create your views here.
def posts(request, page=1, hash_tag=None, date=None):

    """filter by hastag query param"""
    hash_tag = request.GET.get("hash_tag")

    """way of sorting the posts"""
    sort_by = request.GET.get("sort_by") or "date"

    """filter by date query param"""
    if request.GET.get("date"):
        date = list(map(int, request.GET.get("date").split(",")))
    else:
        date = None

    """get the posts"""
    if hash_tag or date:
        """for some reason order_by doesnt work with filter so have to use ordered here"""
        if hash_tag:
            posts = get_list_or_404(models.Post.objects
                                    .filter(hash_tags__name__contains=hash_tag)
                                    .annotate(num_comments=Count('comments'))
                                    .order_by(sort_by))
            #todo fix empty tags
            if posts:

                hash_tag_object = hash_tags_models.HashTag.objects.get(name=hash_tag)
                HitCountMixin.hit_count(request, HitCount.objects.get_for_object(hash_tag_object))

        elif date:
            posts = get_list_or_404(models.Post.objects
                                    .filter(date__month=date[1])
                                    .annotate(num_comments=Count('comments'))
                                    .order_by(sort_by))
            #todo fix empty dates
    else:
        posts = get_list_or_404(models.Post.objects.annotate(num_comments=Count('comments')).order_by(sort_by))

    """Pagination"""
    pages = Paginator(posts, 10)
    page = pages.page(page)

    return render(request, "posts_app/posts.html", {"page": page,
                                                    "pages": pages,
                                                    "hash_tag": hash_tag})


def post(request, post_id):

    """Get post"""
    try:
        post = models.Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        return redirect("posts")

    """Get all the comments"""
    try:
        comments = post.comments.all()
    except ObjectDoesNotExist:
        comments = None

    """Comment form"""
    if request.POST:
        comment = Comment(user=request.user, post=post)
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid() and request.user.is_authenticated:
            comment_form.save()
    else:
        comment_form = CommentForm()

    """Hit counter"""
    HitCountMixin.hit_count(request,  HitCount.objects.get_for_object(post))

    return render(request, "posts_app/post.html", {"post": post,
                                                   "comments": comments,
                                                   "comment_form": comment_form})

