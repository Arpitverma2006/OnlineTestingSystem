
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from OTS.models import *
import random
import datetime

def welcome(request):
    template=loader.get_template('welcome.html')
    return HttpResponse(template.render())

def candidateRegistrationForm(request):
    res=render(request,'registration_form.html')
    return res

def candidateRegistration(request):
    if request.method=='POST':
        username=request.POST['username']
        # check if the user already exists
        if len(Candidate.objects.filter(username=username)):
            userStatus=1
        else:
            
            candiate=Candidate()
            candiate.username=username
            candiate.password=request.POST['password']
            candiate.name=request.POST['name']
            candiate.save()
            userStatus=2
    else:
        userStatus=3 #Request method is not POST
    context = {
        'user-status':userStatus
    }
    res=render(request,'registration.html',context)
    return res

def loginView(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        candidate=Candidate.objects.filter(username=username,password=password)
        if len(candidate)==0:
            loginError='Invalid Username or Password'
            res=render(request,'login.html',{'loginError':loginError})
        else:
            #login Success
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name
            res=HttpResponseRedirect("home")
    else:
        res=render(request,'login.html')
    return res

def candidateHome(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    else:
        res=render(request,'home.html')
    return res

# def testPaper(request):
#     if 'name' not in request.session.keys():
#         res=HttpResponseRedirect("login")
#     #fetch question from database table
#     n=request.GET.get('n')
#     question_pool=list(Question.objects.all())
#     random.shuffle(question_pool)
#     question_list=question_pool[:int(n)]
#     context={'questions':question_list, 'test_duration': 30}  # 30 minutes
#     return render(request, 'test_paper.html', context)

# def calculateTestResult(request):
#     if 'name' not in request.session.keys():
#         return HttpResponseRedirect("login")
#     total_attempt = 0
#     total_right = 0
#     total_wrong = 0
#     qid_list = []
#     for k in request.POST:
#         if k.startswith('qno'):
#             qid_list.append(int(request.POST[k]))
#     for n in qid_list:
#         question = Question.objects.get(qid=n)
#         try:
#             if question.ans == request.POST['q' + str(n)]:
#                 total_right += 1
#             else:
#                 total_wrong += 1
#         except:
#             pass
#     points = (total_right * 10) - (total_wrong * 5) if qid_list else 0
#     # store result in result table
#     # store result in result table
#     attempt = len(qid_list)
#     right = total_right
#     wrong = total_wrong
#     points = (total_right * 10) - (total_wrong * 5) if qid_list else 0

#     try:
#         result = Result.objects.filter(username=request.session['username']).latest('date')
#         result.attempt = attempt
#         result.right = right
#         result.wrong = wrong
#         result.points = points
#         result.date = datetime.datetime.now().date()
#         result.time = datetime.datetime.now().time()
#         result.save()
#     except Result.DoesNotExist:
#         result = Result()
#         result.username = Candidate.objects.get(username=request.session['username'])
#         result.attempt = attempt
#         result.right = right
#         result.wrong = wrong
#         result.points = points
#         result.date = datetime.datetime.now().date()
#         result.time = datetime.datetime.now().time()
#         result.save()

#     return render(request, 'show_result.html', {
#         'result': result,
#         'attempt': attempt,
#         'right': right,
#         'wrong': wrong,
#         'points': points,
#     })

# import datetime
# import random
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Question, Result, Candidate

def testPaper(request):
    if 'username' not in request.session:
        return HttpResponseRedirect("login")

    n = request.GET.get('n', 10)  # Default to 10 questions if not specified
    try:
        n = int(n)
    except ValueError:
        n = 10  # Fallback in case of invalid input

    # Fetch and shuffle questions
    question_pool = list(Question.objects.all())
    random.shuffle(question_pool)
    question_list = question_pool[:n]

    context = {
        'questions': question_list,
        'test_duration': 30,  # 30 minutes
    }
    return render(request, 'test_paper.html', context)

def calculateTestResult(request):
    if 'username' not in request.session:
        return HttpResponseRedirect("login")

    username = request.session['username']
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    qid_list = []

    print("Processing test results for user:", username)  # Debugging step

    # Collect all question IDs from the POST request
    for key in request.POST:
        if key.startswith('qno'):
            qid_list.append(int(request.POST[key]))

    print("Questions attempted:", qid_list)  # Debugging step

    # Processing user answers
    for qid in qid_list:
        try:
            question = Question.objects.get(qid=qid)
            user_answer = request.POST.get(f'q{qid}', None)  # Safely get the user's answer
            print(f"QID: {qid}, Correct Answer: {question.ans}, User Answer: {user_answer}")  # Debugging

            if user_answer is not None:
                total_attempt += 1
                if user_answer == question.ans:
                    total_right += 1
                else:
                    total_wrong += 1
        except Question.DoesNotExist:
            print(f"Question ID {qid} not found in database!")  # Debugging step
            continue

    # Calculate points: +10 for correct, -5 for wrong answers
    points = (total_right * 10) - (total_wrong * 5) if total_attempt else 0
    print(f"Attempts: {total_attempt}, Right: {total_right}, Wrong: {total_wrong}, Points: {points}")  # Debugging step

    # Fetch candidate object
    try:
        candidate = Candidate.objects.get(username=username)
    except Candidate.DoesNotExist:
        print("Candidate not found in the database!")  # Debugging
        return HttpResponseRedirect("login")

    # ✅ Always create a new result for every test attempt
    result = Result.objects.create(
        username=candidate,
        attempt=total_attempt,
        right=total_right,
        wrong=total_wrong,
        points=points,
        date=datetime.date.today(),
        time=datetime.datetime.now().time(),
    )

    print("Result saved successfully!")  # Debugging step

    return render(request, 'show_result.html', {
        'result': result,
        'attempt': total_attempt,
        'right': total_right,
        'wrong': total_wrong,
        'points': points,
    })




def testResultHistory(request):
    if 'name' not in request.session.keys():
        return HttpResponseRedirect("login")
    
    try:
        candidate = Candidate.objects.get(username=request.session['username'])
    except Candidate.DoesNotExist:
        return HttpResponseRedirect("login")  # Redirect if candidate is not found
    
    results = Result.objects.filter(username=candidate)
    
    context = {'candidate': candidate, 'results': results}
    return render(request, 'candidate_history.html', context)

# def testResultHistory(request):
#     if 'name' not in request.session.keys():
#         return HttpResponseRedirect("login")
    
#     try:
#         candidate = Candidate.objects.get(username=request.session['username'])
#     except Candidate.DoesNotExist:
#         return HttpResponseRedirect("login")  # Redirect if candidate is not found
    
#     results = Result.objects.filter(username=candidate)
    
#     context = {'candidate': candidate, 'results': results}
#     return render(request, 'candidate_history.html', context)

def showTestResult(request):
     if 'name' not in request.session.keys():
        return HttpResponseRedirect("login")
        
     #fetch latest result from Result Table
     result=Result.objects.filter(username_id=request.session['username']).latest('date')
     context={'result':result}
     return render(request,'show_result.html',context)

def logoutView(request):
    if 'name'  in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect("login")