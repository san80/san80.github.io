from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(auction_list)
admin.site.register(bids)
admin.site.register(User)
admin.site.register(comments)
admin.site.register(Category)

