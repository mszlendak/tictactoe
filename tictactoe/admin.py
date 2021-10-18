from django.contrib import admin
from tictactoe.models import Match


class MatchAdmin(admin.ModelAdmin):
    pass


admin.site.register(Match, MatchAdmin)
