from django.contrib import admin
from .models import Payment, Profile, Post, Referral, ProductScheme,Services

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referral_code', 'referred_by', 'kyc_document_type', 'pan_card', 'bank_passbook')
    search_fields = ('user__username', 'referral_code')
    list_filter = ('kyc_document_type',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('product_id','title','total', 'img', 'desc')
    search_fields = ('title',)
    list_filter = ('title',)

class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referred_by', 'referred_user', 'timestamp')

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'img','desc') 

class ProductSchemeAdmin(admin.ModelAdmin):
    list_display = ('product_id','investment', 'total', 'days')

admin.site.register(ProductScheme)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Referral,ReferralAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Services,ServicesAdmin)
admin.site.register(Payment)