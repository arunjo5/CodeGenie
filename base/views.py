from django.shortcuts import redirect, render
from django.db.models import Q
from .models import User, Language, Snippet, Comment, Explain, Translate
from .forms import ExplainForm, MyUserCreationForm, TranslateForm, UserForm, SnippetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect

# from codecarbon import EmissionsTracker
import openai
import os
from dotenv import load_dotenv
from djangocodemirror.settings import *
load_dotenv()


openai.api_key = ('KEY HERE')

# Create your views here.
def index(request):
    return render(request, 'base/index.html')



def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
 
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does NOT exists!')
        
        # Authentication
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Adds session in db and browser
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credentials Incorrect')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)



def registerPage(request):
    form = MyUserCreationForm

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration!')
    
    context = {'form':form}
    return render(request, 'base/login_register.html', context)



def logoutPage(request):
    logout(request)
    return redirect('home')



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    snippets = Snippet.objects.filter(Q(language__name__icontains=q) |
                                  Q(name__icontains=q) |
                                  Q(code__icontains=q)
    )

    languages = Language.objects.all()

    # ChatBot
    if request.GET.get('res') != None:

        res = request.GET.get('res')
        reply = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"You are a chatbot who only answers questions about coding, computer science, AI, software development, Information Technology and closely related fields and don't entertain other questions. Answer the following question:\n\n{res}?",
        temperature=0.3,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["You:"]
        )
        final_answer = reply["choices"][0]["text"].lstrip()
        context = {'snippets':snippets, 'languages':languages,
        'reply':reply, 'final_answer':final_answer, 'res':res}
        return render(request, 'base/home.html', context)

    else:
        context = {'snippets':snippets, 'languages':languages}
        return render(request, 'base/home.html', context)


def snippet(request, pk):
    snippet = Snippet.objects.get(id=pk)
    snippet_comments = snippet.comment_set.all()

    # To add a new message
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = Comment.objects.create(
                user = request.user,
                snippet = snippet,
                body = request.POST.get('body')
            )
            
            return redirect('snippet', pk=snippet.id)
        else:
            return redirect('login')

    context = {'snippet':snippet, 'snippet_comments':snippet_comments}
    return render(request, 'base/snippet.html', context)



@login_required(login_url='login')
def createSnippet(request):
    form = SnippetForm()
    languages = Language.objects.all()

    if request.method == 'POST':
        language_name = request.POST.get('language')

        language, created = Language.objects.get_or_create(name=language_name)

        # Snippet creation
        Snippet.objects.create(
            author = request.user,
            language = language,
            name = request.POST.get('name'),
            code = request.POST.get('code')
        )
        return redirect('home')
    
    
    context = {'form':form, 'languages':languages}
    return render(request, 'base/create_snippet.html', context)



@login_required(login_url='login')
def deleteSnippet(request, pk):
    snippet = Snippet.objects.get(id=pk)

    if request.user != snippet.author:
        messages.error(request, 'you are not allowed here')
    
    if request.method == 'POST':
        snippet.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':snippet})




def autoCode(request):
    if request.GET.get('p'):
        p = request.GET.get('p')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"The user is novice to programming. Write a code for the following prompt:\n\n{p}",
            temperature=0,
            max_tokens=1000 ,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0
        )
        final_answer = response["choices"][0]["text"].lstrip()
        context = {'response':response, 'final_answer':final_answer, 'p':p}
        return render(request, 'base/autocode.html', context)

    context = {}
    return render(request, 'base/autocode.html', context)



def codeExplain(request):
    form = ExplainForm
    explain = Explain.objects.all()
    

    if request.method == 'POST':
        get_explain_code = request.POST.get('explain')

        Explain.objects.create(
            explain = request.POST.get('explain')
        )

        answer = openai.Completion.create(
        model="text-davinci-003",
        prompt="The user is a novice in programming. Explain the following code in detail. Use bullet points if required\n\n"+str(Explain.objects.last()),
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        final_answer = answer["choices"][0]["text"].lstrip()
        print(final_answer)

        # To reload the page with prefilled form
        form = ExplainForm(initial={'explain':f'{str(Explain.objects.last())}'})
        context = {'form':form, 'explain':explain, 'final_answer':final_answer}
        return render(request, 'base/explain.html', context)
    context = {'form':form}
    return render(request, 'base/explain.html', context)



def codeTranslate(request):
    form = TranslateForm
    get_translate = Translate.objects.all()
    

    if request.method == 'POST':
        first_language = request.POST.get('first_language')
        second_language = request.POST.get('second_language')
        translate = request.POST.get('translate')

        Translate.objects.create(
            translate = request.POST.get('translate'),
            first_language = request.POST.get('first_language'),
            second_language = request.POST.get('second_language')
        )
        
        answer = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"##### The user is a novice to programming. Translate the following code from {first_language} into {second_language}. Translate the code such the translated code is ready to be executed.\n### {first_language}\n\n{translate}\n\n### {second_language}\n\n",
        temperature=0.05,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        final_answer = answer["choices"][0]["text"].lstrip()

        # To access the latest field values from the database
        latest_object = Translate.objects.latest('id')
        translate_from = latest_object.first_language
        translate_to = latest_object.second_language
        code = latest_object.translate

        # print(a)
        # print(b)
        # print(c)
        form = TranslateForm(initial={'first_language':f'{translate_from}','second_language':f'{translate_to}', 'translate':f'{code}' })

        context = {'form':form, 'final_answer':final_answer}

        return render(request, 'base/translate.html', context)

    context = {'form':form}
    return render(request, 'base/translate.html', context)

