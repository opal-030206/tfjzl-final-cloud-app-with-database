from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission


def index(request):
    course_list = Course.objects.all()
    context = {'course_list': course_list}
    return render(request, 'onlinecourse/course_list_bootstrap.html', context)


def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        return render(request, 'onlinecourse/login.html',
                      {'message': 'Invalid username or password'})
    return render(request, 'onlinecourse/login.html')


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(
        reverse('onlinecourse:course_details', args=(course.id,))
    )


@login_required
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(
        user=request.user, course=course
    ).first()
    course.is_enrolled = enrollment is not None
    context = {
        'course': course,
        'enrollment': enrollment,
        'lesson_list': course.lesson_set.all(),
        'question_list': course.question_set.all(),
    }
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)


def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            submitted_answers.append(int(value))
    return submitted_answers


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    return HttpResponseRedirect(
        reverse(
            'onlinecourse:show_exam_result',
            args=(course_id, submission.id),
        )
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission, id=submission_id, enrollment__course=course
    )
    choices = submission.choices.all()
    selected_ids = list(choices.values_list('id', flat=True))
    questions = course.question_set.all()

    total_score = 0
    for question in questions:
        if question.is_get_score(selected_ids):
            total_score += question.grade

    total_grade = sum(question.grade for question in questions)
    score = int(total_score * 100 / total_grade) if total_grade else 0

    context = {
        'course': course,
        'submission': submission,
        'choices': choices,
        'question_list': questions,
        'grade': total_score,
        'total_grade': total_grade,
        'score': score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
