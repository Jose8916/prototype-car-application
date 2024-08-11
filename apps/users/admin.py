from django.contrib import admin
from apps.users.models import *
# Register your models here.
admin.site.register(Extended_User)
admin.site.register(AllyCategory)
admin.site.register(Category)
admin.site.register(Ally)
admin.site.register(Subscription)
admin.site.register(Coupon)
admin.site.register(Invoice)

