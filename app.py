
from flask import Flask,flash,redirect,render_template,url_for,request,jsonify,session,abort
from flask_session import Session
import mysql.connector
from datetime import date
from datetime import datetime
from sdmail import sendmail
from tokenreset import token
from stoken1 import token1
import os
from mysql.connector import OperationalError

from itsdangerous import URLSafeTimedSerializer
from key import *
app=Flask(__name__)
app.secret_key='hello'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
app.config['SESSION_TYPE'] = 'filesystem'
mydb=mysql.connector.connect(host='localhost',user='root',password='admin',db='music_streaming')
Session(app)
@app.route('/')
def index():
    cursor=mydb.cursor(buffered=True)
    # cursor.execute('SELECT s.album_name, s.uploaded_at,s.audio_data,s.song_picture,a.artist_name, al.album_name, al.release_year,s.song_id FROM songs s JOIN albums al ON s.album_id = al.album_id JOIN artists a ON al.artist_id = a.artist_id ORDER BY al.release_year DESC')
    # songs = cursor.fetchall()
    cursor.execute('select * from albums')
    albums = cursor.fetchall()
    print(albums)
    cursor.execute('select * from artists')
    artists = cursor.fetchall()
    cursor.execute('select * from directors')
    directors = cursor.fetchall()
    cursor.execute('select * from singers')
    singers = cursor.fetchall()
    cursor.execute('select * from songs')
    songs = cursor.fetchall()

    return render_template('index.html',a = albums,ar = artists,d = directors,s=singers,so = songs)

#=========================================Users login and register
@app.route('/ulogin',methods=['GET','POST'])
def ulogin():
    if session.get('user'):
        return redirect(url_for('index'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT count(*) from users where username=%s and password=%s',[username,password])
        count=cursor.fetchone()[0]
        if count==1:
            session['user']=username
            if not session.get(username):
                session[username]={}
            flash('sucessfully logged in')
            return redirect(url_for("index"))
        else:
            flash('Invalid username or password')
            return render_template('user_login.html')
    return render_template('user_login.html')

@app.route('/uregistration',methods=['GET','POST'])
def uregistration():
    if request.method=='POST':
        username = request.form['username']
        password=request.form['password']
        email=request.form['email']
        
        
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from users where username=%s',[username])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from users where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('user_registration.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('user_registration.html')
        
        data={'username':username,'password':password,'email':email}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('uconfirm',token=token(data,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('uregistration'))
    
    return render_template('user_registration.html')
@app.route('/uconfirm/<token>')
def uconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        cursor=mydb.cursor(buffered=True)
        id1=data['username']
        cursor.execute('select count(*) from users where username=%s',[id1])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('ulogin'))
        else:
            cursor.execute('INSERT INTO users (username,email, password) VALUES (%s,%s,%s)',[data['username'], data['email'], data['password']])

            mydb.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('ulogin'))
@app.route('/forget',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        id1=request.form['id1']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from users where username=%s',[id1])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mydb.cursor(buffered=True)

            cursor.execute('SELECT email  from users where username=%s',[id1])
            email=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('reset',token=token(id1,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('ulogin'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update  users set password=%s where username=%s',[newpassword,id1])
                mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('ulogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')
@app.route('/viewartistsongs/<artist_id>')
def viewartistsongs(artist_id):
    cursor=mydb.cursor(buffered=True)
    
    cursor.execute('select * from songs where artist_id = %s OR artist2 = %s', (artist_id, artist_id))
    artists = cursor.fetchall()
    
    return render_template('artistsongs.html',ar = artists)
@app.route('/viewsingerssongs/<singer_id>')
def viewsingerssongs(singer_id):
    cursor=mydb.cursor(buffered=True)
    
    cursor.execute('select * from songs where singer_id = %s OR singer2 = %s', (singer_id, singer_id))
    singers = cursor.fetchall()
    
    
    #print("========================",singers)
    return render_template('singers.html',s = singers)
@app.route('/viewdirectorsongs/<director_id>')
def viewdirectorsongs(director_id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from songs where director_id=%s',[director_id])
    directors = cursor.fetchall()
    

    return render_template('viewdirectorsongs.html',d = directors)

@app.route('/viewalbumsongs/<album_id>')
def viewalbumsongs(album_id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from songs where album_id=%s',[album_id])
    albums = cursor.fetchall()
   
    

    return render_template('albumsongs.html',a = albums)
@app.route('/moodsongs/<mood>')
def moodsongs(mood):
    
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from songs where FIND_IN_SET(%s, mood)',(mood,))
    mood = cursor.fetchall()
    
    return render_template('moodsongs.html', m=mood)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        cursor = mydb.cursor(buffered=True)
        cursor.execute('''
        SELECT 
            s.song_id,
            s.song_name,
            s.audio_data,
            s.song_picture,
            a.artist_name AS artist1,
            a2.artist_name AS artist2,
            al.album_name,
            d.director_name,
            si.singer_name AS singer1,
            si2.singer_name AS singer2,
            al.release_year,
            s.uploaded_at,
            s.likes,
            s.mood
        FROM 
            songs s
        Left JOIN 
            artists a ON s.artist_id = a.artist_id
        left JOIN 
            artists a2 ON s.artist2 = a2.artist_id
        left JOIN 
            albums al ON s.album_id = al.album_id
        left JOIN 
            directors d ON s.director_id = d.director_id
        left JOIN 
            singers si ON s.singer_id = si.singer_id
        left JOIN 
            singers si2 ON s.singer2 = si2.singer_id
        WHERE 
            d.director_name like %s or s.song_name like %s or a.artist_name like %s or a2.artist_name like %s or al.album_name like %s or si.singer_name like %s or si2.singer_name  like %s or s.mood like %s or s.created_by like %s COLLATE utf8mb4_general_ci
        ''',[search_term+'%',search_term+'%',search_term+'%',search_term+'%',search_term+'%',search_term+'%',search_term+'%',search_term+'%',search_term+'%'])
        search_results = cursor.fetchall()
        cursor.close()
        return render_template('searchresults.html', items=search_results)
    return render_template('home1.html')

@app.route('/likes/<song_id>',methods=['GET','POST'])
def like_song(song_id):
   if session.get('user'):
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select * from likes where user_id=%s and song_id=%s',[session.get('user'),song_id])
        lcount=cursor.fetchall()
        print(lcount)
        if request.method == 'POST':
            
            unlike = request.form['unlike']
            print(unlike)
            if unlike == 'true':
                # Unlike the song
                cursor.execute('DELETE FROM likes WHERE song_id=%s AND user_id=%s', [song_id, session.get('user')])
                mydb.commit()
                flash('Song unliked successfully')
            else:
                # Like the song
                cursor.execute('SELECT created_by FROM songs WHERE song_id=%s', [song_id])
                cid = cursor.fetchone()[0]
                cursor.execute('INSERT INTO likes (creator_id, user_id, song_id) VALUES (%s, %s, %s)', [cid, session['user'], song_id])
                mydb.commit()
                flash('Song liked successfully')

                cursor.execute('select * from likes where user_id=%s and song_id=%s',[session.get('user'),song_id])
                lcount=cursor.fetchall()
                return redirect(url_for('viewsongs', song_id=song_id))
        return redirect(url_for('viewsongs', song_id=song_id, lcount=lcount))

 
   else:
       return redirect(url_for('ulogin'))
@app.route('/viewsongs/<song_id>')
def viewsongs(song_id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('''SELECT 
                   s.song_id,
                   s.song_name,
                   s.audio_data,
                   s.song_picture,
            a.artist_name AS artist1,
            a2.artist_name AS artist2,
            al.album_name,
            d.director_name,
            si.singer_name AS singer1,
            si2.singer_name AS singer2,
            al.release_year,
            s.uploaded_at,
            s.likes,
            s.mood
            FROM 
            songs s
            LEFT JOIN 
            artists a ON s.artist_id = a.artist_id
            LEFT JOIN 
            artists a2 ON s.artist2 = a2.artist_id
            LEFT JOIN 
            albums al ON s.album_id = al.album_id
            LEFT JOIN 
            directors d ON s.director_id = d.director_id
            LEFT JOIN 
            singers si ON s.singer_id = si.singer_id
            LEFT JOIN 
            singers si2 ON s.singer2 = si2.singer_id
            WHERE 
             s.song_id = %s''', (song_id,))
    songs = cursor.fetchone()
    cursor = mydb.cursor(buffered=True)
    cursor.execute('select * from likes where user_id=%s and song_id=%s',[session.get('user'),song_id])
    lcount=cursor.fetchall()
    print(lcount)
    if lcount:
        cursor.execute('select count(*) from likes  where song_id=%s group by song_id=%s',[song_id,song_id])
        count=cursor.fetchone()[0]
        print(count)
    else:
        count=0
    return render_template('viewsongs.html',song = songs,lcount=lcount,count=count)

#=====================share song
@app.route('/sharesong/<songid>')
def sharesong(songid):
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select album_name,audio_data where blogid=%s',[songid])
        data=cursor.fetchone()
        cursor.close()
        return redirect(url_for('users_dashboard'))
    return redirect(url_for('ulogin'))
#=======favourites songs
@app.route('/add_to_favourites/<song_id>/<name>/<pic>/<audio>/<album>')
def add_to_favourites(song_id,name,pic,audio,album):
    print(session)
    if session.get('user'):
        #print(song_id,name,pic,audio,album)
        #print('-------------------',session[session['user']])
        if song_id not in session.get(session['user'], {}): 
            session.get(session['user'], {})[song_id] = [name, pic, audio, album]
            session.modified = True
            #print(session[session.get('user')])
            flash(f'{name} added to favourites')
            return redirect(url_for('viewcart'))
        else:
            flash(f'{name} is already in favorites')
        return redirect(url_for('viewcart'))
    return redirect(url_for('ulogin'))
@app.route('/viewcart')
def viewcart():
    if 'user' not in session:
        return redirect(url_for('ulogin'))
   
    songs = session.get(session['user'], {})
    if not songs:
        return 'No added favourite songs'
    return render_template('favourites.html', items=songs)
@app.route('/remove_song/<song_id>')
def remove_song(song_id):
    if session.get('user'):
        session[session.get('user')].pop(song_id)
        return redirect(url_for('viewcart'))
    return redirect(url_for('login'))
@app.route('/ulogout')
def ulogout():
    if session.get('user'):
        session.pop('user')
        flash('Successfully loged out')
        return redirect(url_for('ulogin'))
    else:
        return redirect(url_for('ulogin'))
    
'''@app.route('/users_dashboard')
def users_dashboard():
    
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT s.album_id, s.uploaded_at,s.audio_data,s.song_picture,a.artist_name, al.album_name, al.release_year,s.song_id FROM songs s JOIN albums al ON s.album_id = al.album_id JOIN artists a ON al.artist_id = a.artist_id')
    songs = cursor.fetchall()
    return render_template('users_dashboard.html',songs=songs)'''
#============================== creater registration
@app.route('/clogin',methods=['GET','POST'])
def clogin():
    if session.get('creater'):
        return redirect(url_for('creater_dashboard'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT count(*) from creater where creatername=%s and password=%s',[username,password])
        count=cursor.fetchone()[0]
        if count==1:
            session['creater']=username
            return redirect(url_for("creater_dashboard"))
        else:
            flash('Invalid username or password')
            return render_template('creater_login.html')
    return render_template('creater_login.html')

@app.route('/cregistration',methods=['GET','POST'])
def cregistration():
    if request.method=='POST':
        username = request.form['username']
        password=request.form['password']
        email=request.form['email']
        
        
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from creater where creatername=%s',[username])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from creater where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('creater_registration.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('creater_registration.html')
        
        data1={'creatername':username,'password':password,'email':email}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('cconfirm',token=token1(data1,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('cregistration'))
    
    return render_template('creater_registration.html')
@app.route('/cconfirm/<token>')
def cconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        cursor=mydb.cursor(buffered=True)
        id1=data['creatername']
        cursor.execute('select count(*) from creater where creatername=%s',[id1])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('clogin'))
        else:
            cursor.execute('INSERT INTO creater (creatername,email, password) VALUES (%s,%s,%s)',[data['creatername'], data['email'], data['password']])

            mydb.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('clogin'))
@app.route('/cforget',methods=['GET','POST'])
def cforgot():
    if request.method=='POST':
        id1=request.form['id1']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from creater where creatername=%s',[id1])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mydb.cursor(buffered=True)

            cursor.execute('SELECT email  from creater where creatername=%s',[id1])
            email=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('creset',token=token1(id1,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('clogin'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/creset/<token>',methods=['GET','POST'])
def creset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update creater set password=%s where creatername=%s',[newpassword,id1])
                mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('clogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')
@app.route('/clogout')
def clogout():
    if session.get('creater'):
        session.pop('creater')
        flash('Successfully loged out')
        return redirect(url_for('clogin'))
    else:
        return redirect(url_for('clogin'))
@app.route('/creater_dashboard')
def creater_dashboard():
    if session.get('creater'):
        return render_template('creater_dashboard.html')
    return redirect(url_for('clogin'))

#==================upload music data
import random
def genotp():
    u_c=[chr(i) for i in range(ord('A'),ord('Z')+1)]
    l_c=[chr(i) for i in range(ord('a'),ord('z')+1)]
    otp=''
    for i in range(3):
        otp+=random.choice(u_c)
        otp+=str(random.randint(0,9))
        otp+=random.choice(l_c)
    return otp
'''@app.route('/uploadmusic',methods=['GET','POST'])
def uploadmusic():
    if session.get('creater'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT artist_name FROM artists WHERE created_by = %s', (session['creater'],))
        existing_artists = cursor.fetchall()

        cursor.execute('SELECT album_name FROM albums WHERE created_by = %s', (session['creater'],))
        existing_albums = cursor.fetchall()
        if request.method=="POST":
            id1_pic=genotp()  # Generate unique id for picture
            id1_audio=genotp()
            album_name=request.form['album_name']
            audio_file=request.files['audio_file']
            song_picture=request.files['song_picture']
            artist_name=request.form['artist_name']
            album_name=request.form['album_name']
            release_year=request.form['release_year']
            new_artist= request.form['new_artist']
            new_album = request.form['new_album']
            if new_artist !=None:
                cursor.execute('SELECT artist_id FROM artists WHERE artist_name = %s AND created_by = %s', (artist_name, session['creater']))
                artist_record = cursor.fetchone()

            if artist_record:
                artist_id = artist_record[0]
            else:
                # Insert the artist if it doesn't exist
                cursor.execute('INSERT INTO artists (artist_name, created_by) VALUES (%s, %s)', (new_artist, session['creater']))
                mydb.commit()
                artist_id = cursor.lastrowid
            if new_album!=None:
                cursor.execute('SELECT album_id FROM albums WHERE album_name = %s AND created_by = %s', (album_name, session['creater']))
            album_record = cursor.fetchone()

            if album_record:
                album_id = album_record[0]
            else:
                # Insert the album if it doesn't exist
                cursor.execute('INSERT INTO albums (album_name, release_year, artist_id, created_by,album_name) VALUES (%s, %s, %s, %s,%s)', (album_name, release_year, artist_id, session['creater'],album_name))
                
                flash('album added sucessfully')
                mydb.commit()
                album_id = cursor.lastrowid

            #album_name=request.form['album_name']
            filename=id1_pic+'.jpg'#picture
            audio_filename = id1_audio + '.mp3'#audio
            cursor.execute('SELECT song_id FROM songs WHERE song_name = %s AND album_id = %s AND created_by = %s',
                           (album_name, album_id, session['creater']))
            existing_song = cursor.fetchone()

            if existing_song:
                flash('This song already exists in the album.')
                return redirect(url_for('uploadmusic'))
            cursor.execute('SELECT artist_id FROM artists WHERE artist_name = %s AND created_by = %s', (artist_name, session['creater']))
            artist_record = cursor.fetchone()

            if artist_record:
                artist_id = artist_record[0]
            else:
                # Insert the artist if it doesn't exist
                cursor.execute('INSERT INTO artists (artist_name, created_by) VALUES (%s, %s)', (artist_name, session['creater']))
                mydb.commit()
                artist_id = cursor.lastrowid

            # Check if the album already exists for the current user
            cursor.execute('SELECT album_id FROM albums WHERE album_name = %s AND created_by = %s', (album_name, session['creater']))
            album_record = cursor.fetchone()

            if album_record:
                album_id = album_record[0]
            else:
                # Insert the album if it doesn't exist
                cursor.execute('INSERT INTO albums (album_name, release_year, artist_id, created_by,album_name) VALUES (%s, %s, %s, %s,%s)', (album_name, release_year, artist_id, session['creater'],album_name))
                
                flash('album added sucessfully')
                mydb.commit()
                album_id = cursor.lastrowid
            audio_filename = id1_audio + '.mp3'
            audio_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', audio_filename)
            if not os.path.exists(audio_path):
                os.makedirs(audio_path,exist_ok=True)
            audio_file.save(audio_path)

            upload_date = datetime.now()
            cursor.execute('INSERT INTO songs (album_name, audio_data, song_picture, album_id, created_by, uploaded_at,album_name) VALUES (%s, %s, %s, %s, %s, %s,%s)', (album_name, id1_audio, id1_pic, album_id, session['creater'], upload_date,album_name))
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
            song_picture.save(os.path.join(path, filename))
            flash(f'song {album_name} of {album_name} uploaded sucessfully!' )
            mydb.commit()

            return redirect(url_for('songsdashboard'))

        return render_template('upload_music.html',artists=existing_artists,albums=existing_albums)
    return redirect(url_for('clogin'))'''

'''
#============================ creater upload music
@app.route('/upload_music',methods=['GET','POST'])
def uploadmusic():
    if session.get('creater'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from artists')
        artist = cursor.fetchall()
        cursor.execute('select * from albums')
        album = cursor.fetchall()
        cursor.execute('select * from directors')
        directors = cursor.fetchall()
        cursor.execute('select * from singers')
        singers = cursor.fetchall()
        cursor.close()
        if request.method=="POST":
            print("========================  POST DATA ==============================")
            song_name = request.form['song_name']
            cursor=mydb.cursor(buffered=True)
            cursor.execute("SELECT * FROM songs WHERE song_name = %s AND created_by = %s", (song_name, session['creater']))
            existing_song = cursor.fetchone()
            cursor.close()
            if existing_song:
                flash(f"You have already added '{song_name}' before.")
                return redirect(url_for('uploadmusic'))
            mood_list = request.form.getlist('mood')
            # Convert the mood list to a string for database insertion
            mood_str = ','.join(mood_list) if mood_list else None
            audio_file = request.files['audio_file']
            song_picture = request.files['song_picture']
            release_year = request.form['release_year']
            new_director = request.form['new_director']
            new_singer = request.form['new_singer']
            new_artist = request.form['new_artist']
            new_album = request.form['new_album']
            # Director=request.form['Director']
            # print(new_artist,1)
            # print(new_album,2)
            # print(new_director,3)
            # print(new_singer,4)
            
            if 'Director' in request.form:
                Director = request.form['Director']
            if 'singers' in request.form:
                singers = request.form['singers']
            if 'artist_name' in request.form:
                artist_name = request.form['artist_name']
            if 'album_name' in request.form:
                album_name = request.form['album_name']
            # print(artist_name,1)
            # print(album_name,2)
            # print(Director,3)
            # print(singers,4)
            if new_director:
                new_director = request.form['new_director']
                director_image = request.files['director_image']
                cursor=mydb.cursor(buffered=True)
                cursor.execute("SELECT * FROM directors WHERE director_name = %s", (new_director,))
                existing_director = cursor.fetchone()
                cursor.close()
                if existing_director:
                    flash(f"{new_director} Director already exists in the database.")
                    return redirect(url_for('uploadmusic'))
                else:
                    filename=new_director+'.jpg'
                    d_id = genotp()
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into directors (director_name,director_pic,created_by) values (%s,%s,%s) ',[new_director,d_id,session['creater']])

                    path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                    if not os.path.exists(path):
                        os.makedirs(path,exist_ok=True)
            
                    director_image.save(os.path.join(path, filename))
                    mydb.commit()

                    cursor.execute('select director_id from directors where director_name=%s',[new_director])
                    n_director_id = cursor.fetchone()[0]
                    cursor.close()
            # else:
            #     Director=request.form['Director']

            if new_singer:
                new_singer = request.form['new_singer']
                singer_image = request.files['singer_image']
                cursor=mydb.cursor(buffered=True)
                cursor.execute("SELECT * FROM singers WHERE singer_name = %s", (new_singer,))
                existing_singer = cursor.fetchone()
                cursor.close()
                if existing_singer:
                    flash(f"{new_singer} singer already exists in the database.")
                    return redirect(url_for('uploadmusic'))
                else:
                    s_id = genotp()
                    filename=new_singer+'.jpg'
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into singers (singer_name,singer_pic,created_by) values (%s,%s,%s) ',[new_singer,s_id,session['creater']])
                    path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                    if not os.path.exists(path):
                        os.makedirs(path,exist_ok=True)
            
                    singer_image.save(os.path.join(path, filename))
                    mydb.commit()

                    cursor.execute('select singer_id from singers where singer_name=%s',[new_singer])
                    n_singer_id = cursor.fetchone()[0]
                    cursor.close()
            # else:
            #     singers = request.form['singers']
            if new_artist:
                new_artist = request.form['new_artist']
                artist_image = request.files['artist_image']
                cursor=mydb.cursor(buffered=True)
                cursor.execute("SELECT * FROM artists WHERE artist_name = %s", (new_artist,))
                existing_artist = cursor.fetchone()
                cursor.close()
                if existing_artist:
                    flash(f"{new_artist} artist already exists in the database.")
                    return redirect(url_for('uploadmusic'))
                else:
                    art_id = genotp()
                    filename=new_artist+'.jpg'
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into artists (artist_name,created_by,artist_pic) values (%s,%s,%s) ',[new_artist,session['creater'],art_id])
                    path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                    if not os.path.exists(path):
                        os.makedirs(path,exist_ok=True)
            
                    artist_image.save(os.path.join(path, filename))
                    mydb.commit()

                    cursor.execute('select artist_id from artists where artist_name=%s',[new_artist])
                    n_artist_id = cursor.fetchone()[0]
                    cursor.close()

            # else:
            #     artist_name = request.form['artist_name']
            if new_album: 
                new_album = request.form['new_album']
                album_image = request.files['album_image']
                cursor=mydb.cursor(buffered=True)
                cursor.execute("SELECT * FROM albums WHERE album_name = %s", (new_album,))
                existing_album = cursor.fetchone()
                cursor.close()
                if existing_album:
                    flash(f"{new_album} already exists in the database.")
                    return redirect(url_for('uploadmusic'))
                else:
                    alb_id = genotp()
                    filename=new_album+'.jpg'
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into albums (album_name,release_year,created_by,album_pic) values (%s,%s,%s,%s) ',[new_album,release_year,session['creater'],alb_id])

                    path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                    if not os.path.exists(path):
                        os.makedirs(path,exist_ok=True)
            
                    album_image.save(os.path.join(path, filename))
                    mydb.commit()

                    cursor.execute('select album_id from albums where album_name=%s',[new_album])
                    n_alnum_id = cursor.fetchone()[0]
                    # print(n_alnum_id)
                    cursor.close()

            # else:
            #     album_name = request.form['album_name']
            
            audio_id = genotp()
            song_id = genotp()
            filename=song_name+song_id+'.jpg'
            filename1 = song_name+audio_id+'.mp3'
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
    
            song_picture.save(os.path.join(path, filename))
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
    
            audio_file.save(os.path.join(path, filename1))
            present_date = datetime.now().date()
            # cursor.execute('select directors_pic from songs where directors=%s',[Director])
            # director_id = cursor.fetchone()
            # cursor.execute('select singers_image from songs where singers_names=%s',[singers])
            # singer_i = cursor.fetchone()
            #print((song_name,release_year, song_name+audio_id, song_name+song_id,mood_str,album_name if 'album_name' in request.form else n_alnum_id[0], session['creater'],present_date,artist_name if 'artist_name' in request.form else n_artist_id[0],Director[0] if 'Director' in  request.form else n_director_id[0],singers if 'singers' in request.form else n_singer_id[0]))
        
            cursor=mydb.cursor(buffered=True)
            x  = cursor.execute('INSERT INTO songs (song_name,release_date, audio_data, song_picture,mood,album_id, created_by,uploaded_at,artist_id,director_id,singer_id) VALUES (%s, %s, %s, %s,%s,%s, %s, %s,%s,%s, %s)',
                           (song_name,release_year, song_name+audio_id, song_name+song_id,mood_str,album_name if request.form['album_name'] else n_alnum_id, session['creater'],present_date,artist_name if request.form['artist_name'] else n_artist_id,Director if request.form['Director'] else n_director_id,singers if request.form['singers'] else n_singer_id))
            
            # Commit the insertion
            mydb.commit()
            cursor.close()
            flash(f'{song_name} added sucessfully!')
            return redirect(url_for('songsdashboard'))
            

        return render_template('upload_music.html',a = artist,al=album,d= directors,s=singers)
    return redirect(url_for('clogin'))#=========================== Songs Dashboard'''

@app.route('/songs_dashboard/<sid>')
def songsdashboard(sid):
    cursor = mydb.cursor(buffered=True)
    if session.get('creater'):
        cursor.execute('''SELECT 
            s.song_id,
            s.song_name,
            s.audio_data,
            s.song_picture,
            a.artist_name AS artist1,
            a2.artist_name AS artist2,
            al.album_name,
            d.director_name,
            si.singer_name AS singer1,
            si2.singer_name AS singer2,
            al.release_year,
            s.uploaded_at,
            s.likes,
            s.mood
            FROM 
            songs s
            LEFT JOIN 
            artists a ON s.artist_id = a.artist_id
            LEFT JOIN 
            artists a2 ON s.artist2 = a2.artist_id
            LEFT JOIN 
            albums al ON s.album_id = al.album_id
            LEFT JOIN 
            directors d ON s.director_id = d.director_id
            LEFT JOIN 
            singers si ON s.singer_id = si.singer_id
            LEFT JOIN 
            singers si2 ON s.singer2 = si2.singer_id
            WHERE 
            s.created_by = %s AND s.song_id = %s''', (session['creater'], sid))

        song = cursor.fetchone()  # Fetch only one song
        #print("=================================", song)
        
        cursor.execute('select count(*) from likes where song_id=%s group by song_id=%s',[sid,sid])

        count=cursor.fetchone()
        if count:
            count=count[0]
        else:
            count=0



        return render_template('creater_songs_dashboard.html', song=song,count=count)  # Pass 'song' instead of 'songs'
    else:
        return redirect(url_for('clogin'))
@app.route('/creater_all_songs')
def creater_all_songs():
    if session.get('creater'):
        cursor = mydb.cursor(buffered=True)
        cursor.execute('''SELECT 
                                s.song_id,
                                s.song_name,
                                s.song_picture,
                                al.album_name,
                                a.artist_name AS artist1,
                                a2.artist_name AS artist2,  -- Added artist2 alias
                                si.singer_name AS singer1,
                                si2.singer_name AS singer2  -- Added singer2 alias
                          FROM 
                                songs s
                          LEFT JOIN 
                                artists a ON s.artist_id = a.artist_id
                          LEFT JOIN 
                                artists a2 ON s.artist2 = a2.artist_id  -- Joining artist2 based on the artist2 column in songs table
                          LEFT JOIN 
                                albums al ON s.album_id = al.album_id
                          LEFT JOIN 
                                singers si ON s.singer_id = si.singer_id
                          LEFT JOIN 
                                singers si2 ON s.singer2 = si2.singer_id  -- Joining singer2 based on the singer2 column in songs table
                          WHERE 
                                s.created_by = %s''', [session['creater']])

        songs_info = cursor.fetchall()
        return render_template('creater_songs_1.html', songs_info=songs_info)
    else:
        return redirect(url_for('clogin'))




@app.route('/upload_music',methods=['GET','POST'])
def uploadmusic():
    if session.get('creater'):
        if mydb.is_connected():
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select * from artists')
            artist = cursor.fetchall()
            cursor.execute('select * from albums')
            album = cursor.fetchall()
            cursor.execute('select * from directors')
            directors = cursor.fetchall()
            cursor.execute('select * from singers')
            singers = cursor.fetchall()
            
            if request.method=="POST":
                #print("========================  POST DATA ==============================")
                song_name = request.form['song_name']
                
                cursor.execute("SELECT * FROM songs WHERE song_name = %s AND created_by = %s", (song_name, session['creater']))
                existing_song = cursor.fetchone()
                
                if existing_song:
                    flash(f"You have already added '{song_name}' before.")
                    return redirect(url_for('uploadmusic'))
                mood_list = request.form.getlist('mood')
                # Convert the mood list to a string for database insertion
                mood_str = ','.join(mood_list) if mood_list else None
                audio_file = request.files['audio_file']
                song_picture = request.files['song_picture']
                release_year = request.form['release_year']
                new_director = request.form['new_director']
                new_singer = request.form['new_singer']
                new_singer_2 = request.form['new_singer_2']
                new_artist = request.form['new_artist']
                new_artist_2 = request.form['new_artist_2']
                new_album = request.form['new_album']

                # Director=request.form['Director']
                # print(new_artist,1)
                # print(new_album,2)
                # print(new_director,3)
                # print(new_singer,4)
                print(new_artist_2,1)
                
                if 'Director' in request.form:
                    Director = request.form['Director']
                if 'singers' in request.form:
                    singers = request.form['singers']
                if 'singers_2' in request.form:
                    singers_2 = request.form['singers_2']
                if 'artist_name' in request.form:
                    artist_name = request.form['artist_name']
                if 'artist_name_2' in request.form:
                    artist_name_2 = request.form['artist_name_2']
                if 'album_name' in request.form:
                    album_name = request.form['album_name']
                # print(artist_name,1)
                # print(album_name,2)
                # print(Director,3)
                # print(singers,4)
                if new_director:
                    new_director = request.form['new_director']
                    director_image = request.files['director_image']
                    
                    cursor.execute("SELECT * FROM directors WHERE director_name = %s", (new_director,))
                    existing_director = cursor.fetchone()
                    
                    if existing_director:
                        flash(f"{new_director} Director already exists in the database.")
                        return redirect(url_for('uploadmusic'))
                    else:
                        
                        d_id = genotp()
                        filename=new_director+d_id+'.jpg'
                        
                        cursor.execute('insert into directors (director_name,director_pic,created_by) values (%s,%s,%s) ',[new_director,new_director+d_id,session['creater']])
                        
                        path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                        if not os.path.exists(path):
                            os.makedirs(path,exist_ok=True)
                
                        director_image.save(os.path.join(path, filename))
                        mydb.commit()

                        cursor.execute('select director_id from directors where director_name=%s',[new_director])
                        n_director_id = cursor.fetchone()[0]
                        
                # else:
                #     Director=request.form['Director']

                if new_singer:
                    new_singer = request.form['new_singer']
                    singer_image = request.files['singer_image']
                    
                    cursor.execute("SELECT * FROM singers WHERE singer_name = %s", (new_singer,))
                    existing_singer = cursor.fetchone()
                    
                    if existing_singer:
                        flash(f"{new_singer} singer already exists in the database.")
                        return redirect(url_for('uploadmusic'))
                    else:
                        s_id = genotp()
                        filename=new_singer+s_id+'.jpg'
                        
                        cursor.execute('insert into singers (singer_name,singer_pic,created_by) values (%s,%s,%s) ',[new_singer,new_singer+s_id,session['creater']])
                        path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                        if not os.path.exists(path):
                            os.makedirs(path,exist_ok=True)
                
                        singer_image.save(os.path.join(path, filename))
                        mydb.commit()

                        cursor.execute('select singer_id from singers where singer_name=%s',[new_singer])
                        n_singer_id = cursor.fetchone()[0]
                        
                if new_singer_2:
                    
                    singer_image_2 = request.files['singer_image_2']
                    
                    cursor.execute("SELECT * FROM singers WHERE singer_name = %s", (new_singer_2,))
                    existing_singer = cursor.fetchone()
                    
                    if existing_singer:
                        flash(f"{new_singer_2} singer already exists in the database.")
                        return redirect(url_for('uploadmusic'))
                    else:
                        s_id = genotp()
                        filename=new_singer_2+s_id+'.jpg'
                        
                        cursor.execute('insert into singers (singer_name,singer_pic,created_by) values (%s,%s,%s) ',[new_singer_2,new_singer_2+s_id,session['creater']])
                        path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                        if not os.path.exists(path):
                            os.makedirs(path,exist_ok=True)
                
                        singer_image_2.save(os.path.join(path, filename))
                        mydb.commit()

                        cursor.execute('select singer_id from singers where singer_name=%s',[new_singer_2])
                        n_singer_id_2 = cursor.fetchone()[0]
                        
                else:
                    n_singer_id_2=None
                
                # else:
                #     singers = request.form['singers']
                if new_artist:
                    new_artist = request.form['new_artist']
                    artist_image = request.files['artist_image']
                    
                    cursor.execute("SELECT * FROM artists WHERE artist_name = %s", (new_artist,))
                    existing_artist = cursor.fetchone()
                    
                    if existing_artist:
                        flash(f"{new_artist} artist already exists in the database.")
                        return redirect(url_for('uploadmusic'))
                    else:
                        art_id = genotp()
                        filename=new_artist+art_id+'.jpg'
                        
                        cursor.execute('insert into artists (artist_name,created_by,artist_pic) values (%s,%s,%s) ',[new_artist,session['creater'],new_artist+art_id])
                        path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                        if not os.path.exists(path):
                            os.makedirs(path,exist_ok=True)
                
                        artist_image.save(os.path.join(path, filename))
                        mydb.commit()

                        cursor.execute('select artist_id from artists where artist_name=%s',[new_artist])
                        n_artist_id = cursor.fetchone()[0]
                        
                if new_artist_2:

                    artist_image = request.files['artist_image']
                    
                    cursor.execute("SELECT * FROM artists WHERE artist_name = %s", (new_artist_2,))
                    existing_artist = cursor.fetchone()
                    
                    if existing_artist:
                        flash(f"{new_artist_2} artist already exists in the database.")
                        return redirect(url_for('uploadmusic'))
                    else:
                        art_id = genotp()
                        filename=new_artist_2+art_id+'.jpg'
                        
                        cursor.execute('insert into artists (artist_name,created_by,artist_pic) values (%s,%s,%s) ',[new_artist_2,session['creater'],new_artist_2+art_id])
                        path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                        if not os.path.exists(path):
                            os.makedirs(path,exist_ok=True)
                
                        artist_image.save(os.path.join(path, filename))
                        mydb.commit()

                        cursor.execute('select artist_id from artists where artist_name=%s',[new_artist_2])
                        n_artist_id2 = cursor.fetchone()[0]
                        print(n_artist_id2)
                        
                else:
                    n_artist_id2=None

                # else:
                #     artist_name = request.form['artist_name']
                if new_album: 
                    new_album = request.form['new_album']
                    album_image = request.files['album_image']
                    
                    cursor.execute("SELECT * FROM albums WHERE album_name = %s", (new_album,))
                    existing_album = cursor.fetchone()
                    
                    if existing_album:
                        flash(f"{new_album} already exists in the database.")
                        return redirect(url_for('uploadmusic'))
                    else:
                        alb_id = genotp()
                        filename=new_album+alb_id+'.jpg'
                        
                        cursor.execute('insert into albums (album_name,release_year,created_by,album_pic) values (%s,%s,%s,%s) ',[new_album,release_year,session['creater'],new_album+alb_id])

                        path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                        if not os.path.exists(path):
                            os.makedirs(path,exist_ok=True)
                
                        album_image.save(os.path.join(path, filename))
                        mydb.commit()

                        cursor.execute('select album_id from albums where album_name=%s',[new_album])
                        n_alnum_id = cursor.fetchone()[0]
                        # print(n_alnum_id)
                        

                # else:
                #     album_name = request.form['album_name']
                
                audio_id = genotp()
                song_id = genotp()
                filename=song_name+song_id+'.jpg'
                filename1 = song_name+audio_id+'.mp3'
                path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                if not os.path.exists(path):
                    os.makedirs(path,exist_ok=True)
        
                song_picture.save(os.path.join(path, filename))
                path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'static')
                if not os.path.exists(path):
                    os.makedirs(path,exist_ok=True)
        
                audio_file.save(os.path.join(path, filename1))
                present_date = datetime.now().date()
                # cursor.execute('select directors_pic from songs where directors=%s',[Director])
                # director_id = cursor.fetchone()
                # cursor.execute('select singers_image from songs where singers_names=%s',[singers])
                # singer_i = cursor.fetchone()
                #print((song_name,release_year, song_name+audio_id, song_name+song_id,mood_str,album_name if 'album_name' in request.form else n_alnum_id[0], session['creater'],present_date,artist_name if 'artist_name' in request.form else n_artist_id[0],Director[0] if 'Director' in  request.form else n_director_id[0],singers if 'singers' in request.form else n_singer_id[0]))
            
                
                x  = cursor.execute('INSERT INTO songs (song_name,release_date, audio_data, song_picture,mood,album_id, created_by,uploaded_at,artist_id,director_id,singer_id,artist2,singer2) VALUES (%s, %s, %s, %s,%s,%s, %s, %s,%s,%s, %s,%s,%s)',
                            (song_name,release_year, song_name+audio_id, song_name+song_id,mood_str,album_name if request.form['album_name'] else n_alnum_id, session['creater'],present_date,artist_name if request.form['artist_name'] else n_artist_id,Director if request.form['Director'] else n_director_id,singers if request.form['singers'] else n_singer_id,artist_name_2 if request.form['artist_name_2'] else n_artist_id2,singers_2 if request.form['singers_2'] else n_singer_id_2))
                
                # Commit the insertion
                mydb.commit()
             
                flash(f'{song_name} added sucessfully!')
                return redirect(url_for('creater_all_songs'))
                

            return render_template('upload_music.html',a = artist,al=album,d= directors,s=singers)
        else:
             print("MySQL connection is not available.")
    return redirect(url_for('clogin'))
@app.route('/delete_song/<int:song_id>', methods=['GET','POST'])
def delete_song(song_id):
    if session.get('creater'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('SELECT song_picture FROM songs WHERE song_id = %s and  created_by = %s', [song_id,session['creater'],])
        image_filename = cursor.fetchone()[0]  # Get the image filename
        #print('==================================',image_filename)
      
        path_to_image = os.path.join(app.config['UPLOAD_FOLDER'], image_filename+'.jpg')
        #print("=======================================",path_to_image)
        if os.path.exists(path_to_image):
            #print('=================================,the path exists')
            os.remove(path_to_image)  # Delete the image file from the static folder
        cursor.execute('SELECT audio_data FROM songs WHERE song_id = %s and  created_by = %s', [song_id,session['creater'],])
        audio_filename = cursor.fetchone()[0]  # Get the image filename
      
        path_to_audio = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename+'.mp3')
        #print("=======================================",path_to_image)
        if os.path.exists(path_to_audio):
            #print('=================================,the path exists')
            os.remove(path_to_audio)  # Delete the audio file from the static folder
        
        cursor.execute('DELETE FROM likes WHERE song_id = %s AND creator_id = %s', (song_id, session['creater']))

        cursor.execute('DELETE FROM songs WHERE song_id = %s AND created_by = %s', (song_id, session['creater']))
        mydb.commit()
       
        flash('song deleted sucessfully')
        return redirect(url_for('creater_all_songs'))
    return redirect(url_for('clogin'))
@app.route('/update_song/<song_id>',methods=['GET','POST'])
def updatesong(song_id):
    if session.get('creater'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('''SELECT 
            s.song_id,
            s.song_name,
            s.release_date,
            s.audio_data,
            s.song_picture,
            s.mood,
            al.album_id,
            al.album_name,
            al.release_year AS album_release_year,
            a1.artist_id AS artist1_id,
            a1.artist_name AS artist1_name,
            a2.artist_id AS artist2_id,
            a2.artist_name AS artist2_name,
            d.director_id,
            d.director_name,
            si1.singer_id AS singer1_id,
            si1.singer_name AS singer1_name,
            si2.singer_id AS singer2_id,
            si2.singer_name AS singer2_name
        FROM 
            songs s
        LEFT JOIN 
            albums al ON s.album_id = al.album_id
        LEFT JOIN 
            artists a1 ON s.artist_id = a1.artist_id
        LEFT JOIN 
            artists a2 ON s.artist2 = a2.artist_id
        LEFT JOIN 
            directors d ON s.director_id = d.director_id
        LEFT JOIN 
            singers si1 ON s.singer_id = si1.singer_id
        LEFT JOIN 
            singers si2 ON s.singer2 = si2.singer_id
        WHERE 
            s.song_id =%s AND s.created_by = %s
        GROUP BY 
            s.song_id;
        ''',(song_id,session['creater']))
        songs = cursor.fetchone()
        if request.method=="POST":
            song_name= request.form['song_name']
            release_date = request.form['release_date']
            mood_list = request.form.getlist('mood[]')
            print(mood_list)
            mood_str = ','.join(mood_list)
            print('=======',mood_str)
            album_name = request.form['album_name']
            artist_name = request.form['artist_name']
            print(artist_name)
            artist2 = request.form['artist2']
            print(artist2)
            singer_name = request.form['singer_name']
            singer2 = request.form['singer2']
            director_name = request.form['director_name']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from albums where album_name=%s',[album_name])
            count=cursor.fetchone()[0]
            cursor.execute('SELECT album_id FROM songs WHERE song_id = %s and created_by=%s', [song_id,session['creater']])
            album_id = cursor.fetchone()[0]
            
            # print('=================================',album_name)
            # print('================================',album_id)
            # print('=====================',session['creater'])
            cursor.execute('update albums set album_name =%s where created_by=%s and album_id=%s',(album_name,session['creater'],album_id))
            mydb.commit()
            cursor.execute('select director_id from songs where song_id=%s and created_by=%s',(song_id,session['creater']))
            director_id = cursor.fetchone()[0]
            cursor.execute('update directors set director_name =%s where created_by=%s and director_id=%s',(director_name,session['creater'],director_id))
            mydb.commit()
            cursor.execute('SELECT artist_id FROM songs WHERE song_id = %s and created_by=%s', (song_id,session['creater'])) 
            artist1_id = cursor.fetchone()[0]
            print(artist1_id)
            cursor.execute('update artists set  artist_name=%s where artist_id=%s',(artist_name,artist1_id))
            mydb.commit()
            cursor.execute('SELECT singer_id FROM songs WHERE song_id = %s', [song_id]) 

            singer1_id = cursor.fetchone()[0]
            cursor.execute('update singers set singer_name=%s where singer_id=%s',(singer_name,singer1_id))
            if singer2 !=None:
                cursor.execute('SELECT singer2 FROM songs WHERE  song_id= %s', (song_id,)) 
                singer2_id = cursor.fetchone()[0]
                cursor.execute('update singers set singer_name=%s where singer_id=%s',(singer2,singer2_id))
                mydb.commit()
            if artist2!=None:
                cursor.execute('SELECT artist2 FROM songs WHERE  song_id= %s', (song_id,)) 
                artist2_id = cursor.fetchone()[0]
                print(artist2_id)
                cursor.execute('update artists set  artist_name=%s where artist_id=%s',(artist2,artist2_id)) 
                mydb.commit()   
            # cursor.execute('select song_id from songs where song_name=%s and created_by=%s',(song_name,session['creater']))
            # song_id = cursor.fetchone()[0]
            print('=========================',cursor.execute('update songs set song_name =%s,release_date = %s,mood =%s where song_id=%s and created_by=%s',(song_name,release_date,mood_str,song_id,session['creater'])))
            mydb.commit()
            flash('songs updated successfully!')
            return redirect(url_for('creater_all_songs'))

            

        return render_template('creater_update_song.html',i = songs)
    else:
        return redirect(url_for('clogin'))
app.run(use_reloader=True,debug=True)

