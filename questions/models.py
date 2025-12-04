from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.postgres.aggregates import ArrayAgg
from django.templatetags.static import static

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.get_queryset().order_by("-created_at")[:20]

    def get_hot_questions_parameters(self):
        return (
            self.get_queryset()
            .select_related("user_id", "user_id__userprofile")
            .annotate(
                tag_names=ArrayAgg("tags__name", distinct=True),
                nickname=models.F("user_id__userprofile__nickname"),
            )
            .order_by("-like_count")[:50]
        )

    def get_hot_questions(self):
        return self.get_queryset().order_by("-like_count")[:20]

    def get_tag_questions(self, tag):
        return self.filter(tags__name=tag).order_by("-created_at")

    def get_user_questions(self, user_nickname):
        return self.filter(user_id__userprofile__nickname=user_nickname).order_by(
            "-created_at"
        )


class Question(models.Model):
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["-created_at"]

    title = models.CharField(verbose_name="Заголовок", max_length=256)
    text = models.TextField(verbose_name="Текст", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано в")
    user_id = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, verbose_name="Пользователь", null=True
    )
    tags = models.ManyToManyField("questions.Tag", blank=True, verbose_name="Теги")

    like_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество лайков"
    )
    answer_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество ответов"
    )

    objects = QuestionManager()

    def __str__(self):
        return f"Question #{self.id} "

    def inc_answers(self):
        from django.db.models import F
        Question.objects.filter(id=self.id).update(answer_count=F('answer_count') + 1)
        self.refresh_from_db(fields=['answer_count'])


class AnswerManager(models.Manager):
    def old_answers(self):
        return self.order_by("created_at")


class Answer(models.Model):
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    user_id = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, verbose_name="Пользователь", null=True
    )
    question_id = models.ForeignKey(
        "questions.Question", on_delete=models.CASCADE, verbose_name="Вопрос"
    )
    text = models.TextField(verbose_name="Текст")
    is_correct = models.BooleanField(default=False, verbose_name="Правильность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создвно ы")
    like_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество лайков"
    )

    objects = AnswerManager()

    # def __str__(self):
    #     return f'#{self.id} "{self.name}"'


class Tag(models.Model):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    name = models.CharField(max_length=64, verbose_name="Название")

    def __str__(self):
        return f"{self.name}"


class UserProfile(models.Model):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    user = models.OneToOneField(
        "auth.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    avatar = models.ImageField(verbose_name="Аватарка",null=True,blank=True,)
    nickname = models.CharField(max_length=64, verbose_name="Ник")

    @property
    def avatar_url(self):
        if self.avatar and self.avatar.file:
            return self.avatar.url
        return static('questions/img/reviewsphoto.png')

    def __str__(self):
        return self.user.username


class QuestionLike(models.Model):

    user_id = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    question_id = models.ForeignKey(
        "questions.Question", on_delete=models.CASCADE, verbose_name="Вопрос"
    )

    class Meta:
        verbose_name = "Лайки вопроса"
        verbose_name_plural = "Лайк вопросов"
        constraints = [
            UniqueConstraint(
                fields=["user_id", "question_id"], name="unique_question_like"
            )
        ]


class AnswerLike(models.Model):

    user_id = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    answer_id = models.ForeignKey(
        "questions.Answer", on_delete=models.CASCADE, verbose_name="Ответ"
    )

    class Meta:
        verbose_name = "Лайк ответа"
        verbose_name_plural = "Лайки ответов"
        constraints = [
            UniqueConstraint(fields=["user_id", "answer_id"], name="unique_answer_like")
        ]
