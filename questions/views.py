from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from questions.models import Question, Answer


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


def settings(request, *args, **kwarags):
    context = {}
    GetMembersTags(context)
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


def ask(request, *args, **kwarags):
    context = {}
    GetMembersTags(context)
    return render(request, "questions/ask.html", context)


def login(request, *args, **kwarags):
    context = {}
    GetMembersTags(context)
    return render(request, "questions/login.html", context)


def signup(request, *args, **kwarags):
    context = {}
    GetMembersTags(context)
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
