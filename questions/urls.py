from django.urls import path
from questions.views import (
    question,
    hot_questions,
    settings,
    tag,
    ask,
    login_view,
    signup,
    user,
    logout_view
)
from . import views

urlpatterns = [
    path("hot/", hot_questions, name="hot_questions"),
    path("<int:id>/", question, name="question"),
    path("settings/", settings, name="settings"),
    path("tag/<str:tag_name>/", tag, name="tag"),
    path("user/<str:user_nickname>/", user, name="user"),
    path("ask/", ask, name="ask"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup, name="signup"),
]
