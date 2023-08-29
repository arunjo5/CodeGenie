from django.contrib import admin

from django.contrib import admin
from base.models import Explain, Language, User, Snippet, Comment, Translate

# Register your models here.
admin.site.register(User)
admin.site.register(Language)
admin.site.register(Snippet)
admin.site.register(Comment)
admin.site.register(Explain)
admin.site.register(Translate)