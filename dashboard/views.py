from django.shortcuts import render, redirect
from dashboard.models import Homework, Note, Task
from dashboard.forms import HomeworkForm, NoteForm, TaskForm
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from youtubesearchpython import VideosSearch
import requests
import wikipedia


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "dashboard/index.html")


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            login(request, user)
            error = "no"
        except:
            error = "yes"
    context = {
        'error': error,
    }
    return render(request, 'common/login.html', context)


def signout(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = ""
    if request.method == 'POST':
        l = request.POST['lname']
        f = request.POST['fname']
        e = request.POST['email']
        u = request.POST['uname']
        p = request.POST['pwd']
        try:
            User.objects.create_user(
                last_name=l, first_name=f, username=u, email=e, password=p)
            error = "no"
        except:
            error = "yes"
    context = {
        'error': error,
    }
    return render(request, 'common/register.html', context)


@login_required(login_url='login')
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method == 'POST':
        c = request.POST['currentpwd']
        n = request.POST['newpwd']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    context = {
        'error': error,
    }
    return render(request, 'common/change_password.html', context)


@login_required(login_url='login')
def profile(request):
    return render(request, "dashboard/profile.html")


@login_required(login_url='login')
def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    return render(request, "dashboard/home.html")


# =============== Notes ===============
@login_required(login_url='login')
def notes(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            user_note = form.save(commit=False)
            user_note.user = request.user
            user_note.title = request.POST.get('title')
            user_note.description = request.POST.get('description')
            user_note.save()
            return redirect('notes')
    else:
        form = NoteForm()
        notes = Note.objects.filter(user=request.user)

    context = {
        'notes': notes,
        'form': form,
    }
    return render(request, "dashboard/notes.html", context)


@login_required(login_url='login')
def delete_note(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return redirect('notes')


@login_required(login_url='login')
def note_detail(request, pk):
    note = Note.objects.get(id=pk)
    context = {
        'note': note,
    }
    return render(request, 'dashboard/note_detail.html', context)


# class NoteDetail(generic.DetailView):
#     model = Note


# =============== Homeworks ===============
@login_required(login_url='login')
def homeworks(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            user_homework = form.save(commit=False)
            user_homework.user = request.user
            user_homework.subject = request.POST.get('subject')
            user_homework.title = request.POST.get('title')
            user_homework.description = request.POST.get('description')
            user_homework.deadline = request.POST.get('deadline')

            try:
                finished = request.POST['completed']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            user_homework.completed = finished

            user_homework.save()
            return redirect('homeworks')
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user)

    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {
        'homeworks': homeworks,
        'homework_done': homework_done,
        'form': form,
    }
    return render(request, "dashboard/homeworks.html", context)


@login_required(login_url='login')
def update_homework(request, pk):
    homework = Homework.objects.get(id=pk)
    if homework.completed == True:
        homework.completed = False
    else:
        homework.completed = True
    homework.save()
    return redirect('homeworks')


@login_required(login_url='login')
def delete_homework(request, pk):
    homework = Homework.objects.get(id=pk)
    homework.delete()
    return redirect('homeworks')


# =============== Youtube ===============
@login_required(login_url='login')
def youtube(request):
    error = ""
    if request.method == "POST":
        try:
            search = request.POST['search']
            video = VideosSearch(search, limit=10)

            result_list = []

            for i in video.result()['result']:
                result_dict = {
                    'input': search,
                    'title': i['title'],
                    'duration': i['duration'],
                    'thumbnail': i['thumbnails'][0]['url'],
                    'channel': i['channel']['name'],
                    'link':  i['link'],
                    'views': i['viewCount']['short'],
                    'published': i['publishedTime'],
                }
                desc = ''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc += j['text']
                result_dict['description'] = desc
                result_list.append(result_dict)
            error = "no"
        except:
            error = "yes"

        context = {
            'results': result_list,
            'error': error,
        }
        return render(request, 'dashboard/youtube.html', context)

    return render(request, "dashboard/youtube.html")


# =============== Todo ===============
@login_required(login_url='login')
def todo(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            user_task = form.save(commit=False)
            user_task.user = request.user
            user_task.title = request.POST.get('title')

            try:
                finished = request.POST['completed']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            user_task.completed = finished

            user_task.save()
            return redirect('todo')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user)

    if len(tasks) == 0:
        task_done = True
    else:
        task_done = False

    context = {
        'tasks': tasks,
        'task_done': task_done,
        'form': form,
    }
    return render(request, "dashboard/todo.html", context)


@login_required(login_url='login')
def update_todo(request, pk):
    task = Task.objects.get(id=pk)
    if task.completed == True:
        task.completed = False
    else:
        task.completed = True
    task.save()
    return redirect('todo')


@login_required(login_url='login')
def delete_todo(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('todo')


# =============== Books ===============
def books(request):
    error = ""
    if request.method == "POST":
        try:
            search = request.POST['search']

            url = 'https://www.googleapis.com/books/v1/volumes?q='+search

            r = requests.get(url)
            answer = r.json()

            result_list = []

            for i in range(10):
                result_dict = {
                    'title': answer['items'][i]['volumeInfo']['title'],
                    'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description': answer['items'][i]['volumeInfo'].get('description'),
                    'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories': answer['items'][i]['volumeInfo'].get('categories'),
                    'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                    'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                    'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
                }
                result_list.append(result_dict)
            error = "no"
        except:
            error = "yes"

        context = {
            'results': result_list,
            'error': error,
        }

        return render(request, 'dashboard/books.html', context)

    return render(request, "dashboard/books.html")


# =============== Dictionary ===============
@login_required(login_url='login')
def dictionary(request):
    error = ""
    if request.method == "POST":
        search = request.POST['search']

        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'+search

        r = requests.get(url)
        answer = r.json()

        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            origin = answer[0]['origin']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            partOfSpeech = answer[0]['meanings'][0]['partOfSpeech']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            antonyms = answer[0]['meanings'][0]['definitions'][0]['antonyms']
            try:
                example = answer[0]['meanings'][0]['definitions'][0]['example']
                error = "no"
                context = {
                    'word': search,
                    'phonetics': phonetics,
                    'audio': audio,
                    'origin': origin,
                    'definition': definition,
                    'example': example,
                    'partOfSpeech': partOfSpeech,
                    'synonyms': synonyms,
                    'antonyms': antonyms,
                    'error': error,
                }
            except:
                error = "no"

                context = {
                    'word': search,
                    'phonetics': phonetics,
                    'audio': audio,
                    'origin': origin,
                    'definition': definition,
                    'example': 'None',
                    'partOfSpeech': partOfSpeech,
                    'synonyms': synonyms,
                    'antonyms': antonyms,
                    'error': error,
                }

        except:
            error = "yes"

            context = {
                'error': error,
            }

        return render(request, 'dashboard/dictionary.html', context)

    return render(request, "dashboard/dictionary.html")


# =============== Wikipedia ===============
@login_required(login_url='login')
def wiki(request):
    error = ""
    if request.method == "POST":
        search = request.POST['search']

        try:
            wiki = wikipedia.page(search)

            try:
                error = "no"

                context = {
                    'title': wiki.title,
                    'link': wiki.url,
                    'summary': wiki.summary,
                    'error': error,
                }
            except:
                error = "no"

                context = {
                    'title': wiki.title,
                    'link': 'None',
                    'summary': wiki.summary,
                    'error': error,
                }
        except:
            error = "yes"

            context = {
                'error': error,
            }

        return render(request, 'dashboard/wiki.html', context)

    return render(request, "dashboard/wiki.html")


# =============== Converter ===============
@login_required(login_url='login')
def converter(request):
    return render(request, "dashboard/converter.html")


@login_required(login_url='login')
def unit_converter(request):
    return render(request, "dashboard/unit_converter.html")


@login_required(login_url='login')
def number_converter(request):
    return render(request, "dashboard/number_converter.html")


@login_required(login_url='login')
def morse_converter(request):
    return render(request, "dashboard/morse_converter.html")


@login_required(login_url='login')
def currency_converter(request):
    return render(request, "dashboard/currency_converter.html")


