from django.contrib import admin
from .models import Soru, Secenek, OyKullanici

class SecenekInline(admin.TabularInline):
    model = Secenek
    extra = 3

class SoruAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['soru_metni']}),
        ('Tarih bilgisi', {'fields': ['yayinlanma_tarihi']}),
    ]
    inlines = [SecenekInline]
    list_display = ('soru_metni', 'yayinlanma_tarihi')
    list_filter = ['yayinlanma_tarihi']
    search_fields = ['soru_metni']

class OyKullaniciAdmin(admin.ModelAdmin):
    list_display = ('ip_adresi', 'soru', 'oy_kullanma_tarihi')
    list_filter = ['oy_kullanma_tarihi']
    search_fields = ['ip_adresi']

admin.site.register(Soru, SoruAdmin)
admin.site.register(OyKullanici, OyKullaniciAdmin)