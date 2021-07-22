from django.contrib import admin

from .models import Choice, Question
from account.models import Account

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        #('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['email']}),
    ]
    list_display = ('email', 'username')
    list_filter = ['username']
    search_fields = ['username']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Account, AccountAdmin)