from django.shortcuts import render

from . import util

from markdown2 import Markdown

import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    markdowner=Markdown()
    if content == None:
        return render(request, "encyclopedia/error.html",{
            "alert": "Entry page was not found"
            
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": markdowner.convert(content)
        })


def search(request):
    if request.method=="POST":
        search_result= request.POST['q']
        content = util.get_entry(search_result)
        markdowner=Markdown()
        if content is not None:
            return render(request, "encyclopedia/entry.html",{
            "title": search_result,
            "content": markdowner.convert(content)
        })
        else:
            entry_list= util.list_entries()
            search_list=[]
            for x in entry_list:
                if search_result.lower() in x.lower():
                    search_list.append(x)
            return render(request, "encyclopedia/search.html",{
                "content": search_list
            })
def newpage(request):
    if request.method=="POST":
        result_title=request.POST['title_text']
        result_textarea=request.POST['textarea']
        entry_list= util.list_entries()
        if result_title in entry_list:
            return render(request, "encyclopedia/error.html",{
            "alert": "Entry already exists."})
        else:
            util.save_entry(result_title,result_textarea)
            content=util.get_entry(result_title)
            
            markdowner=Markdown()
            return render(request, "encyclopedia/entry.html",{
            "title": result_title,
            "content": markdowner.convert(content)
        })

    return render(request, "encyclopedia/newpage.html")

def edit(request):
    if request.method=="POST":
        title=request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "content":content
        })
def edit_save(request):
    if request.method=="POST":
        title = request.POST['title_text']
        content = request.POST['textarea']
        util.save_entry(title, content)
        
        result_content=util.get_entry(title)
            
        markdowner=Markdown()
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": markdowner.convert(result_content)
        })

def random_page(request):
    entry_list=util.list_entries()
    random_entry=random.choice(entry_list)
    result_content=util.get_entry(random_entry)
    markdowner=Markdown()
    return render(request, "encyclopedia/entry.html",{
            "title": random_entry,
            "content": markdowner.convert(result_content)
        })
