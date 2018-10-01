from django.contrib import admin
from sgb.models import Professor, Aluno, Salas, Banca, Disponibilidade

admin.site.register(Professor)
admin.site.register(Aluno)
admin.site.register(Salas)
admin.site.register(Banca)
admin.site.register(Disponibilidade)
