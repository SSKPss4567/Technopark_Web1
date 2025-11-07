from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
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
    paginator=Paginator(QUESTIONS,per_page=3)
    page=request.GET.get('page',1)

    if not str(page).isdigit():
        page = 1

    questions_page=paginator.page(page)
    context={"questions_page":questions_page}
    GetMembersTags(context)
    return render(request,'questions/index.html',context)

def question(request, *args,**kwarags):
    question = QUESTIONS[kwarags.get('id')]
    answers = question['answers']
    
    paginator=Paginator(answers,per_page=2)
    page=request.GET.get('page',1)
    answers_page=paginator.page(page)

    context={
        "questions_page":answers_page,
        "question": question
    }
    GetMembersTags(context)
    return render(request,'questions/question.html',context)

def hot_questions(request, *args,**kwarags):
    paginator=Paginator(QUESTIONS[::-1],per_page=3)
    page=request.GET.get('page',1)
    questions_page=paginator.page(page)
    context={"questions_page":questions_page}
    GetMembersTags(context)
    return render(request,'questions/hot_questions.html',context)

def settings(request, *args,**kwarags):
    context={}
    GetMembersTags(context)
    return render(request,'questions/settings.html',context)

def tag(request,*args,**kwarags):
    tag_name = kwarags.get('tag_name')
    tagged_questions = [q for q in QUESTIONS if tag_name in  q["tags"]]
    
    paginator=Paginator(tagged_questions,per_page=3)
    page=request.GET.get('page',1)
    questions_page=paginator.page(page)

    context = {
        "questions_page": questions_page,
        "tag_name": tag_name,
    }
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

def GetMembersTags(context,request=None):
    p_t = ["python",
           "TechnoPark",
           "MYSQL",
           "Mail.ru",
           "Firefox",
           "python",
           "TechnoPark",
           "black-jack",
           "bender",
           ]
    b_m = ["Mr. Freeman",
        "Dr. House",
        "Bender",
        "Queen Victoria",
        "V. Pupkin"
        ]
    
    user_data = [
        {
            "Login": "dr_pepper",
            "Email": "dr.pepper@mail.ru", 
            "NickName": "Dr. Pepper"
        }
    ]   

    is_authenticated =True
 
    context["best_members"] = b_m
    context["popular_tags"] = p_t
    context["user_data"] = user_data
    context["is_authenticated"] = is_authenticated