# OnlineCourse — Add a New Assessment Feature (Final Project)

A Django web application for an online course platform with a new **assessment / mock exam**
feature. Students enroll in a course, read its lessons, take a multiple-choice assessment and
receive an immediate score with a congratulations message.

## Features

- **Courses & Lessons** — each course shows its name, description and all related lessons on a
  Bootstrap-styled course details page.
- **Assessment (mock exam)** — each course can hold questions; every question has choices, one or
  more of which are correct. Students answer with checkboxes and submit the exam.
- **Automatic grading** — the `submit` view stores a `Submission`, the `show_exam_result` view
  calculates the score from each question's grade, shows a *Congratulations* message on a passing
  attempt (70% or more) and lists the full exam results.
- **Django Admin** — `QuestionInline` and `ChoiceInline` so questions and choices can be managed
  inline, with dedicated `QuestionAdmin` and `LessonAdmin` classes.

## Models

| Model | Purpose |
|-------|---------|
| `Instructor` | instructor profile linked to a Django user |
| `Learner` | learner profile linked to a Django user |
| `Course` | name, description, publication date and total enrollment |
| `Lesson` | title, order and content, belongs to a course |
| `Enrollment` | links a user to a course |
| `Question` | content, grade and course, with `is_get_score(selected_ids)` |
| `Choice` | content and `is_correct` flag, belongs to a question |
| `Submission` | an exam attempt linked to an `Enrollment`, many-to-many with `Choice` |

`admin.py` imports the seven model classes
(`Course, Lesson, Instructor, Learner, Question, Choice, Submission`) and implements
`QuestionInline`, `ChoiceInline`, `QuestionAdmin` and `LessonAdmin`.

## Key URLs

| URL | View |
|-----|------|
| `/` | `index` — course list |
| `/course/<course_id>/` | `course_details` — lessons + exam form |
| `/course/<course_id>/submit/` | `submit` — records the exam submission |
| `/course/<course_id>/submission/<submission_id>/result/` | `show_exam_result` — score and results |

## Run the project

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_demo     # optional demo data
python manage.py runserver
```

Then open http://127.0.0.1:8000/

### Demo accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin@123` |
| Student | `student` | `student@123` |

Admin site: http://127.0.0.1:8000/admin/

### Take the exam (demo flow)

1. Login as `student`.
2. Open **Course Details** for *Python Programming Basics*.
3. Select the correct answers for the 4 questions and click **Submit Exam**.
4. The result page shows *Congratulations! You passed the mock exam*, the score (100/100) and the
   full exam results.

## Screenshots

- [`screenshots/03-admin-site.png`](screenshots/03-admin-site.png) — Django admin site showing the
  **Authentication and Authorization** section and the **OnlineCourse** section with Choices,
  Courses, Instructors, Learners, Lessons, Questions and Submissions.
- [`screenshots/07-final.png`](screenshots/07-final.png) — Mock exam result with the
  *Congratulations* message, 100/100 score and exam results.

## Submission file map

| Task | File |
|------|------|
| 1 | `onlinecourse/models.py` — Question, Choice, Submission |
| 2 | `onlinecourse/admin.py` — seven imports, QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin |
| 3 | `screenshots/03-admin-site.png` |
| 4 | `onlinecourse/templates/onlinecourse/course_details_bootstrap.html` |
| 5 | `onlinecourse/views.py` — submit, show_exam_result |
| 6 | `onlinecourse/urls.py` — submit and result paths |
| 7 | `screenshots/07-final.png` |
