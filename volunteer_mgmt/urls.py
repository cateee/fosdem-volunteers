from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import volunteers.views as views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'volunteer_mgmt.views.home', name='home'),
    # url(r'^volunteer_mgmt/', include('volunteer_mgmt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #url(r'^volunteers/', include('volunteers.urls', namespace='volunteers')),
    #url(r'^accounts/login/.*$', 'django.contrib.auth.views.login'),
    #url(r'^volunteers/LogOut/$', 'volunteers.views.logOut'),
    #url(r'^AddTasks/$', views.add_tasks, name='add_tasks'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Userena urls:
    url(r'^(?P<edition_name>[\w-]+)/$', 'volunteers.views.promo', name='promo'),
    url(r'^(?P<edition_name>[\w-]+)/faq/', 'volunteers.views.faq', name='faq'),
    url(r'^(?P<edition_name>[\w-]+)/volunteers/signup', 'volunteers.views.signup', name='signup'),
    url(r'^(?P<edition_name>[\w-]+)/volunteers/(?P<username>(?!signout|signup|signin)[\.\w-]+)/$', 'volunteers.views.profile_detail', name='profile_detail'),
    url(r'^(?P<edition_name>[\w-]+)/volunteers/(?P<username>[\.\w-]+)/edit/$', 'volunteers.views.profile_edit', name='userena_profile_edit'),
    url(r'^(?P<edition_name>[\w-]+)/volunteers/page/(?P<page>[0-9]+)/$', views.ProfileListView.as_view(), name='userena_profile_list_paginated'),
    url(r'^(?P<edition_name>[\w-]+)/volunteers/$', views.ProfileListView.as_view(), name='userena_profile_list'),
    url(r'^(?P<edition_name>[\w-]+)/volunteers/', include('userena.urls')),
    url(r'^(?P<edition_name>[\w-]+)/messages/', include('userena.contrib.umessages.urls')),
    # other urls:
    url(r'^(?P<edition_name>[\w-]+)/tasks/(?P<username>[\.\w-]+)', 'volunteers.views.task_list_detailed', name='task_list_detailed'),
    url(r'^(?P<edition_name>[\w-]+)/task/(?P<task_id>\d+)/$', 'volunteers.views.task_detailed', name='task_detailed'),
    url(r'^(?P<edition_name>[\w-]+)/talk/(?P<talk_id>\d+)/$', 'volunteers.views.talk_detailed', name='talk_detailed'),
    url(r'^(?P<edition_name>[\w-]+)/tasks/', 'volunteers.views.task_list', name='task_list'),
    url(r'^(?P<edition_name>[\w-]+)/talks/', 'volunteers.views.talk_list', name='talk_list'),
    url(r'^(?P<edition_name>[\w-]+)/category_schedule/', 'volunteers.views.category_schedule_list', name='category_schedule_list'),
    url(r'^(?P<edition_name>[\w-]+)/task_schedule/(?P<template_id>\d+)/$', 'volunteers.views.task_schedule', name='task_schedule'),
    url(r'^(?P<edition_name>[\w-]+)/task_schedule_csv/(?P<template_id>\d+)/$', 'volunteers.views.task_schedule_csv', name='task_schedule_csv'),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
