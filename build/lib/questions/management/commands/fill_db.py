from django.core.management.base import BaseCommand
from questions.models import (
    Question,
    Answer,
    Tag,
    UserProfile,
    QuestionLike,
    AnswerLike,
)
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count
import random


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("Deleting old data...")

        User.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Tag.objects.all().delete()
        UserProfile.objects.all().delete()
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()

        ratio = options["ratio"]
        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        self.stdout.write(f"ratio = {ratio}")

        # USERS
        self.stdout.write("Creating users...")
        users = [
            User(username=f"user{i}", email=f"user{i}@mail.ru")
            for i in range(num_users)
        ]

        User.objects.bulk_create(users, batch_size=5000)
        users = list(User.objects.all())

        # ------------------ UserProfile ----------------
        self.stdout.write("Creating profiles...")
        profiles = [
            UserProfile(
                user=user,
                nickname=f"nick_{user.username}",
                avatar="avatars/reviewsphoto.png",
            )
            for user in users
        ]
        UserProfile.objects.bulk_create(profiles, batch_size=5000)

        # TAGS
        self.stdout.write("Creating tags...")
        tags = [Tag(name=f"tag_{i}") for i in range(num_tags)]
        Tag.objects.bulk_create(tags, batch_size=5000)
        tags = list(Tag.objects.all())

        # QUESTIONS
        self.stdout.write("Creating questions...")

        questions = [
            Question(
                title=f"Question {i} ?",
                text=f"Text of question {i} Etiam posuere quam ac quam. Maecenas aliquet accumsan leo. Nullam dapibus fermentum ipsum. Etiam quis quam. Integer lacinia. Nulla est. Nulla turpis magna, cursus sit amet, suscipit a, interdum id?",
                user_id=users[i % num_users],
            )
            for i in range(num_questions)
        ]
        Question.objects.bulk_create(questions, batch_size=5000)
        questions = list(Question.objects.all())

        self.stdout.write("Assigning tags to questions...")

        for i, q in enumerate(questions):
            num_to_add = random.randint(1, 3)
            for j in range(num_to_add):
                tag_to_add = tags[(i + j) % num_tags]
                q.tags.add(tag_to_add)

        # ANSWERS
        self.stdout.write("Creating answers...")
        answers = [
            Answer(
                text=f"Answer text {i}",
                user_id=users[i % num_users],
                question_id=questions[i % num_questions],
            )
            for i in range(num_answers)
        ]
        Answer.objects.bulk_create(answers, batch_size=5000)
        answers = list(Answer.objects.all())

        # LIKES
        self.stdout.write("Creating likes...")

        # Половина лайков — вопросам, половина — ответам
        num_question_likes = num_likes // 2
        num_answer_likes = num_likes - num_question_likes

        # ----------- Лайки вопросов -----------
        popular_share = 0.1  # 10% вопросов считаем популярными
        num_popular_questions = max(1, int(len(questions) * popular_share))
        popular_questions = random.sample(questions, num_popular_questions)

        qlikes = []
        for _ in range(num_question_likes):
            user = random.choice(users)

            # 70% — лайкаем популярный вопрос, 30% — любой другой
            if random.random() < 0.7:
                question = random.choice(popular_questions)
            else:
                question = random.choice(questions)

            # избегаем лайка своего же вопроса
            if question.user_id == user.id:
                continue

            qlikes.append(
                QuestionLike(
                    user_id=user,  # можно передавать сам объект User
                    question_id=question,
                )
            )

        QuestionLike.objects.bulk_create(qlikes, batch_size=5000, ignore_conflicts=True)

        # ----------- Лайки ответов -----------
        # Тут логика другая: каждый пользователь лайкает случайное число ответов
        alikes = []
        max_likes_per_user = max(1, num_answer_likes // max(1, num_users))

        for user in users:
            # случайное число лайков от 0 до max_likes_per_user
            likes_for_user = random.randint(0, max_likes_per_user)
            for _ in range(likes_for_user):
                answer = random.choice(answers)

                # избегаем лайка своего ответа
                if answer.user_id == user.id:
                    continue

                alikes.append(AnswerLike(user_id=user, answer_id=answer))

        # если в итоге лайков чуть больше, чем хотели — обрежем список
        if len(alikes) > num_answer_likes:
            alikes = alikes[:num_answer_likes]

        AnswerLike.objects.bulk_create(alikes, batch_size=5000, ignore_conflicts=True)

        # ========== Обновляем счётчики ==========

        self.stdout.write("Updating like_count and answer_count fields...")

        batch_size = 10000

        # Обновляем like_count у вопросов
        q_like_counts = QuestionLike.objects.values("question_id").annotate(
            count=Count("pk")
        )
        questions_to_update = []
        for entry in q_like_counts.iterator(chunk_size=batch_size):
            questions_to_update.append(
                Question(id=entry["question_id"], like_count=entry["count"])
            )
        with transaction.atomic():
            for i in range(0, len(questions_to_update), batch_size):
                Question.objects.bulk_update(
                    questions_to_update[i : i + batch_size], ["like_count"]
                )

        # Обновляем answer_count у вопросов
        ans_counts = Answer.objects.values("question_id").annotate(count=Count("pk"))
        questions_to_update = []
        for entry in ans_counts.iterator(chunk_size=batch_size):
            questions_to_update.append(
                Question(id=entry["question_id"], answer_count=entry["count"])
            )
        with transaction.atomic():
            for i in range(0, len(questions_to_update), batch_size):
                Question.objects.bulk_update(
                    questions_to_update[i : i + batch_size], ["answer_count"]
                )

        # Обновляем like_count у ответов
        a_like_counts = AnswerLike.objects.values("answer_id").annotate(
            count=Count("pk")
        )
        answers_to_update = []
        for entry in a_like_counts.iterator(chunk_size=batch_size):
            answers_to_update.append(
                Answer(id=entry["answer_id"], like_count=entry["count"])
            )
        with transaction.atomic():
            for i in range(0, len(answers_to_update), batch_size):
                Answer.objects.bulk_update(
                    answers_to_update[i : i + batch_size], ["like_count"]
                )

        self.stdout.write(
            self.style.SUCCESS("DB filled and counters updated successfully!")
        )

        # ================================================================
        # ================================================================
        # ================================================================

        self.stdout.write(self.style.SUCCESS("DB filled successfully!"))
        self.stdout.write(
            self.style.SUCCESS(
                f"{num_users} users\n"
                f"{num_questions} questions\n"
                f"{num_answers} answers\n"
                f"{num_tags} tags\n"
                f"{num_likes} likes total"
            )
        )
