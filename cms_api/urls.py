from . import views
from django.urls import re_path

urlpatterns = [

    # User Registration And Login
    re_path(r'^register/', views.UserRegistration.as_view()),  # POST
    re_path(r'^login/', views.UserLogin.as_view()),  # POST

    # Content CRUD Opration
    re_path(r'^git initgit init/', views.CreateContent.as_view()),  # POST
    re_path(r'^retrieve-content/(?P<pk>\d+)/', views.RetrieveContent.as_view()),  # GET
    re_path(r'^update-content/(?P<pk>\d+)/', views.UpdateContent.as_view()),  # POST
    re_path(r'^delete-content/(?P<pk>\d+)/', views.DeleteContent.as_view()),  # GET
    re_path(r'^all-content/', views.GetAllContentAPI.as_view()),  # GET

    # Searching Content # pass keyword in ?search={{search_keyword}}
    re_path(r'^search-content/', views.SearchContent.as_view()),  # GET

]
