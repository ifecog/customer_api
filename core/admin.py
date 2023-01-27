from django.contrib import admin
from .models import *

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)


admin.site.register(Document)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Profession)
admin.site.register(Datasheet)
