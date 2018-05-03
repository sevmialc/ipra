from django.contrib import admin
from .models import *


class PrgAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Место', {
            'fields': ('okr', 'nreg', 'dt',)
        }),
        ('Человек', {
            'fields': (('lname', 'fname', 'sname'), ('bdate', 'gndr', 'snils'), ('docnum', 'docdt')),
        }),
        ('Программа', {
            'fields': ('prg', 'oivid', 'prgnum', 'prgdt', 'mseid'),
        }),
    )


admin.site.register(PrgRhb)
admin.site.register(Prg, PrgAdmin)

admin.site.register(AppVer)
admin.site.register(DelLog)
admin.site.register(PrgOiv)
admin.site.register(PrgOkr)
admin.site.register(PrgReg)
admin.site.register(RhbDic)
admin.site.register(RhbEvnt)
admin.site.register(RhbExc)
admin.site.register(RhbGrp)
admin.site.register(RhbGtsr)
admin.site.register(RhbTsr)
admin.site.register(RhbType)
admin.site.register(RhbRes)
