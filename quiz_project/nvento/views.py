from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from operator import itemgetter
from .models import *

class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class QuizCategory(View):
    def get(self, request):
        quiz = Quiz.objects.all()

        for item in quiz:
         
            print(item.thumbnailUrl) 

        items_per_page = 3
        paginator = Paginator(quiz, items_per_page)

        page = request.GET.get('page')

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        return render(request,  'quiz_category.html', {'quiz_count': len(quiz),'objects': objects, 'paginator': paginator, 'page_obj': objects})
    
class Profile(View):
    def get(self, request):
        user = request.user
        return render(request, 'profile.html', {'user':user})
    
class QuizView(View):
    def get(self, request, category):
        user = request.user

        quiz = Quiz.objects.get(title=category)
        questions = Question.objects.filter(quiz=quiz)

        print(questions)

        context = {
            'user':user,
            'category': category,
            'questions':questions,
            }

        return render(request, 'quiz.html', context)

class QuizScore(View):
    def get(self, request, category=None):
        return render(request, 'your_quiz_template.html', {'category': category})

    def post(self, request, category=None):
        score = 0

        for question_id, answer_id in request.POST.items():
            if question_id.startswith('question_'):
                question_id = question_id.replace('question_', '')
                try:
                    question = Question.objects.get(pk=question_id)
                    selected_answer = Answer.objects.get(pk=answer_id)
                    correct_answer = question.answer_set.get(is_correct=True)

                    if selected_answer == correct_answer:
                        score += 1

                except (Question.DoesNotExist, Answer.DoesNotExist):
                    pass
                
        user = request.user 
        quiz = Quiz.objects.get(title=category)
        Score.objects.create(user=user, quiz=quiz, score=score)

        return redirect('my_scores', category=category) 

class TopScorer(View):
    def get(self, request, category):
        try:
            quiz = Quiz.objects.get(title=category)

            all_scores = Score.objects.filter(quiz=quiz)

            user_scores = {}
            for score in all_scores:
                user_id = score.user.id
                current_score = score.score
                college = score.user.userprofile.college
                program = score.user.userprofile.program

                if user_id not in user_scores or current_score > user_scores[user_id]['score']:
                    user_scores[user_id] = {
                        'user': score.user.username,
                        'score': current_score,
                        'college': college,
                        'program': program
                    }

            sorted_scores = sorted(user_scores.values(), key=itemgetter('score'), reverse=True)

            context = {
                'category': category,
                'top_scorers': sorted_scores
            }

            return render(request, 'top_scorer.html', context)
        
        except Quiz.DoesNotExist:
            return render(request, 'top_scorer.html', {'category': category})


class MyScores(View):
    def get(self, request, category):
        try:
            user = request.user
            quiz = Quiz.objects.get(title=category)

            all_scores = Score.objects.filter(user=user, quiz=quiz)

            print(all_scores)

            user_scores = []
            for score in all_scores:
                user_id = score.user.id
                current_score = score.score
                college = score.user.userprofile.college
                program = score.user.userprofile.program

            
                user_scores.append({
                'user_id': user_id,
                'user': score.user.username,
                'score': current_score,
                'college': college,
                'program': program
                })

            sorted_scores = sorted(user_scores, key=lambda item: item['score'], reverse=True)

            context = {
                'category': category,
                'scores': sorted_scores
            }

            return render(request, 'your_scores.html', context)
        
        except Quiz.DoesNotExist:
            return render(request, 'your_scores.html', {'category': category})
        
class SaveProfileChanges(View):
    def post(self, request):
        if request.method == "POST":
            name  = request.POST['name']
            college = request.POST['college']
            program = request.POST['program']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['pass']

            user = request.user

            if user is not None:
                if username != "":
                    user.username = username
                if name != "":
                    user.userprofile.name = name
                if college != "":
                    user.userprofile.college = college
                if program != "":
                    user.userprofile.program = program
                if email != "":
                    user.userprofile.email = email
                if password != "":
                    user.password = password

                user.save()

                messages.success(request, ("Profile update successfull!"))
                return redirect('profile')
            else:
                messages.success(request, ("There was an error, please try again..."))
                return redirect('profile')
                
        else:
            return render(request, "profile.html")
