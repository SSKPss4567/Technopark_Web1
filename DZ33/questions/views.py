from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from questions.models import Question,Answer,Tag

# Create your views here.

QUESTIONS = [
    {
        "id": 0,
        "question": "How to build a moon park1",
        "answer_count": 4,
        "description": "Etiam posuere quam ac quam. Maecenas aliquet accumsan leo. Nullam dapibus fermentum ipsum. Etiam quis quam. Integer lacinia. Nulla est. Nulla turpis magna, cursus sit amet, suscipit a, interdum id",
        "tags": ["black-jack", "bender"],
        "answers": [
            {
                "id": 0,
                "text": "You need to start with proper planning and funding. The first step is to secure investment from major space companies.",
                "likes": 15,
                "is_correct": False
            },
            {
                "id": 1,
                "text": "Actually, building a moon park requires international cooperation. NASA and Roscosmos should work together.",
                "likes": 8,
                "is_correct": False
            },
            {
                "id": 1,
                "text": "Actually, building a moon park requires international cooperation. NASA and Roscosmos should work together.",
                "likes": 8,
                "is_correct": False
            },
            {
                "id": 1,
                "text": "Actually, building a moon park requires international cooperation. NASA and Roscosmos should work together.",
                "likes": 8,
                "is_correct": False
            }
        ]
    },
    {
        "id": 1,
        "question": "How to build a moon park2",
        "answer_count": 2,
        "description": "Etiam posuere quam ac quam. Maecenas aliquet accumsan leo. Nullam dapibus fermentum ipsum. Etiam quis quam. Integer lacinia. Nulla est. Nulla turpis magna, cursus sit amet, suscipit a, interdum id",
        "tags": ["bender"],
        "answers": [
            {
                "id": 2,
                "text": "The main challenge is life support systems. You need closed ecological systems for long-term sustainability.",
                "likes": 12,
                "is_correct": False
            },
            {
                "id": 3,
                "text": "Radiation protection is crucial. You'll need several meters of lunar regolith as shielding.",
                "likes": 7,
                "is_correct": False
            }
        ]
    },
    {
        "id": 2,
        "question": "How to build a moon park3",
        "answer_count": 1,
        "description": "Etiam posuere quam ac quam. Maecenas aliquet accumsan leo. Nullam dapibus fermentum ipsum. Etiam quis quam. Integer lacinia. Nulla est. Nulla turpis magna, cursus sit amet, suscipit a, interdum id",
        "tags": ["black-jack", "bender"],
        "answers": [
            {
                "id": 4,
                "text": "Start with a small habitat module. Expand gradually as technology improves.",
                "likes": 9,
                "is_correct": False
            }
        ]
    },
    {
        "id": 3,
        "question": "How to build a moon park4",
        "answer_count": 1,
        "description": "Etiam posuere quam ac quam. Maecenas aliquet accumsan leo. Nullam dapibus fermentum ipsum. Etiam quis quam. Integer lacinia. Nulla est. Nulla turpis magna, cursus sit amet, suscipit a, interdum id",
        "tags": ["black-jack", "bender"],
        "answers": [
            {
                "id": 5,
                "text": "Water extraction from lunar ice is the key first step for any permanent settlement.",
                "likes": 11,
                "is_correct": False
            }
        ]
    },
    {
        "id": 4,
        "question": "How to build a moon park5",
        "answer_count": 1,
        "description": "Etiam posuere quam ac quam. Maecenas aliquet accumsan leo. Nullam dapibus fermentum ipsum. Etiam quis quam. Integer lacinia. Nulla est. Nulla turpis magna, cursus sit amet, suscipit a, interdum id",
        "tags": ["black-jack", "bender"],
        "answers": [
            {
                "id": 6,
                "text": "3D printing with lunar soil could revolutionize construction methods on the Moon.",
                "likes": 14,
                "is_correct": False
            }
        ]
    },
]

def index(request, *args,**kwarags):
    questions = Question.objects.new_questions()
    context = {}
    context["questions_page"] = paginate(questions,request,5)
    GetMembersTags(context)
    return render(request,'questions/index.html',context)

def question(request, *args,**kwarags):

    question = Question.objects.get(id=kwarags.get('id'))
    answers = Answer.objects.filter(question_id=kwarags.get('id'))
    
    context={
        "question": question
    }
    context["questions_page"] = paginate(answers,request,5)
    GetMembersTags(context)
    return render(request,'questions/question.html',context)

def hot_questions(request, *args,**kwarags):
    questions = Question.objects.get_hot_questions()
    context = {}
    GetMembersTags(context)
    context["questions_page"] = paginate(questions,request,5)
    return render(request,'questions/hot_questions.html',context)

def settings(request, *args,**kwarags):
    context={}
    GetMembersTags(context)
    return render(request,'questions/settings.html',context)

def tag(request,*args,**kwarags):
    tag_name = kwarags.get('tag_name')
    questions_page = Question.objects.get_tag_questions(tag_name)
    context = {
        "tag_name": tag_name,
    }
    context["questions_page"] = paginate(questions_page,request,5)
    GetMembersTags(context)
    return render(request,'questions/tag.html',context)

def ask(request, *args,**kwarags):
    context={}
    GetMembersTags(context)
    return render(request,'questions/ask.html',context)

def login(request, *args,**kwarags):
    context={}
    GetMembersTags(context)
    return render(request,'questions/login.html',context)

def signup(request, *args,**kwarags):
    context={}
    GetMembersTags(context)
    return render(request,'questions/signup.html',context)


def paginate(objects_list, request, per_page=6):
    paginator = Paginator(objects_list,per_page)
    page= request.GET.get("page",1)
    if not str(page).isdigit():
        page = 1
    data = paginator.get_page(page)
    return data


def GetMembersTags(context,request=None):
    q = Question.objects.get_hot_questions_parameters()[:6]
    p_t = []
    b_m = []
    for i in q:
        p_t += (i.tag_names)
        b_m.append(i.nickname)

    is_authenticated =True
    
    user_data = [
        {
            "Login": "dr_pepper",
            "Email": "dr.pepper@mail.ru", 
            "NickName": "Dr. Pepper"
        }
    ] 
    
    context["best_members"] = b_m
    context["popular_tags"] = p_t
    context["user_data"] = user_data
    context["is_authenticated"] = is_authenticated