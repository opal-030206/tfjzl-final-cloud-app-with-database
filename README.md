# OnlineCourse — Add a New Assessment Feature (Final Project)

A Django web application for an online course platform with a new **assessment / mock exam**
feature. Students enroll in a course, read its lessons, take a multiple-choice assessment and
receive an immediate score with a congratulations message.

## Features

- **Courses & Lessons** — each course shows its name, description and all related lessons on a
  Bootstrap-styled course details page.
- **Assessment (mock exam)** — each lesson can hold questions; every question has choices, one of
  which is correct. Students answer with radio buttons and submit the exam.
- **Automatic grading** — the `submit` view stores a `Submission`, the `show_exam_result` view
  calculates the score, shows a *Congratulations* message on success and lists the exam results.
- **Django Admin** — `QuestionInline` inside `LessonAdmin` and `ChoiceInline` inside
  `QuestionAdmin` so questions and choices can be managed inline.

## Models

| Model | Purpose |
|-------|---------|
| `Course` | name + description |
| `Lesson` | title + content, belongs to a course |
| `Enrollment` | links a user to a course |
| `Question` | question text, belongs to a lesson |
| `Choice` | choice text + `is_correct` flag, belongs to a question |
| `Submission` | a student's exam attempt; many-to-many with `Choice`, computes the score |

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
3. Answer the 4 questions and click **Submit Exam**.
4. The result page shows *Congratulations! You passed the mock exam*, the score (100%) and the
   full exam results.

## Screenshots

- [`screenshots/03-admin-site.png`](screenshots/03-admin-site.png) — Django admin site showing the
  **Authentication and Authorization** section and the **OnlineCourse** section.
- [`screenshots/07-final.png`](screenshots/07-final.png) — Mock exam result with the
  *Congratulations* message, 100% score and exam results.

## Key URLs

| URL | View |
|-----|------|
| `/` | course list |
| `/course/<id>/` | course details (lessons + exam form) |
| `/course/<id>/submit/` | `submit` — records the exam submission |
| `/course/<submission_id>/result/` | `show_exam_result` — shows score and results |
