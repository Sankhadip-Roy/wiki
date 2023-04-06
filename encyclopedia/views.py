from django.shortcuts import render
import markdown
import random
from . import util
from django.http import HttpResponse
from django.shortcuts import redirect


def mdToHtml(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    html_content = mdToHtml(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This Entry Does Not Exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    if request.method == 'POST':
        entry_search = request.POST['q']

    for item in util.list_entries():
        if entry_search.lower() == item.lower():
            return redirect('entry', item)
    else:
        allEntries = util.list_entries()
        recommendation = []
        for entry in allEntries:
            if entry_search.lower() in entry.lower():
                recommendation.append(entry)
        if (len(recommendation) == 0):
            return render(request, "encyclopedia/error.html", {
                "message": "Entry does not exist."
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = mdToHtml(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })


def edit(request, title):
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })


def save_edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('entry', title)


def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    return redirect('entry', rand_entry)
