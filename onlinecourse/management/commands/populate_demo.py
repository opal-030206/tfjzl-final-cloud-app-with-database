from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from onlinecourse.models import (
    Course, Lesson, Enrollment, Instructor, Learner, Question, Choice
)


class Command(BaseCommand):
    help = 'Create demo users, a course with lessons, an assessment and an enrollment'

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True},
        )
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('admin@123')
        admin.save()

        student, _ = User.objects.get_or_create(
            username='student',
            defaults={'email': 'student@example.com'},
        )
        student.set_password('student@123')
        student.save()

        instructor, _ = Instructor.objects.get_or_create(
            user=admin, defaults={'full_time': True, 'total_learners': 1}
        )
        Learner.objects.get_or_create(
            user=student, defaults={'occupation': Learner.STUDENT}
        )

        course, _ = Course.objects.get_or_create(
            name='Python Programming Basics',
            defaults={
                'description': 'Learn the fundamentals of Python programming with hands-on lessons and a mock exam.',
                'pub_date': timezone.now().date(),
                'total_enrollment': 1,
            },
        )
        course.instructors.add(instructor)
        course.total_enrollment = 1
        course.save()

        lessons = [
            ('Introduction to Python',
             'Python is an interpreted, high-level language. In this lesson you install Python, run your first script and learn about indentation.'),
            ('Variables and Data Types',
             'Learn how to create variables and work with numbers, strings, booleans and lists in Python.'),
            ('Control Flow: if, for, while',
             'Use conditional statements and loops to control the flow of your Python programs.'),
            ('Functions and Modules',
             'Define reusable functions, pass arguments and organize your code into modules and packages.'),
        ]
        for order, (title, content) in enumerate(lessons, start=1):
            Lesson.objects.get_or_create(
                title=title,
                course=course,
                defaults={'content': content, 'order': order},
            )

        questions = [
            ('Which keyword is used to define a function in Python?', [
                ('def', True), ('func', False), ('function', False)]),
            ('Which of the following is a valid Python data type?', [
                ('integer', False), ('int', True), ('number', False)]),
            ('Which statement is used for conditional branching in Python?', [
                ('if', True), ('when', False), ('switch', False)]),
            ('What symbol starts a single line comment in Python?', [
                ('#', True), ('//', False), ('<!--', False)]),
        ]
        for question_text, choices in questions:
            question, q_created = Question.objects.get_or_create(
                content=question_text,
                course=course,
                defaults={'grade': 25},
            )
            if q_created:
                for choice_text, is_correct in choices:
                    Choice.objects.create(
                        question=question,
                        content=choice_text,
                        is_correct=is_correct,
                    )

        Enrollment.objects.get_or_create(user=student, course=course)

        self.stdout.write(self.style.SUCCESS(
            'Demo data ready: %d lessons, %d questions, student enrolled'
            % (course.lesson_set.count(), course.question_set.count())
        ))
