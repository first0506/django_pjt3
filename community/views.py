from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Review, Comment
from .forms import ReviewForm, CommentForm

# Create your views here.
@login_required
def create(request):
    if request.method=='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form' : form
    }
    return render(request, 'community/form.html', context)

def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews' : reviews
    }
    return render(request, 'community/review_list.html', context)

def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm()
    context = {
        'review' : review,
        'form' : form,
    }
    return render(request, 'community/review_detail.html', context)

@require_POST
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user==review.user:
        if request.method=='POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form' : form
        }
        return render(request, 'community/form.html', context)
    else:
        return redirect('community:detail', review.pk)

@login_required
def delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user==review.user:
        review.delete()
    else:
        return redirect('community:detail', review.pk)
    return redirect('community:index')

@require_POST
def comments_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
    return redirect('community:detail', review.pk)

@login_required
def comments_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user==comment.user:
        comment.delete()
    return redirect('community:detail', review_pk)