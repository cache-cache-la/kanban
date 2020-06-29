from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView
from .forms import UserForm, ListForm, CardForm
from .mixins import OnlyYouMixin
from . models import List, Card

# トップページ
def index(request):
    return render(request, "kanban/index.html")

# サインアップ完了
@login_required
def home(request):
    return render(request, "kanban/home.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("kanban:home")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'kanban/signup.html', context)

# ユーザー詳細
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "kanban/users/detail.html"

# ユーザー編集
class UserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    template_name = "kanban/users/update.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('kanban:users_detail', pk=self.kwargs['pk'])

# リスト作成
class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    template_name = "kanban/lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:lists_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# リスト閲覧
class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = "kanban/lists/list.html"

# リスト詳細
class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "kanban/lists/detail.html"

# リスト編集
class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    template_name = "kanban/lists/update.html"
    form_class = ListForm

    def get_success_url(self):
        return resolve_url('kanban:lists_detail', pk=self.kwargs['pk'])

# リスト削除
class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = "kanban/lists/delete.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:lists_list")

# カード作成
class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "kanban/cards/create.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:cards_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# カード閲覧
class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "kanban/cards/list.html"


class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "kanban/cards/detail.html"

