from django.contrib import admin
from .models import Question, Answer, Tag, UserProfile, QuestionLike, AnswerLike


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
        "user_id",
        "like_count",
        "answer_count",
    )
    search_fields = (
        "title",
        "text",
    )
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    # raw_id_fields=['user_id']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question_id",
        "user_id",
        "is_correct",
        "created_at",
        "like_count",
    )
    search_fields = ("text",)
    list_filter = ("is_correct",)

    # raw_id_fields=['user_id','question_id']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "avatar")
    search_fields = ("user__username",)

    # raw_id_fields=['user_id']


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "question_id")

    # raw_id_fields=['user_id','question_id']


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "answer_id")

    # raw_id_fields=['user_id','answer_id']
