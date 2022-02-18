from django.contrib import admin
from .models import Waiting,Connected,GroupModel
# Register your models here.
admin.site.register(Waiting)
admin.site.register(Connected)
admin.site.register(GroupModel)