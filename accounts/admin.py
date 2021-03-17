from django.contrib import admin
from .models import GuestEmail
from django.contrib.auth import get_user_model
# Register your models here.
User = get_user_model()
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User

class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmail
User = get_user_model()
admin.site.register(User, UserAdmin)
admin.site.register(GuestEmail, GuestEmailAdmin)
