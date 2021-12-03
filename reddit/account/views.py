from django.shortcuts import render,redirect
from django.http import HttpResponse

from category.models import Category
from question_answer.models import Question,Answer

from user_profile.models import UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from comment.models import Comment
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def homePage(request):
    navigation_categories = Category.objects.filter(status=True).order_by('-id')[:5]
    categories = Category.objects.filter(status=True)
    questions = Question.objects.filter(status=True).order_by('-id')[:5]


    return render(request, 'home.html',{'navigation_categories':navigation_categories,
                                         'categories':categories,
                                         'questions':questions})
def categoryQuestion(request,category_id):
    navigation_categories = Category.objects.filter(status=True).order_by('-id')[:5]
    categories = Category.objects.filter(status=True)
    questions = Question.objects.filter(status=True,category_id=category_id)

    return render(request,'category-question.html',{
        'navigation_categories':navigation_categories,
        'categories':categories,
        'questions':questions,
    })
def QuestionDetails(request,question_id):
    navigation_categories = Category.objects.filter(status=True).order_by('-id')[:5]
    answersObjects=Answer.objects.filter(question_id=question_id)
    answers={}
    for key, answer in enumerate(answersObjects):
        comments=Comment.objects.filter(answer=answer)
        try:
            userProfileObject=UserProfile.objects.get(user=answer.user)
        except UserProfile.DoesNotExist:
            userProfileObject={}
        answers[key]={
            'answer':answer,
            'user_profile':userProfileObject,
            'comments':comments,
        }
    try:
        question=Question.objects.get(id=question_id)
    except Question.DoesNotExist:
          question= {}
    return render(request, 'question-details.html',{
        'navigation_categories':navigation_categories,
        'question':question,
        'answers':list(answers.values()),
    })
from datetime import datetime

def SaveComment(request):
    questionId = request.POST.get('question_id')
    answerId = request.POST.get('answer_id')
    comment = request.POST.get('comment')
    image = request.FILES.get('image')
    if comment:
        Comment.objects.create(
            answer_id=answerId,
            comments=comment,
            added_date=datetime.now(),
            user=request.user,
            image = image
        )
        messages.success(request, 'Comment added successfully')
    else:
        messages.error(request, 'Comment can not be empty')
    return redirect('QuestionDetails', question_id=questionId)
    
def UserRegistration(request):
    if request.method=='POST':
        firstName=request.POST.get('first_name')
        lastName=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirmPassword=request.POST.get('confirm_password')
        checkUsername=User.objects.filter(username=username)
        if checkUsername:
            messages.error(request,'username is already taken')
            return redirect('UserRegistration')
        
        else:
            if password == '':
                messages.error(request,'Password is required')
                return redirect('UserRegistration')
            elif confirmPassword == '':
                messages.error(request,'Confirm Password is required')
                return redirect('UserRegistration')
            
            
            elif password != confirmPassword:
                messages.error(request,'passwords does not matches')
                return redirect('UserRegistration')
            else:
                user=User.objects.create(
                    first_name=firstName,
                    last_name=lastName,
                    username=username,   
                )
                user.set_password(password)
                user.save()
                messages.success(request,'Congratulations Your Registration is Completed')
                return redirect('UserLogin')
                
    else:
       navigation_categories = Category.objects.filter(status=True).order_by('-id')[:5]
       return render(request, 'user-registration.html',{
        'navigation_categories':navigation_categories,})

def UserLogin(request):
    
    if request.method== 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfull")
            return redirect('homePage')
        else:
            messages.error(request,'Invalid UserName or password')
            return redirect('UserLogin')

    else:
        navigation_categories = Category.objects.filter(status=True).order_by('-id')[:5]

        return render(request,'user-login.html',{
            'navigation_categories':navigation_categories,})
def userProfile(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        mobileNo = request.POST.get('mobile_no')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm_password')
        profilePicture = request.FILES.get('profile_picture')
        userProfileObject = UserProfile.objects.get(user=request.user)
        if password != "" and confirmPassword != "":
            if password == confirmPassword:
                request.user.set_password(password)
            else:
                messages.error(request, 'Password does not match with the confirm password')
                return redirect('userProfile')
        user = request.user
        
        userProfileObject.address = address
        userProfileObject.profile_picture = profilePicture
        messages.success(request, 'Profile is updated')
        userProfileObject.save()
        request.user.first_name = firstName
        request.user.last_name = lastName
        request.user.email = email
        userProfileObject.mobile_no = mobileNo
        request.user.save()
        login(request, user)
        return redirect('userProfile')
    else:
        navigation_categories = Category.objects.filter(status=True).order_by('-id')[:5]
        userProfileObject,_ = UserProfile.objects.get_or_create(user=request.user)
        return render(request, 'user-profile.html', {
            'navigation_categories':navigation_categories,
            'userProfile' : userProfileObject,
        })
        
def logout_view(request):
    logout(request)
    messages.success(request,'User LOgged Out Successfully')
    return redirect('homePage')