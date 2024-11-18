from django.db import models
from django.utils import timezone

class Soru(models.Model):
    soru_metni = models.CharField(max_length=200)
    yayinlanma_tarihi = models.DateTimeField('yayınlanma tarihi')
    
    def __str__(self):
        return self.soru_metni
    
    def yeni_mi(self):
        return self.yayinlanma_tarihi >= timezone.now() - timezone.timedelta(days=1)

class Secenek(models.Model):
    soru = models.ForeignKey(Soru, on_delete=models.CASCADE)
    secenek_metni = models.CharField(max_length=200)
    oylar = models.IntegerField(default=0)
    
    def __str__(self):
        return self.secenek_metni

class OyKullanici(models.Model):
    soru = models.ForeignKey(Soru, on_delete=models.CASCADE)
    ip_adresi = models.GenericIPAddressField()
    oy_kullanma_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('soru', 'ip_adresi')  # Bir IP'den bir soruya sadece bir oy
        verbose_name = 'Oy Kullanan'
        verbose_name_plural = 'Oy Kullananlar'
    
    def __str__(self):
        return f"{self.ip_adresi} - {self.soru.soru_metni}"