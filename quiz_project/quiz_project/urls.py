from django.contrib import admin
from django.urls import path, include
from nvento.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('login/', include('login.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', include('register.urls')),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('top_scorer/<str:category>/', TopScorer.as_view(), name='top_scorer'),
    path('my_scores/<str:category>/', MyScores.as_view(), name='my_scores'),
    path('quiz/', QuizCategory.as_view(), name='quiz'),
    path('quiz/<str:category>/', QuizView.as_view(), name='quiz'),
    path('quiz_score/', QuizScore.as_view(), name='quiz_score'),
    path('quiz_score/<str:category>/', QuizScore.as_view(), name='quiz_score'),
    path('save_profile_changes', SaveProfileChanges.as_view(), name='save_profile_changes'),

]
