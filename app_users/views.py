from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from curriculum.checkComment.checkComment import checkText
from curriculum.checkComment.classificationText import checkNegComment
from curriculum.forms import CommentForm, ReplyForm
from .forms import UserForm, UserProfileInfoForm, ProfileUpdateForm, UserUpdateForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.generic import TemplateView, FormView
from curriculum.views import Standard
from curriculum.models import Courses
from .models import UserProfileInfo, News, HonoraryTeachers
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views.generic import ListView, DetailView


# Create your views here.

def index(req):
    return HttpResponse('hello world')


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'app_users/registration.html',
                  {'registered': registered,
                   'user_form': user_form,
                   'profile_form': profile_form,
                   'valid': user_form.is_valid()})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("username yoki parol xato")
            # return HttpResponseRedirect(reverse('register'))

    else:
        return render(request, 'app_users/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class HomeView(TemplateView):
    template_name = 'app_users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        standards = Standard.objects.all()
        teachers = UserProfileInfo.objects.filter(user_type='teacher')
        user_profiles = UserProfileInfo.objects.all()
        hTeachers = HonoraryTeachers.objects.all()
        news = News.objects.all()
        news = list(news)
        news_list = []

        ul_news = False
        if news:
            ul_news = news[0]
            news.remove(news[0])

            if len(news) > 0:
                k = 0
                for i in range(len(news)):
                    if k == 4:
                        break
                    else:
                        news_list.append(news[i])
                        k += 1

        courses = Courses.objects.all()

        context['standards'] = standards
        context['teachers'] = teachers
        context['profiles'] = user_profiles
        context['news'] = news_list
        context['ul_news'] = ul_news
        context['courses'] = courses
        context['honorary'] = hTeachers
        return context


def about_school_view(request):
    teachers = HonoraryTeachers.objects.all()
    return render(request, 'app_users/about_school.html', {'teachers': teachers})


def about_us_view(request):
    return render(request, 'app_users/about_us.html')


def news_view(request):
    news = News.objects.all()
    return render(request, 'app_users/news.html', {'news': news})


class NewDetailView(DetailView, FormView):
    model = News
    template_name = 'app_users/new_detail.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form.is_valid():
            comment = form.save(commit=False)
            body = comment.body if form_name == 'form' else comment.reply_body
            typeComment = checkText(body.lower())['label']
            comment.type = typeComment
            if typeComment == 'negative':
                field = checkNegComment(body.lower())['label']
                comment.field = field
            # comment.save()

            if form_name == 'form':
                print("comment form is returned")
                return self.form_valid(form)
            elif form_name == 'form2':
                print("reply form is returned")
                return self.form2_valid(form)

        return self.form_invalid(form)


def profile(request):
    return render(request, 'app_users/profile.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!

            return HttpResponse("<h1>Parol o'zgardi!</h1>")
        else:
            messages.error(request, "Parollarni to'g'ri kiriting.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app_users/change_password.html', {
        'form': form
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofileinfo)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Yangilandi!')
            return redirect('edit_profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.userprofileinfo)
        u_form = UserUpdateForm(instance=request.user)

    context = {'p_form': p_form, 'u_form': u_form}
    return render(request, 'app_users/edit_profile.html', context)
