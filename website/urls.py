from django.urls import path, include, re_path
from . import views
from django.views.static import serve

#USE ONLY ON DEVELOPMENT
from django.conf import settings
from django.conf.urls.static import static
#USE ONLY ON DEVELOPMENT


urlpatterns = [
    path('', views.DashboardView, name='home'),
    path('', views.RepositoryView, name='home'),
    path('publish-thesis/', views.ThesisPublishView.as_view(), name='thesis_publish'),
    path('thesis-list/', views.ThesisListView.as_view(), name='thesis_list'),
    path('thesis/<slug:slug>', views.ThesisDetailView, name='thesis_detail'),
    path('thesis/<slug:slug>/request', views.ThesisRequestView, name='thesis_request'),
    path('thesis/<slug:slug>/delete', views.ThesisDeleteView.as_view(), name='thesis_delete'),
    path('thesis/<slug:slug>/download', views.ThesisDownload, name='thesis_download'),
    path('thesis/update/<slug:slug>', views.ThesisUpdateView, name='thesis_update'),
    path('generate-pdf-url/<slug:slug>', views.generate_temp_url, name='generate_temp_url'),
    path('temp/pdf/<str:url_key>', views.temp_url_redirect, name='temporary_url_redirect'),
    path('request-list/<str:status_filter>', views.ThesisRequestListView.as_view(), name='request_list'),
    path('request/<slug:slug>', views.RequestDetailView, name='request_view'),
    path('request/<slug:slug>/reject', views.RequestReject, name='request_reject'),
    path('download-pdf/<str:source>/<slug:slug>', views.ThesisDownload, name='download'),
    path('window-blur/<str:temp_url>', views.window_blur_method, name='window_blur_method'),
    path('tags-list', views.tags_list, name='tags_list'),
    path('tags/<slug:tag_slug>', views.tags_filter, name='tags_filter'),
    #path('tags/<slug:tag_slug>', views.tags_filter.as_view(), name='tags_filter'),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = views.custom_404


#USE ONLY ON DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#USE ONLY ON DEVELOPMENT
