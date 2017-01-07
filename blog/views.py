from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.db.models import Q
# Create your views here.

def post_create(request):
    #checks if user is authorized
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404


    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid(): # checks if all required fields are filled out
        instance = form.save(commit=False)
        instance.save()
        # succes message
        messages.success(request, "Succesfully Created")
        # return user to list page after creations
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }

    return render(request, "post_form.html", context)

def post_detail(request, id):
    #
    instance = get_object_or_404(Post, id=id)
    context_data = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context_data)

def post_list(request): #list items
    queryset_list = Post.objects.all().order_by("-timestamp")

    query = request.GET.get("searchquery")
    if query:
        queryset_list = queryset_list.filter(

            Q(title__icontains=query) |
            Q(content__icontains=query)
            ).distinct()

    paginator = Paginator(queryset_list, 4) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context_data ={
        "object_list": queryset,
        "title": "List",
    }
    return render(request, "post_list.html", context_data)
    #return HttpResponse("<h1>List</h1>")

def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid(): #if all required fields are filled out
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    context_data = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context_data)

def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Succesfully Deleted")
    return redirect("posts:list")
