from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from onlinecourse.models import Course, Lesson, Enrollment, Question, Choice


class Command(BaseCommand):
    help = 'Create demo users, a course with lessons, an assessment and an enrollment'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin@123')
            self.stdout.write(self.style.SUCCESS('Created superuser admin / admin@123'))

        if not User.objects.filter(username='student').exists():
            User.objects.create_user('student', 'student@example.com', 'student@123')
            self.stdout.write(self.style.SUCCESS('Created student student / student@123'))

        student = User.objects.get(username='student')

        course, created = Course.objects.get_or_create(
            name='Python Programming Basics',
            defaults={'description': 'Learn the fundamentals of Python programming with hands-on lessons and a mock exam.'},
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created course: ' + course.name))

        lessons = [
            ('Introduction to Python', 'Python is an interpreted, high-level language. In this lesson you install Python, run your first script and learn about indentation.'),
            ('Variables and Data Types', 'Learn how to create variables and work with numbers, strings, booleans and lists in Python.'),
            ('Control Flow: if, for, while', 'Use conditional statements and loops to control the flow of your Python programs.'),
            ('Functions and Modules', 'Define reusable functions, pass arguments and organize your code into modules and packages.'),
        ]
        for title, content in lessons:
            Lesson.objects.get_or_create(title=title, course=course, defaults={'content': content})

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
        lesson_list = list(Lesson.objects.filter(course=course).order_by('id'))
        for index, (question_text, choices) in enumerate(questions):
            question, q_created = Question.objects.get_or_create(
                question_text=question_text,
                lesson=lesson_list[index % len(lesson_list)],
            )
            if q_created:
                for choice_text, is_correct in choices:
                    Choice.objects.create(question=question, choice_text=choice_text, is_correct=is_correct)

        Enrollment.objects.get_or_create(enroll_user=student, course=course)

        self.stdout.write(self.style.SUCCESS(
            'Demo data ready: %d lessons, %d questions, student enrolled'
            % (Lesson.objects.filter(course=course).count(),
               Question.objects.filter(lesson__course=course).count())
        ))
