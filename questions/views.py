from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.contrib.auth.models import User
from questions.models import Question, Answer,UserProfile,Tag
from django.core.files.uploadedfile import UploadedFile
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout


def index(request, *args, **kwarags):
    questions = Question.objects.new_questions()
    context = {}
    context["questions_page"] = paginate(questions, request, 5)
    GetMembersTags(context)
    return render(request, "questions/index.html", context)


def question(request, *args, **kwarags):
    question = Question.objects.get(id=kwarags.get("id"))
    answers = Answer.objects.filter(question_id=kwarags.get("id"))

    context = {"question": question}
    context["questions_page"] = paginate(answers, request, 5)
    GetMembersTags(context)
    return render(request, "questions/question.html", context)


def hot_questions(request, *args, **kwarags):
    questions = Question.objects.get_hot_questions()
    context = {}
    GetMembersTags(context)
    context["questions_page"] = paginate(questions, request, 5)
    return render(request, "questions/hot_questions.html", context)


class ProfieleForm(forms.ModelForm):
     
    nickname = forms.CharField(max_length=64, required=True)
    avatar = forms.ImageField(required=False)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if not avatar or not isinstance(avatar, UploadedFile):
            return avatar

        if avatar:
            max_size = 2 * 1024 * 1024  
            if avatar.size > max_size:
                raise forms.ValidationError("Размер файла не должен превышать 2 МБ.")

            valid_mime_types = ['image/jpeg', 'image/png']
            if avatar.content_type not in valid_mime_types:
                raise forms.ValidationError("Поддерживаются только файлы формата JPEG, PNG.")

        return avatar

    class Meta:
        model=User
        fields=('username','email')

    def __init__(self, *args, **kwargs):
        # Передаём userprofile через kwargs
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)
        if self.userprofile:
            self.fields['nickname'].initial = self.userprofile.nickname
            self.fields['avatar'].initial = self.userprofile.avatar

    def save(self, commit=True):
        user = super().save(commit=commit)
        
        if self.userprofile:
            self.userprofile.nickname = self.cleaned_data['nickname']
            if self.cleaned_data.get('avatar'):
                self.userprofile.avatar = self.cleaned_data['avatar']
            if commit:
                self.userprofile.save()
        return user
    


@login_required(login_url=reverse_lazy('login'))
def settings(request, *args, **kwarags):
    context = {}
    GetMembersTags(context)

    form = ProfieleForm(instance=request.user, userprofile=request.user.userprofile)

    if request.method == 'POST':  
        
        form = ProfieleForm(request.POST,request.FILES,instance=request.user,userprofile=request.user.userprofile)
        if form.is_valid():
            user = form.save()
            context["form"]=form
            return render(request, "questions/settings.html", context)

    context["form"]=form

    return render(request, "questions/settings.html", context)


def tag(request, *args, **kwarags):
    tag_name = kwarags.get("tag_name")
    questions_page = Question.objects.get_tag_questions(tag_name)
    context = {
        "tag_name": tag_name,
    }
    context["questions_page"] = paginate(questions_page, request, 5)
    GetMembersTags(context)
    return render(request, "questions/tag.html", context)


def user(request, *args, **kwarags):
    nickname = kwarags.get("user_nickname")
    questions_page = Question.objects.get_user_questions(nickname)
    context = {
        "nickname": nickname,
    }
    context["questions_page"] = paginate(questions_page, request, 5)
    GetMembersTags(context)
    return render(request, "questions/user.html", context)

class AskForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Введите теги через запятую (например: python, django)"
    )
    class Meta:
        model = Question
        fields = ['title', 'text']
       
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        tag_list = [t.strip().lower() for t in tags_str.split(',') if t.strip()]
        # опциональная валидация
        if len(tag_list) > 10:
            raise forms.ValidationError("Максимум 10 тегов.")

        for tag in tag_list:
            if len(tag) > 30:
                raise forms.ValidationError(f"Тег '{tag}' слишком длинный.")

        return tag_list


    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Заголовок не может быть пустым.")
        if len(title) > 256:
            raise forms.ValidationError("Заголовок не может быть длиннее 256 символов.")
        return title

    def save(self, commit=True):
        question = super().save(commit=False)
        question.user_id = self.user  

        if commit:
            question.save()

        tag_names = self.cleaned_data.get('tags', [])

        # Создаём или получаем объекты Tag и собираем их в список
        tag_objs = []
        for name in tag_names:
            tag_obj = Tag.objects.get_or_create(name=name)[0]
            tag_objs.append(tag_obj)

        if commit:
            question.tags.set(tag_objs)
        return question

@login_required(login_url=reverse_lazy('login'))
def ask(request, *args, **kwarags):
    context = {}
    GetMembersTags(context) 

    form = AskForm(user=request.user)

    if request.method == 'POST':  
        
        form = AskForm(request.POST,request.FILES, user=request.user)
        if form.is_valid():
            question = form.save()
            context["form"]=form
            return redirect(reverse('question', kwargs={'id': question.id}))


    context["form"]=form

    return render(request, "questions/ask.html", context)


def login_view(request, *args, **kwargs):
    
    context = {}
    GetMembersTags(context)

    form = AuthenticationForm(request)

    if request.method == 'POST':  
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('index'))

    context["form"]=form
    return render(request, "questions/login.html", context)


def logout_view(request, *args, **kwarags):
    logout(request)
    return redirect(reverse('index'))




class RegisterForm(UserCreationForm):

    nickname = forms.CharField(max_length=64, required=True)

    class Meta:
        model=User
        fields=('username','email', 'password1','password2')

    def save(self, commit=True):
        user = super().save(commit=commit)

        UserProfile.objects.create(
            user=user,
            nickname=self.cleaned_data["nickname"],
        )

        return user



def signup(request, *args, **kwarags):
    context = {}
    GetMembersTags(context)

    form = RegisterForm()

    if request.method == 'POST':  
        
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user= form.save()
            login(request,user)
            return redirect(reverse('index'))

    context["form"]=form

    return render(request, "questions/signup.html", context)


def paginate(objects_list, request, per_page=6):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get("page", 1)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        raise Http404("Страница не найдена")
    data = paginator.get_page(page)
    return data


def GetMembersTags(context, request=None):
    questions = Question.objects.get_hot_questions_parameters()[:6]
    popular_tags = []
    best_members = []
    for question in questions:
        popular_tags += question.tag_names
        best_members.append(question.nickname)

    is_authenticated = True 

    user_data = [
        {"Login": "dr_pepper", "Email": "dr.pepper@mail.ru", "NickName": "Dr. Pepper"}
    ]

    context["best_members"] = best_members
    context["popular_tags"] = popular_tags
    context["user_data"] = user_data
    context["is_authenticated"] = is_authenticated
