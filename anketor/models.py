from django.db import models

class Anket(models.Model):
    baslik = models.CharField(max_length=200)
    yayin_tarihi = models.DateTimeField('yayınlanma tarihi')

    def __str__(self):
        return self.baslik

class Secenek(models.Model):
    anket = models.ForeignKey(Anket, on_delete=models.CASCADE)
    secenek_metni = models.CharField(max_length=200)
    oy_sayisi = models.IntegerField(default=0)

    def __str__(self):
        return self.secenek_metni