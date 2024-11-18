from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Soru, Secenek, OyKullanici

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    son_anketler = Soru.objects.order_by('-yayinlanma_tarihi')[:5]
    context = {'son_anketler': son_anketler}
    return render(request, 'anketler/index.html', context)

def detail(request, soru_id):
    soru = get_object_or_404(Soru, pk=soru_id)
    ip_adresi = get_client_ip(request)
    
    # Kullanıcının daha önce oy kullanıp kullanmadığını kontrol et
    daha_once_oy_kullanmis = OyKullanici.objects.filter(
        soru=soru, 
        ip_adresi=ip_adresi
    ).exists()
    
    return render(request, 'anketler/detail.html', {
        'soru': soru,
        'daha_once_oy_kullanmis': daha_once_oy_kullanmis
    })

def vote(request, soru_id):
    soru = get_object_or_404(Soru, pk=soru_id)
    ip_adresi = get_client_ip(request)
    
    try:
        secilen_secenek = soru.secenek_set.get(pk=request.POST['secenek'])
    except (KeyError, Secenek.DoesNotExist):
        return render(request, 'anketler/detail.html', {
            'soru': soru,
            'error_message': "Bir seçenek seçmediniz.",
        })
    
    try:
        # Oy kaydını oluştur
        OyKullanici.objects.create(
            soru=soru,
            ip_adresi=ip_adresi
        )
        
        # Oyu kaydet
        secilen_secenek.oylar += 1
        secilen_secenek.save()
        
        return HttpResponseRedirect(reverse('anketler:detail', args=(soru.id,)))
        
    except IntegrityError:
        # Eğer kullanıcı daha önce oy kullandıysa
        return render(request, 'anketler/detail.html', {
            'soru': soru,
            'error_message': "Bu ankete daha önce oy kullandınız!",
            'daha_once_oy_kullanmis': True
        })