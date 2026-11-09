from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods

from core.pagination import paginate
from core.views import render_form
from .data import ANSWERS, QUESTIONS


@require_GET
def index(request):
    return render(request, "questions/index.html", {
        "page_obj": paginate(sorted(QUESTIONS, key=lambda item: item["id"], reverse=True), request, 20),
    })


@require_GET
def hot(request):
    return render(request, "questions/hot.html", {
        "page_obj": paginate(sorted(QUESTIONS, key=lambda item: item["rating"], reverse=True), request, 20),
    })


@require_GET
def tag(request, tag):
    questions = [item for item in QUESTIONS if tag in item["tags"]]
    questions.sort(key=lambda item: item["rating"], reverse=True)
    return render(request, "questions/tag.html", {
        "tag": tag, "page_obj": paginate(questions, request, 20),
    })


@require_http_methods(["GET", "POST"])
def question(request, question_id):
    question = next((item for item in QUESTIONS if item["id"] == question_id), None)
    if question is None:
        raise Http404("Вопрос не найден")
    answers = sorted(ANSWERS[question_id], key=lambda item: (-item["rating"], item["id"]))
    return render_form(request, "questions/question.html", question=question,
                       page_obj=paginate(answers, request, 30))


@require_http_methods(["GET", "POST"])
def ask(request):
    return render_form(request, "questions/ask.html")
