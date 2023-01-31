from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse

import markdown
import random

# Create your views here.

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        content = markdown.markdown(f"{title.capitalize()} page not found.")
    content = markdown.markdown(content)
    return render(request, "encyclopedia/entry.html",{
        "title": title,
        "content": content
    })


def add_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        contents = request.POST.get("content")
        entryExist = util.get_entry(title)
        if entryExist != None:
            content = util.list_entries()
            messages.error(request, "Entry already exists!")
            return render(request, "encyclopedia/add.html", {
                "content": content
            })
        else:
            content = util.save_entry(title, contents)
            content = markdown.markdown(contents)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content": content,
            })
    else:
        title = ""
        contents = ""
        content = util.list_entries()
        return render(request, "encyclopedia/add.html", {
            "content": content
        })


def randoms(request):
    choice = random.choice(util.list_entries())
    content = util.get_entry(choice)
    content = markdown.markdown(content)
    return render(request, "encyclopedia/entry.html",{
        "title": choice,
        "content": content
    })


def search(request):
    content_list = util.list_entries()
    find_entries = list()
    search = request.GET.get("q")
    if search in content_list:
        return HttpResponseRedirect(f"wiki/{search}")
    for content in content_list:
        if search in content:
            find_entries.append(content)
    if find_entries:
        return render(request, "encyclopedia/search.html", {
            "content": find_entries,
            "search": search 
        })


def edit_page(request, title):
    contents = util.get_entry(title)
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect("encyclopedia:entry", title)
    if contents:
        content = util.get_entry(title)
        contents = markdown.markdown(content)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": contents
        })
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))