from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == 'POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Seçim yapılmadıysa formu hata mesajıyla tekrar göster
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "Bir seçenek seçmediniz.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Oy verdikten sonra sonuçlar sayfasına yönlendir
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))