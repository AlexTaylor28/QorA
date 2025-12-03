from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recommendations.services.services import get_user_recommendations, get_topic_recommendations

@login_required
def recommendations_view(request):
    recommended_users = get_user_recommendations(request.user.id)
    recommended_topics = get_topic_recommendations(request.user.id)
    
    context = {
        'recommended_users': recommended_users,
        'recommended_topics': recommended_topics
    }
    
    return render(request, 'recommendations/index.html', context)