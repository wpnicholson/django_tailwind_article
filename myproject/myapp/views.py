from django.shortcuts import render

# Create your views here.
def index(request):
    text = 'Hello World!'
    context = {
        'context_text': text,
    }
    return render(request, 'myapp/index.html', context)
