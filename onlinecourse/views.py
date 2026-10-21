from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


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
        else:
            return render(request, 'onlinecourse/login.html', {'message': 'Invalid username or password'})
    return render(request, 'onlinecourse/login.html')


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment, created = Enrollment.objects.get_or_create(
        enroll_user=request.user, course=course
    )
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


@login_required
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = Lesson.objects.filter(course=course)
    questions = Question.objects.filter(lesson__course=course)
    enrollment = Enrollment.objects.filter(enroll_user=request.user, course=course).first()
    context = {
        'course': course,
        'lesson_list': lessons,
        'question_list': questions,
        'enrollment': enrollment,
    }
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, enroll_user=request.user, course=course)
    submission = Submission.objects.create(enroll=enrollment)
    for key, values in request.POST.lists():
        if key.startswith('choice'):
            for choice_id in values:
                submission.choices.add(Choice.objects.get(pk=choice_id))
    submission.save()
    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(submission.id,))
    )


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    course = submission.enroll.course
    questions = Question.objects.filter(lesson__course=course)
    selected_choices = submission.choices.all()
    total_questions = submission.get_total_questions()
    correct_answers = submission.get_correct_answers()
    score = submission.get_score()
    context = {
        'submission': submission,
        'course': course,
        'question_list': questions,
        'choices': selected_choices,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score': score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
