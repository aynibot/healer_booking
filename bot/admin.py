from django.contrib import admin

from .models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

# Register your models here.
admin.site.register(Member, MemberAdmin)