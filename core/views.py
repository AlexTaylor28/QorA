from django.shortcuts import render
from publications.models import Question
from publications.services.services import get_user_feed
from recommendations.services.services import get_user_recommendations, get_topic_recommendations

def home(request):
    if request.user.is_authenticated:
        #PROBAR SIN LIST
        questions = list(get_user_feed(request.user.id))
        recommended_users = get_user_recommendations(request.user.id)
        recommended_topics = get_topic_recommendations(request.user.id)

        for question in questions:
            question.set_vote_status(request.user.id)
                
        context = {
            'questions': questions,
            'page_title': 'Your Feed',
            'recommended_users': recommended_users[:5],
            'recommended_topics': recommended_topics[:5]
        }
    else:
        questions = list(Question.objects.all().order_by('-timestamp')[:20])
    
        for question in questions:
            question.set_vote_status(None)
            
        context = {
            'questions': questions,
            'page_title': 'Latest Questions'
        }
        
    return render(request, 'pages/index.html', context)