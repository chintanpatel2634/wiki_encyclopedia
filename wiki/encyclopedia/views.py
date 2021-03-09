from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from . import util

def validateTitle(title):
    for entry in util.list_entries():
        if entry == title:
            raise ValidationError('This page already exist')

class NewSubmitForm(forms.Form):
    q = forms.CharField()

class NewEntryForm(forms.Form):
    title = forms.CharField(required=True, label="", widget=forms.TextInput({"placeholder":"Title of the Page","class":"mt-2 w-25 p-2"}),
                                validators=[validateTitle])
    pagedetails = forms.CharField(required=True, label="", 
                                   widget = forms.Textarea({"placeholder":"Enter the Markdown Text","class":"mt-2 w-75 p-2"}))

def index(request):

    if request.method == "POST":
        data = NewSubmitForm(request.POST)

        if data.is_valid():
            query = data.cleaned_data["q"]

            if query != None:
                entryData = util.get_entry(query)

                if entryData == None:
                    entryMatched = list(sorted(entry for entry in util.list_entries() if query in entry))
                    
                    return render(request, "encyclopedia/index.html", {
                        "name" : "All Pages with substring \'" + query + "\'",
                        "entries" : entryMatched
                    })

                return HttpResponseRedirect(reverse("entry", args=(query,)))

    return render(request, "encyclopedia/index.html", {
        "name" : "All Pages",
        "entries" : util.list_entries()
    })

def entry(request, name):
    return render(request, "encyclopedia/name.html", {
        "entry" : util.get_entry(name),
        "title" : name
    })

def newentry(request):
    if request.method == "POST":
        data = NewEntryForm(request.POST)

        if data.is_valid():
            
            title = data.cleaned_data["title"]
            pagedetails = data.cleaned_data["pagedetails"]

            util.save_entry(title, pagedetails)

            return HttpResponseRedirect(reverse("entry", args=(title,)))
        else:
            
            return render(request, "encyclopedia/newentry.html", {
                "form" : data
            })

    return render(request, "encyclopedia/newentry.html", {
        "form" : NewEntryForm()
    })