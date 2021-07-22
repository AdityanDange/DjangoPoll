from django.urls import path
from django.urls.conf import include
from django.contrib.auth import views as auth_views
from . import views
from polls.forms import LoginForm
from django.contrib.auth.decorators import login_required

app_name = 'polls'
urlpatterns = [
    path('', login_required(views.IndexView.as_view()), name='index'),
    path('<int:pk>/', login_required(views.DetailView.as_view()), name='detail'),
    path('<int:pk>/results/', login_required(views.ResultsView.as_view()), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]