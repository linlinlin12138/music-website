from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import re_path as url

urlpatterns=[
    path('home',views.home),
    path('playlist',views.play_list),
    path('playlist/<int:playlist_id>/', views.playlist_song),
    path('<int:song_id>/',views.song),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password-change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('register/', views.register, name='register'),
    path('<int:song_id>/comment/',views.song_comment, name='song_comment'),
    path('favouritelist/<int:user_id>/<int:list_id>/',views.favourite_list_song),
    path('<int:song_id>/add_favourite/',views.add_to_favorite,name='add_to_favorite'),
    path('Singer/',views.SingerInfo,name="SingerInfo"),#/Singer/
    path('CMS/',views.Chinese_MS,name = "Chinese_MS"),#/CMS/
    path('CFMS/',views.Chinese_FMS,name = "Chinese_FMS"),
    path('CB/', views.Chinese_BS, name="Chinese_BS"),
    path('WMS/', views.Western_MS, name="Western_MS"),
    path('WFS/', views.Western_FS, name="Western_FS"),
    path('Singer_detail/<int:singer_id>/',views.SingerDetail,name="SingerDetail"),
    path('read/', views.read, name='read'),
    path('read/singer',views.read_singer,name='read_singer'),
    path('delete/singer/<int:singer_id>/', views.delete_singer, name='delete_singer'),
    path('edit/singer/<int:id>/', views.edit_singer, name='edit_singer'),

    path('read/style', views.read_style, name='read_style'),
    path('add/style', views.add_style, name='add_style'),
    path('edit/style/<int:id>/', views.edit_style, name='edit_style'),
    path('delete/style/<int:style_id>/', views.delete_style, name='delete_style'),

    path('read/have', views.read_have, name='read_have'),
    path('add/have',views.add_have,name='add_have'),
    path('delete/style/<int:song_id> <int:playlist_id>',views.delete_have,name='delete_have'),
    path('read/playlist', views.read_playlist, name='read_playlist'),
    path('read/comment', views.read_comment, name='read_comment'),
    path('read/album', views.read_album, name='read_album'),
    path('delete/comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete/favouritelist/<int:list_id>/', views.delete_list, name='delete_list'),
    path('delete/album/<int:album_id>/', views.delete_album, name='delete_album'),
    path('delete/list_song/<int:song_id>/<int:list_id>/', views.delete_list_song, name='delete_list_song'),
    path('add/', views.add, name='add'),
    path('add/singer',views.add_singer,name='add_singer'),
    path('delete/song/<int:song_id>/', views.dele, name='dele'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('add/playlist', views.add_playlist, name='add_playlist'),
    path('add/album', views.add_album, name='add_album'),
    path('delete/playlist/<int:list_id>/', views.delete_playlist, name='delete_playlist'),
    path('edit/playlist/<int:id>/', views.edit_playlist, name='edit_playlist'),
    path('edit/album/<int:id>/', views.edit_album, name='edit_album'),
    path('styles/', views.style_list, name = 'styles'),
    path('styles/<int:style_id>/songs/', views.songs_by_style, name='songs_by_style'),
    path('album/', views.album_list, name='album_list'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('create/', views.create, name='create'),
]

