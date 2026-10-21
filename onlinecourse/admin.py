from django.contrib import admin
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'lesson', 'get_correct_choice')
    list_filter = ['lesson']
    search_fields = ['question_text']
    inlines = [ChoiceInline]

    def get_correct_choice(self, obj):
        correct = obj.get_choices().filter(is_correct=True)
        if correct:
            return correct[0].choice_text
        return "No correct choice defined"

    get_correct_choice.short_description = 'Correct choice'


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'content')
    list_filter = ['course']
    search_fields = ['title', 'content']
    inlines = [QuestionInline]


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Enrollment)
admin.site.register(Submission)
