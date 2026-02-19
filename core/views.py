from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .forms import QueryForm, QueryMediaForm
from .utils import get_weather
from .utils import get_market_prices
from twilio.twiml.voice_response import VoiceResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# Create your views here.

# Authentication Module

def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
    return render(request, 'auth/login.html')

def user_logout(request):
    logout(request)
    return redirect('/')



@login_required
def farmer_dashboard(request):
    if request.user.role != 'farmer':
        return redirect('/')
    
    queries = Query.objects.filter(farmer=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    
    # Weather based on farmer's district
    city = request.user.farmerprofile.district
    weather_forecast = get_weather(city)
    market_prices = get_market_prices()
    context = {
        'queries': queries,
        'notifications': notifications,
        'weather_forecast': weather_forecast,
        'market_prices':market_prices
    }

    return render(request, 'farmer/dashboard.html', context)


@login_required
def submit_query(request):
    if request.user.role != 'farmer':
        return redirect('/')
    
    MediaFormSet = modelformset_factory(QueryMedia, form=QueryMediaForm, extra=3)
    
    if request.method == 'POST':
        form = QueryForm(request.POST)
        formset = MediaFormSet(request.POST, request.FILES, queryset=QueryMedia.objects.none())
        
        if form.is_valid() and formset.is_valid():
            query = form.save(commit=False)
            query.farmer = request.user
            query.save()
            
            for media_form in formset.cleaned_data:
                if media_form:
                    file = media_form['file']
                    QueryMedia.objects.create(query=query, file=file)
            
            return redirect('/dashboard/')
    else:
        form = QueryForm()
        formset = MediaFormSet(queryset=QueryMedia.objects.none())
    
    return render(request, 'farmer/submit_query.html', {'form': form, 'formset': formset})


@login_required
def expert_dashboard(request):
    if request.user.role != 'expert':
        return redirect('/')
    
    queries = Query.objects.filter(status__in=['submitted', 'assigned']).order_by('-created_at')
    
    context = {'queries': queries}
    return render(request, 'expert/dashboard.html', context)



from django.shortcuts import get_object_or_404

@login_required
def respond_query(request, query_id):
    if request.user.role != 'expert':
        return redirect('/')
    
    query = get_object_or_404(Query, id=query_id)
    
    if request.method == 'POST':
        response_text = request.POST.get('response_text')
        ExpertResponse.objects.create(query=query, expert=request.user, response_text=response_text)
        query.status = 'responded'
        query.save()
        notify_user(query)
        return redirect('/expert/dashboard/')
    
    return render(request, 'expert/respond_query.html', {'query': query})

def notify_user(query):
    Notification.objects.create(
        user=query.farmer,
        message=f'Your query "{query.title}" has been answered by an expert!'
    )



@login_required
def knowledge_list(request):
    articles = Article.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    # Optional filtering
    category_id = request.GET.get('category')
    crop_filter = request.GET.get('crop')

    if category_id:
        articles = articles.filter(category_id=category_id)
    if crop_filter:
        articles = articles.filter(crop__icontains=crop_filter)

    context = {
        'articles': articles,
        'categories': categories
    }
    return render(request, 'knowledge/knowledge_list.html', context)


@login_required
def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'knowledge/article_detail.html', {'article': article})


@login_required
def mark_notification_read(request, notif_id):
    notif = Notification.objects.get(id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('/dashboard/')



from twilio.twiml.voice_response import VoiceResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def ivr(request):
    resp = VoiceResponse()
    resp.say("Welcome to KrishiSetu. Please record your query after the beep.", voice='alice')
    resp.record(max_length=60, action='/ivr/save-recording/')
    return HttpResponse(str(resp), content_type='text/xml')

@csrf_exempt
def ivr_save_recording(request):
    recording_url = request.POST.get('RecordingUrl')
    # Save as a QueryMedia record
    dummy_user = User.objects.get(username='dummy_farmer')  # Replace with mapping
    query = Query.objects.create(farmer=dummy_user, title='Voice Query', description='Recorded via IVR')
    QueryMedia.objects.create(query=query, file=recording_url)
    
    resp = VoiceResponse()
    resp.say("Thank you! Your query has been recorded. Our expert will respond soon.", voice='alice')
    return HttpResponse(str(resp), content_type='text/xml')
