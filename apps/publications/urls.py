from django.urls import path

from publications import views

urlpatterns = [
    path('ask/', views.create_question_view, name = 'ask_question'),
    path('question/<int:question_id>/', views.question_detail_view, name = 'question_detail'),
    path('topic/<int:topic_id>/', views.topic_detail_view, name = 'topic_detail'),
    path('vote/question/<int:question_id>/', views.vote_question_view, name = 'vote_question'),
    path('vote/answer/<int:answer_id>/', views.vote_answer_view, name = 'vote_answer'),
    path('follow/<int:topic_id>/', views.follow_topic_view, name = 'follow_topic'),
    path('unfollow/<int:topic_id>/', views.unfollow_topic_view, name = 'unfollow_topic'),
]