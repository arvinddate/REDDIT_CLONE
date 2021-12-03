from django.urls import path
from . import views
urlpatterns = [
    path('',views.homePage,name='homePage'),
    path('category/<int:category_id>',views.categoryQuestion,name='categoryQuestion'),
    path('question/<int:question_id>',views.QuestionDetails,name='QuestionDetails'),
    path('save-comment', views.SaveComment, name="SaveComment"),
    path('user-registration', views.UserRegistration, name="UserRegistration"),
    path('user-login',views.UserLogin,name="UserLogin"),
    path('user-profile',views.userProfile,name="userProfile"),
    path('user-logout',views.logout_view,name='user-logout')
] 
