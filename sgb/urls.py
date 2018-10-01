"""banca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from sgb import views as sgb_views
#from django.contrib.auth.views import


urlpatterns = [
    url(r'^curso/(?P<pk>\d+)/', sgb_views.curso_update, name='curso_update'),
    url(r'^curso_novo/', sgb_views.curso_create, name='curso_create'),
    url(r'^curso_remover/(?P<pk>\d+)/', sgb_views.curso_delete, name='curso_delete'),
    url(r'^curso/', sgb_views.curso_home, name='curso_home'),
    url(r'^calendar/', sgb_views.calendar, name='calendar'),
    url(r'^professor/(?P<pk>\d+)/', sgb_views.professor_update, name='professor_update'),
    url(r'^aluno/(?P<pk>\d+)/', sgb_views.aluno_update, name='aluno_update'),
    url(r'^tcc_gti/(?P<pk>\d+)/', sgb_views.tcc_update_gti, name='tcc_update_gti'),
    url(r'^tcc_cc/(?P<pk>\d+)/', sgb_views.tcc_update_cc, name='tcc_update_cc'),
    url(r'^tcc_spi/(?P<pk>\d+)/', sgb_views.tcc_update_spi, name='tcc_update_spi'),
    url(r'^tcc_redes/(?P<pk>\d+)/', sgb_views.tcc_update_redes, name='tcc_update_redes'),
    url(r'^banca/(?P<pk>\d+)/', sgb_views.banca_update, name='banca_update'),
    url(r'^sala/(?P<pk>\d+)/', sgb_views.salas_update, name='salas_update'),
    url(r'^disponibilidade/(?P<pk>\d+)/', sgb_views.disp_update, name='disp_update'),
    url(r'^user/(?P<pk>\d+)/', sgb_views.user_update, name='user_update'),
    url(r'^professor/', sgb_views.professor_home, name='professor_home'),
    url(r'^professor_novo/', sgb_views.professor_create, name='professor_create'),
    url(r'^professor_remover/(?P<pk>\d+)/', sgb_views.professor_delete, name='professor_delete'),
    url(r'^aluno_novo/', sgb_views.aluno_create, name='aluno_create'),
    url(r'^aluno_remover/(?P<pk>\d+)/', sgb_views.aluno_delete, name='aluno_delete'),
    url(r'^aluno/', sgb_views.aluno_home, name='aluno_home'),
    url(r'^salas/', sgb_views.salas_home, name='salas_home'),
    url(r'^salas_novo/', sgb_views.salas_create, name='salas_create'),
    url(r'^salas_remover/(?P<pk>\d+)/', sgb_views.salas_delete, name='salas_delete'),
    url(r'^tcc/', sgb_views.tcc_home, name='tcc_home'),
    url(r'^tcc_novo/', sgb_views.tcc_create_cc, name='tcc_create_cc'),
    url(r'^tcc_novo_gti/', sgb_views.tcc_create_gti, name='tcc_create_gti'),
    url(r'^tcc_novo_spi/', sgb_views.tcc_create_spi, name='tcc_create_spi'),
    url(r'^tcc_novo_redes/', sgb_views.tcc_create_redes, name='tcc_create_redes'),
    url(r'^tcc_remover/(?P<pk>\d+)/', sgb_views.tcc_delete, name='tcc_delete'),
    url(r'^banca_data/', sgb_views.banca_data, name='banca_data'),
    url(r'^banca/', sgb_views.banca_home, name='banca_home'),
    url(r'^banca_novo/', sgb_views.banca_create, name='banca_create'),
    url(r'^banca_remover/(?P<pk>\d+)/', sgb_views.banca_delete, name='banca_delete'),
    url(r'^listar_cc/', sgb_views.listar_cc, name='listar_cc'),
    url(r'^listar_spi/', sgb_views.listar_spi, name='listar_spi'),
    url(r'^listar_gti/', sgb_views.listar_gti, name='listar_gti'),
    url(r'^listar_rc/', sgb_views.listar_rc, name='listar_rc'),
    url(r'^disponibilidade/', sgb_views.disp_home, name='disp_home'),
    url(r'^disponibilidade_novo/', sgb_views.disp_create, name='disp_create'),
    url(r'^disponibilidade_remover/(?P<pk>\d+)/', sgb_views.disp_delete, name='disp_delete'),
    url(r'^cadastro/', sgb_views.register, name='register'),
    url(r'^user/', sgb_views.user_home, name='user_home'),
    url(r'^user_remover/(?P<pk>\d+)/', sgb_views.user_delete, name='user_delete'),
    url(r'^index/$', sgb_views.index, name='index'),
    url(r'^relatorios/(?P<pk>\d+)/', sgb_views.testerel, name='testerel'),
    url(r'^etiquetas/(?P<pk>\d+)/', sgb_views.etiqueterel, name='etiqueterel'),
    url(r'^declaracao/(?P<pk>\d+)/(?P<curso>\w+)/$', sgb_views.declaracao, name='declaracao'),
    url(r'^pesquisa_global/', sgb_views.pesquisa_global, name='pesquisa_global'),
    url(r'^admin/', include(admin.site.urls)),
]
