from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from users.models import User
from publications.models import Question, Topic
from .forms import QuestionForm, AnswerForm
from django.contrib import messages
from publications.services.services import (
    create_question,
    upvote_question,
    downvote_question,
    remove_question_vote,
    get_question_vote_status,

    create_answer,
    upvote_answer,
    downvote_answer,
    remove_answer_vote,
    get_answer_vote_status,

    get_topics_from_question,
    get_questions_from_topic,

    is_following_topic,
    follow_topic,
    unfollow_topic,
    get_topic_followers_count,

) 

@login_required
def create_question_view(request):

    form = QuestionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        topic_ids = [t.id for t in data['topics']]

        create_question(
            user = request.user,
            title = data['title'],
            content = data['content'],
            topic_ids = topic_ids
        )
        
        messages.success(request, "Question asked successfully!")
        return redirect('home')

    return render(request, 'publications/ask_question.html', {'form': form})


@login_required
@require_POST
def vote_question_view(request, question_id):
    user_id = request.user.id
    vote_type = request.POST.get('vote_type')
    current_status = get_question_vote_status(user_id, question_id) or 'NONE'

    VOTE_ACTIONS = {
        'UP': ('UPVOTED', upvote_question),
        'DOWN': ('DOWNVOTED', downvote_question),
    }

    action = VOTE_ACTIONS.get(vote_type)

    if action:
        status, func = action
        if current_status == status:
            remove_question_vote(user_id, question_id)
        else:
            func(user_id, question_id)

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
@require_POST
def vote_answer_view(request, answer_id):
    user_id = request.user.id
    vote_type = request.POST.get('vote_type')
    current_status = get_answer_vote_status(user_id, answer_id) or 'NONE'

    VOTE_ACTIONS = {
        'UP': ('UPVOTED', upvote_answer),
        'DOWN': ('DOWNVOTED', downvote_answer),
    }

    action = VOTE_ACTIONS.get(vote_type)

    if action:
        status, func = action
        if current_status == status:
            remove_answer_vote(user_id, answer_id)
        else:
            func(user_id, answer_id)

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def question_detail_view(request, question_id):
    user_id = request.user.id if request.user.is_authenticated else None
    question = get_object_or_404(Question, id = question_id)
    question.set_vote_status(user_id)
    topics = get_topics_from_question(question_id)
    answers = question.answers.all().order_by('-timestamp')
    
    for answer in answers:
        answer.set_vote_status(user_id)
        
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            try:
                create_answer(
                    user = request.user,
                    question_id = question.id,
                    content = form.cleaned_data['content']
                )
                messages.success(request, "Answer posted successfully!")
                return redirect('question_detail', question_id=question.id)
            except Exception as e:
                messages.error(request, f"Error posting answer: {e}")
    else:
        form = AnswerForm()

    context = {
        'question': question,
        'topics': topics,
        'answers': answers,
        'answer_form': form
    }

    return render(request, 'publications/question_detail.html', context)

def topic_detail_view(request, topic_id):
    user_id = request.user.id if request.user.is_authenticated else None
    topic = get_object_or_404(Topic, id = topic_id)
    questions = get_questions_from_topic(topic_id)

    is_following = (
        request.user.is_authenticated 
        and is_following_topic(user_id, topic_id)
    )

    follower_count = get_topic_followers_count(topic_id)
    
    for question in questions:
        question.set_vote_status(user_id)

    context = {
        'topic': topic,
        'is_following': is_following,
        'topic_follower_count': follower_count,
        'questions': questions
    }

    return render(request, 'publications/topic_detail.html', context)

@login_required
@require_POST
def follow_topic_view(request, topic_id):
    follow_topic(request.user.id, topic_id)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
@require_POST
def unfollow_topic_view(request, topic_id):
    unfollow_topic(request.user.id, topic_id)
    return redirect(request.META.get('HTTP_REFERER', 'home'))
