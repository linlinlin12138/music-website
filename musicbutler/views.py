from django.shortcuts import render,get_object_or_404,redirect
import time
from datetime import date
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.db import connection
from .forms import LoginForm, UserRegistrationForm,CommentForm,ListForm,AddToFavoritesForm, SearchForm
from .models import Playlist,Song,Have,Singer,Comments,FavouriteList,Exist
import random
import pymysql
import pymysql.cursors
import MySQLdb


def home(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM song WHERE song.name=%s", [query])
            results = cursor.fetchall()
    return render(request, 'base.html', {'form': form, 'query': query, 'results': results})


def play_list(request, playlist_name=None):
    with connection.cursor() as cursor:
        # Retrieve all playlists
        cursor.execute("SELECT * FROM playlist")
        playlistsData = cursor.fetchall()
        playlists=list(playlistsData)

    return render(request, 'playlist.html', { 'playlists': playlists})

def playlist_song(request,playlist_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT singer.name,s.name,s.song_id FROM singer,(SELECT song.song_id,song.singer_id,song.name FROM song, (SELECT * FROM have WHERE have.playlist_id=%s) as h WHERE h.song_id=song.song_id) as s WHERE s.singer_id=singer.singer_id",[playlist_id])
        songs=cursor.fetchall()
        song=list(songs)
        cursor.execute("SELECT * FROM playlist WHERE playlist.list_id=%s",[playlist_id])
        playlist=cursor.fetchone()

    return render(request,'playlist_song.html',{'song':song,'playlist':playlist,})

#@require_POST
def favourite_list_song(request,list_id,user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM favourite_list WHERE list_id=%s AND user_id=%s",[list_id,user_id])
        list=cursor.fetchone()
        cursor.execute("SELECT song.song_id, name from song,(SELECT song_id FROM exist WHERE list_id=%s AND user_id=%s) as s WHERE s.song_id=song.song_id",[list_id,user_id])
        song=cursor.fetchall()
    return render(request,'flist_song.html',{'list':list,'song':song})


def song(request,song_id):
    if not request.user.id:
        return redirect("http://127.0.0.1:8000/musicbutler/login")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM song WHERE song_id=%s",[song_id])
        song = cursor.fetchone()
        link_id = song[4].split("/")[4]
        cursor.execute("SELECT * FROM singer,(SELECT * FROM song WHERE song_id=%s) as s WHERE singer.singer_id=s.singer_id", [song_id])
        singer=cursor.fetchone()
        cursor.execute("SELECT auth_user.username, c.content FROM auth_user, (SELECT user_id,content FROM comments WHERE song_id=%s) as c WHERE c.user_id=auth_user.id",[song_id])
        comments=cursor.fetchall()
    form=CommentForm()
    add_form=AddToFavoritesForm(request.user)
    return render(request,'song.html',{'singer':singer,'song':song,'comments':comments,'form':form,'add_form':add_form,'link_id':link_id})


def dashboard(request):
    if request.user.username:
        id=request.user.id
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM favourite_list WHERE user_id=%s", [id])
            user_list=cursor.fetchall()
        form=ListForm()
        return render(request,'dashboard.html',{'user_list':user_list,'form':form})
    else:
        return redirect("http://127.0.0.1:8000/musicbutler/login")

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,'register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html',{'user_form': user_form})

@require_POST
def song_comment(request, song_id):
    if request.user.id:
        if request.method == "POST":
            with connection.cursor() as cursor:
                cursor.execute("Select c_id From comments ORDER BY c_id DESC")
                c_id = cursor.fetchone()
                c_id=c_id[0]+1
            try:
                start = time.time()
                content = request.POST['content']
                end = time.time()
                mytime = round(abs(start - end), 3)
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO comments VALUES(%s,%s,%s,%s)", [c_id, request.user.id, song_id,content])
                return render(request, 'finfo.html', {"info": "add successfully！","id":song_id,'time':mytime})
            except:
                return render(request, 'finfo.html', {"info": "add unsuccessfully！","id":song_id,'time':0})
    else:
        return redirect("http://127.0.0.1:8000/musicbutler/login")


def add_to_favorite(request,song_id):
    if request.method=="POST":
        if not request.user.id:
            return redirect("http://127.0.0.1:8000/musicbutler/login")
        try:
            start = time.time()
            list_name=request.POST['list_name']
            end = time.time()
            mytime = round(abs(start - end), 3)
        except:
            return render(request, 'finfo.html', {"info": "add unsuccessfully！","time":0})
        with connection.cursor() as cursor:
            cursor.execute("SELECT list_id FROM favourite_list WHERE name=%s AND user_id=%s",[list_name,request.user.id])
            list_id=cursor.fetchone()
            list_id=list_id[0]
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO exist VALUES(%s,%s,%s)",[list_id,request.user.id,song_id])
            return render(request, 'finfo.html', {"info": "add successfully！","id":song_id,"time":mytime})
        except:
            return render(request, 'finfo.html', {"info": "add unsuccessfully！","id":song_id,'time':0})
    else:
        return render(request, 'song.html')

def delete_list(request,list_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM favourite_list WHERE list_id=%s AND user_id=%s", [list_id,request.user.id])
        end = time.time()
        mytime = round(abs(start - end), 3)
        return render(request, 'dash_info.html', {"info": "Delete Successfully!", 'time': mytime})
    except:
        return render(request, 'dash_info.html', {"info": "Delete Unsuccessfully!", 'time': 0})

def delete_list_song(request,song_id,list_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM exist WHERE list_id=%s AND user_id=%s AND song_id=%s", [list_id,request.user.id,song_id])
        end = time.time()
        mytime = round(abs(start - end), 3)
        return render(request, 'dash_info.html', {"info": "Delete Successfully!", 'time': mytime})
    except:
        return render(request, 'dash_info.html', {"info": "Delete Unsuccessfully!", 'time': 0})

def create(request):
    if request.method=="POST":
        with connection.cursor() as cursor:
            cursor.execute("Select list_id From favourite_list WHERE user_id=%s ORDER BY list_id DESC",[request.user.id])
            list_id = cursor.fetchone()
            if not list_id:
                list_id=0
            else:
                list_id=list_id[0]+1
        try:
            start = time.time()
            list_name=request.POST['list_name']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO favourite_list VALUES(%s,%s,%s)", [list_id, request.user.id, list_name])
            end = time.time()
            mytime = round(abs(start - end), 3)
            return render(request, 'dash_info.html', {"info": "add successfully！",'time':mytime})
        except:
            return render(request, 'dash_info.html', {"info": "add unsuccessfully！",'time':0})
    else:
        return render(request, 'create.html')

def SingerInfo(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM singer")
        Singdata = cursor.fetchall()
        # Singdata = Singer.objects.all()
        singer_li = list(Singdata)
        singer_names = []
        for i in range(len(Singdata)):
            newname = Singdata[i][1].split("，")[0]
            singer_names.append(newname)
        zip_list = zip(Singdata, singer_names)
    return render(request,'Singer.html',{'ziplist':zip_list})

def Chinese_MS(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM singer")
        Singdata = cursor.fetchall()
        names = []
        for i in range(25):
            newname = Singdata[i][1].split("，")[0]
            names.append(newname)
        ziplist = zip(Singdata[:25], names)
    return render(request, 'CMS.html', {'ziplist': ziplist})

def Chinese_FMS(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM singer")
        Singdata = cursor.fetchall()
        names = []
        for i in range(25, 50):
            newname = Singdata[i][1].split("，")[0]
            names.append(newname)
        ziplist = zip(Singdata[25:50], names)
    return render(request, 'CFMS.html', {'ziplist': ziplist})

def Chinese_BS(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM singer")
        Singdata = cursor.fetchall()
        names = []
        for i in range(50, 75):
            newname = Singdata[i][1].split("，")[0]
            names.append(newname)
        ziplist = zip(Singdata[50:75], names)
    return render(request, 'CB.html', {'ziplist': ziplist})

def Western_MS(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM singer")
        Singdata = cursor.fetchall()
        names = []
        for i in range(75, 100):
            newname = Singdata[i][1].split("，")[0]
            names.append(newname)
        ziplist = zip(Singdata[75:100], names)
    return render(request, 'WMS.html', {'ziplist': ziplist})

def Western_FS(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM singer")
        Singdata = cursor.fetchall()
        names = []
        for i in range(100, len(Singdata)):
            newname = Singdata[i][1].split("，")[0]
            names.append(newname)
        ziplist = zip(Singdata[100:len(Singdata)], names)
    return render(request, 'WFS.html', {'ziplist': ziplist})

def SingerDetail(request,singer_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM singer WHERE singer.singer_id = %s",[singer_id])
        singer_info = cursor.fetchall()
        singer_info = singer_info[0]
        true_name = singer_info[1].split("，")[0]
        nickname = singer_info[1].split("，")[1:]
        nickname = ','.join(nickname)
        cursor.execute("SELECT * FROM song WHERE song.singer_id = %s",[singer_id])
        songInfo = cursor.fetchall()
    return render(request,'Singer_detail.html',{'true_name':true_name,'singer_info':singer_info,'songInfo':songInfo})

def read(request):
    page_number = request.GET.get('page', 1)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM song")
        song=cursor.fetchall()
    paginator = Paginator(song, 10)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'song': song,'page':page}
    return render(request, 'read.html', context)

def read_have(request):
    page_number = request.GET.get('page', 1)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM have")
        have = cursor.fetchall()
    paginator = Paginator(have, 1000)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'have': have, 'page': page}
    return render(request, 'read_have.html', context)

def read_singer(request):
    page_number = request.GET.get('page', 1)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM singer")
        song = cursor.fetchall()
    paginator = Paginator(song, 60)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'song': song, 'page': page}
    return render(request, 'read_singer.html', context)

def read_style(request):
    page_number = request.GET.get('page', 1)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM style")
        song = cursor.fetchall()
    paginator = Paginator(song, 10)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'song': song, 'page': page}
    return render(request, 'read_style.html', context)

def read_playlist(request):
    page_number = request.GET.get('page', 1)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM playlist")
        playlist=cursor.fetchall()
    paginator = Paginator(playlist, 10)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'playlist': playlist,'page':page}
    return render(request, 'read_playlist.html', context)

def read_album(request):
    page_number = request.GET.get('page', 1)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM album")
        album=cursor.fetchall()
    paginator = Paginator(album, 100)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'album':album,'page':page}
    return render(request, 'read_album.html', context)

def add(request):
    if request.method == "POST":
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("Select song_id From song ORDER BY song_id DESC")
            song_id = cursor.fetchone()
        song_id = song_id[0] + 1
        try:
            name = request.POST['name']
            photo_link = request.POST['photo_link']
            lyric = request.POST['lyric']
            audio_link = request.POST['audio_link']
            singer_id = request.POST['singer_id']
            album_id = request.POST['album_id']
            style_id = request.POST['style_id']
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM singer WHERE singer_id = %s",[singer_id])
                warn1 = cursor.fetchall()
                if len(warn1) == 0:
                    end = time.time()
                    mytime = round(abs(start - end), 3)
                    return render(request,'info.html',{"info": "Add Unsuccessfully! Please add the song to an existing singer!","time":mytime})
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM album WHERE album_id = %s",[album_id])
                warn2 = cursor.fetchall()
                if len(warn2) == 0:
                    end = time.time()
                    mytime = round(abs(start - end), 3)
                    return render(request,'info.html',{"info": "Add Unsuccessfully! Please add the song to an existing album!","time":mytime})
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM style WHERE style_id = %s",[style_id])
                warn1 = cursor.fetchall()
                if len(warn1) == 0:
                    end = time.time()
                    mytime = round(abs(start - end), 3)
                    return render(request,'info.html',{"info": "Add Unsuccessfully! Please add the song to an existing music style!","time":mytime})
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO song VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",[song_id,name,photo_link,lyric,audio_link,singer_id,album_id,style_id])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"info": "Add Successfully！","time":mytime})
        except:
            return render(request, 'info.html', {"info": "Add Unsuccessfully！",'time':0})
    else:
        return render(request, 'add_song.html')

def add_singer(request):
    if request.method == "POST":
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("Select singer_id From singer ORDER BY singer_id DESC")
            singer_id = cursor.fetchone()
        singer_id = singer_id[0] + 1
        try:
            name = request.POST['name']
            photo_link = request.POST['photo_link']
            introduction = request.POST['introduction']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO singer VALUES(%s,%s,%s,%s)",
                               [singer_id, name, photo_link, introduction])
            end = time.time()
            mytime = round(abs(start - end), 3)
            return render(request, 'info.html', {"info": "Add Successfully！",'read_pos':'singer','time':mytime})

        except:
            return render(request, 'info.html', {"info": "Add Unsuccessfully！",'read_pos':'singer','time':0})
    else:
        return render(request, 'add_singer.html')

def add_have(request):
    if request.method == "POST":

        try:
            start = time.time()
            playlist_id = request.POST['playlist_id']
            song_id = request.POST['song_id']
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM have WHERE playlist_id = %s",[playlist_id])
                warn1 = cursor.fetchall()
                if len(warn1) == 0:
                    end = time.time()
                    mytime = round(abs(start - end), 3)
                    return render(request, 'info.html',
                                  {"info": "Add Unsuccessfully！Please add a song to an existing playlist!", 'read_pos': 'have', 'time': mytime})
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM have WHERE playlist_id = %s AND song_id = %s",[playlist_id,song_id])
                warn2 = cursor.fetchall()
                if len(warn2) != 0:
                    end = time.time()
                    mytime = round(abs(start - end), 3)
                    return render(request, 'info.html',
                                  {"info": "Add Unsuccessfully！The song already exists in this play list!", 'read_pos': 'have', 'time': mytime})
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO have VALUES(%s,%s)",
                               [song_id,playlist_id])
            end = time.time()
            mytime = round(abs(start - end), 3)
            return render(request, 'info.html', {"info": "Add Successfully！",'read_pos':'have','time':mytime})
        except :
            return render(request, 'info.html', {"info": "Add Unsuccessfully！",'read_pos':'have','time':0})

    else:
        return render(request, 'add_have.html')

def add_style(request):
    if request.method == "POST":
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("Select style_id From style ORDER BY style_id DESC")
            style_id = cursor.fetchone()
        style_id = style_id[0] + 1
        try:
            name = request.POST['name']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO style VALUES(%s,%s)",
                               [style_id, name])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"info": "Add Successfully！",'read_pos':'style','time':mytime})
        except:
            return render(request, 'info.html', {"info": "Add Unsuccessfully！",'read_pos':'style','time':0})
    else:
        return render(request, 'add_style.html')

def add_playlist(request):
    if request.method == "POST":
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("Select list_id From playlist ORDER BY list_id DESC")
            list_id = cursor.fetchone()
        list_id = list_id[0] + 1
        try:
            name = request.POST['name']
            photo_link = request.POST['photo_link']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO playlist VALUES(%s,%s,%s)",[list_id,name,photo_link])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"info": "Add Successfully！",'read_pos':"playlist",'time':mytime})
        except:
            return render(request, 'info.html', {"info": "Add Unsuccessfully！",'read_pos':"playlist",'time':0})
    else:
        return render(request, 'add_playlist.html')

def add_album(request):
    if request.method == "POST":
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("Select album_id From album ORDER BY album_id DESC")
            album_id = cursor.fetchone()
        album_id = album_id[0] + 1
        try:
            name = request.POST['name']
            photo_link = request.POST['photo_link']
            release_date = request.POST['release_date']
            company = request.POST['company']
            song_num = 0
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO album VALUES(%s,%s,%s,%s,%s,%s)",[album_id,name,photo_link,release_date,company,song_num])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"info": "Add Successfully！",'read_pos':"album",'time':mytime})
        except:
            return render(request, 'info.html', {"info": "Add Unsuccessfully！",'read_pos':"album",'time':0})
    else:
        return render(request, 'add_album.html')

def edit_singer(request, id):
    if request.method == "POST":
        try:
            start = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM singer WHERE singer_id=%s",[id])
                singer=cursor.fetchone()
            name = request.POST['name']
            photo_link = request.POST['photo_link']
            introduction = request.POST['introduction']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE singer SET name = %s, photo_link=%s,introduction=%s WHERE singer_id=%s",[name,photo_link,introduction,id])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"singer":singer,"info": "Edit Successfully！",'read_pos':'singer','time':mytime})
        except:
            return render(request, 'info.html', {"singer":singer,"info": "Edit Unsuccessfully!",'read_pos':'singer','time':0})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM singer WHERE singer_id=%s", [id])
            singer = cursor.fetchone()
        context = {'singer': singer,'read_pos':'singer'}
        return render(request, 'edit_singer.html', context)

def edit_style(request, id):
    if request.method == "POST":
        try:
            start = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM style WHERE style_id=%s",[id])
                style = cursor.fetchone()
            name = request.POST['name']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE style SET name = %s WHERE style_id=%s",[name,id])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"style":style,"info": "Edit Successfully！",'read_pos':'style','time':mytime})
        except:
            return render(request, 'info.html', {"style":style,"info": "Edit Unsuccessfully!",'read_pos':'style','time':0})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM style WHERE style_id=%s", [id])
            style = cursor.fetchone()
        context = {'style': style,'read_pos':'style'}
        return render(request, 'edit_style.html', context)

def edit_playlist(request, id):
    if request.method == "POST":
        try:
            start = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM playlist WHERE list_id=%s",[id])
                playlist=cursor.fetchone()
            name = request.POST['name']
            photo_link = request.POST['photo_link']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE playlist SET name=%s, photo_link=%s WHERE list_id=%s",[name,photo_link,id])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"playlist":playlist,"info": "Edit Successfully！",'time':mytime,'read_pos':'playlist'})
        except:
            return render(request, 'info.html', {"playlist":playlist,"info": "Edit Unsuccessfully!",'time':0,'read_pos':'playlist'})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM playlist WHERE list_id=%s", [id])
            playlist = cursor.fetchone()
        context = {'playlist': playlist}
        return render(request, 'edit_playlist.html', context)

def edit_album(request, id):
    if request.method == "POST":
        try:
            start = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM album WHERE album_id=%s",[id])
                album=cursor.fetchone()
            name = request.POST['name']
            photo_link = request.POST['photo_link']
            release_date = request.POST['release_date']
            company = request.POST['company']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE album SET name=%s, photo_link=%s,company=%s WHERE album_id=%s",[name,photo_link,company,id])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"album":album,"info": "Edit Successfully！",'time':mytime})
        except:
            return render(request, 'info.html', {"album":album,"info": "Edit Unsuccessfully!",'time':0})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM album WHERE album_id=%s", [id])
            album = cursor.fetchone()
        context = {'album': album}
        return render(request, 'edit_album.html', context)

def edit(request, id):
    if request.method == "POST":
        try:
            start = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM song WHERE song_id=%s",[id])
                song=cursor.fetchone()
            name = request.POST['name']
            photo_link = request.POST['photo_link']
            lyric=request.POST['lyric']
            audio_link = request.POST['audio_link']
            singer_id = request.POST['singer_id']
            album_id = request.POST['album_id']
            style_id = request.POST['style_id']
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM singer WHERE singer_id = %s",[singer_id])
                warn1 = cursor.fetchall()
                if len(warn1) == 0:
                    end = time.time()
                    mytime = round(abs(start - end), 3)
                    return render(request, 'info.html', {"song": song, "info": "Edit Unsuccessfully！This singer does not exist!", 'time': mytime})
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM album WHERE album_id = %s",[album_id])
                warn2 = cursor.fetchall()
                if len(warn2) == 0:
                    end = time.time()
                    mytime = round(abs(start - end), 3)
                    return render(request, 'info.html', {"song": song, "info": "Edit Unsuccessfully！The album does not exist!", 'time': mytime})
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM style WHERE style_id = %s",[style_id])
                warn3 = cursor.fetchall()
                if len(warn3) == 0:
                    end = time.time()
                    mytime = round(abs(start - end), 3)
                    return render(request, 'info.html', {"song": song, "info": "Edit Unsuccessfully！The music style does not exist!", 'time': mytime})
            with connection.cursor() as cursor:
                cursor.execute("UPDATE song SET name=%s, photo_link=%s,lyric=%s,audio_link=%s, singer_id=%s, album_id=%s, style_id=%s WHERE song_id=%s",[name,photo_link,lyric,audio_link,singer_id,album_id,style_id,id])
            end = time.time()
            mytime = round(abs(start-end),3)
            return render(request, 'info.html', {"song":song,"info": "Edit Successfully！",'time':mytime})
        except:
            return render(request, 'info.html', {"song":song,"info": "Edit Unsuccessfully!",'time':0})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM song WHERE song_id=%s", [id])
            song = cursor.fetchone()
        context = {'song': song}
        return render(request, 'edit_song.html', context)

def read_comment(request):
    page_number = request.GET.get('page', 1)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM comments")
        comment=list(cursor.fetchall())
    paginator = Paginator(comment, 25)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context = {'comment': comment,'page':page}
    return render(request, 'read_comment.html', context)


def dele(request, song_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM song WHERE song_id=%s",[song_id])
        end = time.time()
        mytime = round(abs(start-end),3)
        return render(request, 'info.html', {"info": "Delete Successfully!",'time':mytime})
    except:
        return render(request, 'info.html', {"info": "Delete Unsuccessfully!",'time':0})

def delete_have(request, song_id,playlist_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM have WHERE song_id=%s AND playlist_id = %s",[song_id,playlist_id])
        end = time.time()
        mytime = round(abs(start-end),3)
        return render(request, 'info.html', {"info": "Delete Successfully!",'read_pos':"have",'time':mytime})
    except:
        return render(request, 'info.html', {"info": "Delete Unsuccessfully!",'read_pos':"have",'time':0})

def delete_singer(request, singer_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM singer WHERE singer_id=%s",[singer_id])
        end = time.time()
        mytime = round(abs(start-end),3)
        return render(request, 'info.html', {"info": "Delete Successfully!",'read_pos':"singer",'time':mytime})
    except:
        return render(request, 'info.html', {"info": "Delete Unsuccessfully!",'read_pos':"singer",'time':0})

def delete_comment(request, comment_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM comments WHERE c_id=%s",[comment_id])
        end = time.time()
        mytime = round(abs(start-end),3)
        return render(request, 'info.html', {"info": "Delete Successfully!",'read_pos':"comment",'time':mytime})
    except:
        return render(request, 'info.html', {"info": "Delete Unsuccessfully!",'read_pos':"comment",'time':0})

def delete_album(request, album_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM album WHERE album_id=%s",[album_id])
        end = time.time()
        mytime = round(abs(start-end),3)
        return render(request, 'info.html', {"info": "Delete Successfully!",'read_pos':"album",'time':mytime})
    except:
        return render(request, 'info.html', {"info": "Delete Unsuccessfully!",'read_pos':"album",'time':0})

def delete_playlist(request, list_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM playlist WHERE list_id=%s",[list_id])
        end = time.time()
        mytime = round(abs(start-end),3)
        return render(request, 'info.html', {"info": "Delete Successfully!",'read_pos':"playlist",'time':mytime})
    except:
        return render(request, 'info.html', {"info": "Delete Unsuccessfully!",'read_pos':"playlist",'time':0})

def delete_style(request, style_id):
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM style WHERE style_id=%s",[style_id])
        end = time.time()
        mytime = round(abs(start-end),3)
        return render(request, 'info.html', {"info": "Delete Successfully!",'read_pos':"style",'time':mytime})
    except:
        return render(request, 'info.html', {"info": "Delete Unsuccessfully!",'read_pos':"style",'time':0})


'''def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM song WHERE song.name=%s",[query])
            results=cursor.fetchall()
    return render(request,'base.html', {'form': form,'query': query,'results': results})'''

def style_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM style")
        rows = cursor.fetchall()
        styles = []
        for row in rows:
            style = {
                'id': row[0],
                'name': row[1],
            }
            styles.append(style)

    return render(request, 'style_list.html', {'styles': styles})


def songs_by_style(request, style_id):
    page_number = request.GET.get('page', 1)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM song WHERE style_id = %s", [style_id])
        rows = cursor.fetchall()
        songs = []
        for row in rows:
            song = {
                'id':row[0],
                'name': row[1],
                'image_url': row[2],
                'music_url': row[4],
            }
            songs.append(song)

    paginator = Paginator(songs, 10)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    style_name = ''
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM style WHERE style_id = %s", [style_id])
        result = cursor.fetchone()
        if result:
            style_name = result[0]

    return render(request, 'songs_by_style.html', {'songs': songs, 'style_name': style_name, 'page': page})


def album_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM album")
        albumdata = cursor.fetchall()
        ret1 = []
        for r in albumdata:
            d = {}
            d['album_id'] = r[0]
            d['name'] = r[1]
            d['photo__link'] = r[2]
            d['release_date'] = r[3]
            d['company'] = r[4]
            d['song_num'] = r[5]
            ret1.append(d)
        paginator = Paginator(ret1, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "album_list.html", {"page_obj": page_obj,})

def album_detail(request, album_id):
    with connection.cursor() as cursor:
        # 查询专辑的基本信息
        cursor.execute("SELECT * FROM album WHERE album_id=%s", [album_id])
        album_data = cursor.fetchone()
        album = {
            'album_id': album_data[0],
            'name': album_data[1],
            'photo__link': album_data[2],
            'release_date': album_data[3],
            'company': album_data[4],
        }
        # 查询该专辑下的所有歌曲
        cursor.execute("SELECT * FROM song WHERE album_id=%s", [album_id])
        songs_data = cursor.fetchall()
        songs = []
        for song_data in songs_data:
            song = {
                'song_id': song_data[0],
                'name': song_data[1],
                'photo_link': song_data[2],
                'lyric': song_data[3],
                'audio_link': song_data[4],
                'album_id': song_data[5],
                'singer_id': song_data[6],
                'style_id': song_data[7],
            }
            songs.append(song)
        # 将专辑信息和歌曲列表传递给模板进行渲染
        return render(request, "album_detail.html", {"album": album, "songs": songs})



