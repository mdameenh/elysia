from django.contrib import admin

# Register your models here.
from .models import Team_Info, Player_Info, Player_Basic_Stats, Player_Detailed_Stats, FPL_Config

admin.site.register(Team_Info)
admin.site.register(Player_Info)
admin.site.register(Player_Basic_Stats)
admin.site.register(Player_Detailed_Stats)
admin.site.register(FPL_Config)
