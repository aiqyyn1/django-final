from django.shortcuts import render, redirect
from .models import Notes
from .forms import *
from youtubesearchpython import VideosSearch
from django.contrib import messages
from django.views import generic
import requests

# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, tittle=request.POST['tittle'], description=request.POST['description'])
            notes.save()
        messages.success(request, f"Notes Added from {request.user.username} Successfully")
    else:
        form = NotesForm()
    form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finish = request.POST['is_finished']
                if finish == 'on':
                    finish = True
                else:
                    finish = False
            except:
                finish = False
            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                tittle=request.POST['tittle'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finish
            )
            homework.save()
            messages.success(request, f'Homework added from {request.user.username}!')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks': homework, 'homeworks_done': homework_done, 'form': form}

    return render(request, 'dashboard/homework.html', context)


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=30)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc =''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)


def todo(request):
      global todos
      if request.method == 'POST':
           form = TodoForm(request.POST)
           if (form.is_valid()):
                try:
                    finished=request.POST["is_finished"]
                    if (finished == "on"):
                        finished=True
                    else:
                        finished=False
                except:
                    finished = False
                todos = Todo(
                      user=request.user,
                      title=request.POST['title'],
                      is_finished=finished )
                todos.save()
                messages.success(request,f"Todo Added from {request.user.username}!!")
      else:
         form = TodoForm()
      todo=Todo.objects.filter(user=request.user)
      if  len(todo) == 0:
          todos_done=True
      else:
          todos_done=False

      context = {
          'form':form,
          'todos': todo,
          'todos_done':todos_done

      }
      return render(request, "dashboard/todo.html", context)


def update_todo(request, pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return  redirect ('todo')

def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


def books(request):


    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text

        r=requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get("subtitle"),
                'description': answer['items'][i]['volumeInfo'].get("description"),
                'count': answer['items'][i]['volumeInfo'].get("pageCount"),
                'categories': answer['items'][i]['volumeInfo'].get("categories"),
                'rating': answer['items'][i]['volumeInfo'].get("pageRating"),
                'thumbnail': answer['items'][i]['volumeInfo'].get("imageLinks").get("thumbnail"),
                'preview': answer['items'][i]['volumeInfo'].get("previewLink"),
            }

            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)



def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text

        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                 'input':text,
                'phonetics': phonetics,
                 'audio': audio,
                'definition': definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                 'form':form,
                  'input':''
            }
            return render (request, 'dashboard/dictionary.html', context)
    else:
        form=DashboardForm()
        context = {
        'form':form
             }
    return  render(request, 'dashboard/dictionary.html', context)