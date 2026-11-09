from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def render_form(request, template, **context):
    if request.method == "POST":
        context["demo_notice"] = "Это макет формы: обработка и сохранение данных появятся в ДЗ4."
    return render(request, template, context)


@require_http_methods(["GET", "POST"])
def login(request):
    return render_form(request, "core/login.html", guest=True)


@require_http_methods(["GET", "POST"])
def signup(request):
    return render_form(request, "core/signup.html", guest=True)


@require_http_methods(["GET", "POST"])
def profile(request):
    return render_form(request, "core/profile.html")
