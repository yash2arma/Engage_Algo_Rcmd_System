#import dependecies
from flask import Flask,render_template,request,redirect,flash
from flask import *
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, Table
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from ast import literal_eval
from nltk.corpus import wordnet
from surprise import Reader, Dataset, CoClustering


#create database connection
local_server = True
app = Flask(__name__)
app.secret_key = "yash_engage"


#unique user access
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.3:4306/user_detail"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

@login_manager.user_loader
def load_user(user_id):
    return User_details.query.get(int(user_id))

#user details
class User_details(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(50))
    user_email = db.Column(db.String(50), unique=True)
    user_password =  db.Column(db.String(50))    

#add_to_wishlist
class user_wishlist(db.Model,UserMixin):
    movie_no = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)


#import hollywood dataset
dt= pd.read_csv("hollywood_data/hollywood_movie.csv")

#use create similarity function
titles = dt['movie_title']
indices = pd.Series(dt.index, index=dt['movie_title'])

#apply collaborative filtering
reader = Reader()
ratings = pd.read_csv('database/ratings_small.csv')
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
cc = CoClustering()
train_set = data.build_full_trainset()
cc.fit(train_set)


def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan
    
id_map = pd.read_csv('database/links_small.csv')[['movieId', 'tmdbId']]
id_map['tmdbId'] = id_map['tmdbId'].apply(convert_int)
id_map.columns = ['movieId', 'id']
id_map = id_map.merge(dt[['movie_title', 'id']], on='id').set_index('movie_title')
indices_map = id_map.set_index('id')

#personalised recommendation after singin using co-clustering algorithm
def personalised_rcmd(userId, title):
    id = indices[title]
    tmdbId = id_map.loc[title]['id']
    movie_id = id_map.loc[title]['movieId']
    data, similarity = create_similarity()
    lst = list(enumerate(similarity[int(id)]))
    lst = sorted(lst, key=lambda x: x[1], reverse=True)
    lst = lst[1:21]
    movie_indices = [i[0] for i in lst]
    movies = dt.iloc[movie_indices][['movie_title', 'vote_count', 'vote_average','year', 'id']]
    l = []
    for x in list(movies['id']):
        try:
            l.append(cc.predict(userId, indices_map.loc[x]['movieId']).l)
        except:
            l.append(0)
    movies['est'] = l
    movies = movies.sort_values('est', ascending=False)
    print(list(movies['movie_title'].head(8)))
    return list(movies['movie_title'].head(8))

# My API key
my_api_key = '946350b18b862d23ce1763b947a7e3e1'

data = pd.read_csv("hollywood_data/hollywood_movie.csv")

# Get movie id by title ENG
def get_movie_id(movie):
    movie = movie.lower()
    data['movie_title'] = data['movie_title'].str.lower()
    movie_id = list(data[data['movie_title']==movie]['id'])[0]
    return movie_id

data_hi = pd.read_csv("bollywood_data/bollywood_movie.csv")
# Get movie id by title HI
def get_movie_id_hi(movie):
    movie = movie.lower()
    data_hi['movie_title'] = data_hi['movie_title'].str.lower()
    movie_id = list(data_hi[data_hi['movie_title']==movie]['id'])[0]
    return movie_id

# links = pd.read_csv("database/links_small.csv")
# def get_YT_trailer(movie):
#     tmdb_id = get_movie_id(movie)
#     imdbid = links[links["imdbId"]==tmdb_id]
#     video_url = "https://imdb-api.com/en/API/YouTubeTrailer/k_c12pgw48/tt{}".format(imdbid)
#     video = requests.get(video_url) 
#     video = video.json()
#     link = video["videoUrl"]
#     return link
# print(get_YT_trailer("avatar"))

#Get whole movie info ENG
def get_movie_info(movie):

    l = []
    movie_id = get_movie_id(movie)

    #fetch title
    l.append(movie.title()) 

    #fetch data
    url = "https://api.themoviedb.org/3/movie/{}?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(movie_id)
    data = requests.get(url) 
    data = data.json()

    #fetch poster
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + str(poster_path)
    l.append(full_path) 

    #fetch rating
    rating = data['vote_average']
    l.append(rating) 

    #fetch runtime
    runtime = data['runtime']
    l.append(runtime)

    #fetch genre
    genres_path = data['genres']
    genrelist = []
    for i in range(len(genres_path)):
        genrelist.append(genres_path[i]['name'])
    l.append(genrelist)

    #fetch overview
    overview = data['overview']
    l.append(overview)

    #release date
    release_date = data['release_date']
    l.append(release_date)

    #vote count
    l.append(data['vote_count'])

    #tagline
    l.append(data['tagline'])

    #top-6 cast
    cast_url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(movie_id)
    cast_data = requests.get(cast_url)
    cast_data = cast_data.json()
    cast_data
    cl = []
    for i in range(len(cast_data['cast'])):
        c = []
        c.append(cast_data['cast'][i]["name"])
        c.append(cast_data['cast'][i]["character"])
        c.append("https://image.tmdb.org/t/p/w500"+ str(cast_data['cast'][i]["profile_path"]))
        cl.append(c)
    
    l.append(cl[:6])

    #fetch review
    review_url = "https://api.themoviedb.org/3/movie/{}/reviews?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(movie_id)
    review_data = requests.get(review_url)
    review_data = review_data.json()
    review_data
    rl = []
    for i in range(len(review_data['results'])):
        r = []
        r.append(review_data['results'][i]["author"])
        r.append("https://image.tmdb.org/t/p/w500"+ str(review_data['results'][i]["author_details"]["avatar_path"]))
        r.append(review_data['results'][i]["content"])
        rl.append(r)
    l.append(rl)
    return l

#Get whole movie info HI
def get_movie_info_hi(movie):

    l = []
    movie_id = get_movie_id_hi(movie)

    #fetch title
    l.append(movie.title()) 

    #fetch data
    url = "https://api.themoviedb.org/3/movie/{}?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(movie_id)
    data = requests.get(url) 
    data = data.json()

    #fetch poster
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + str(poster_path)
    l.append(full_path) 

    #fetch rating
    rating = data['vote_average']
    l.append(rating) 

    #fetch runtime
    runtime = data['runtime']
    l.append(runtime)

    #fetch genre
    genres_path = data['genres']
    genrelist = []
    for i in range(len(genres_path)):
        genrelist.append(genres_path[i]['name'])
    l.append(genrelist)

    #fetch overview
    overview = data['overview']
    l.append(overview)

    #release date
    release_date = data['release_date']
    l.append(release_date)

    #vote count
    l.append(data['vote_count'])

    #tagline
    l.append(data['tagline'])

    #top-6 cast
    cast_url = "https://api.themoviedb.org/3/movie/{}/credits?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(movie_id)
    cast_data = requests.get(cast_url)
    cast_data = cast_data.json()
    cast_data
    cl = []
    for i in range(len(cast_data['cast'])):
        c = []
        c.append(cast_data['cast'][i]["name"])
        c.append(cast_data['cast'][i]["character"])
        c.append("https://image.tmdb.org/t/p/w500"+ str(cast_data['cast'][i]["profile_path"]))
        cl.append(c)
    
    l.append(cl[:6])

    #fetch review
    review_url = "https://api.themoviedb.org/3/movie/{}/reviews?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(movie_id)
    review_data = requests.get(review_url)
    review_data = review_data.json()
    review_data
    rl = []
    for i in range(len(review_data['results'])):
        r = []
        r.append(review_data['results'][i]["author"])
        r.append("https://image.tmdb.org/t/p/w500"+ str(review_data['results'][i]["author_details"]["avatar_path"]))
        r.append(review_data['results'][i]["content"])
        rl.append(r)
    l.append(rl)
    return l

#Get Hindi movie details by title
def get_movie_detail_hi(moviel):
    doc = []


    for m in moviel:
        l = []
        id = get_movie_id_hi(m)

        #fetch title
        l.append(m.title()) 

        #fetch data
        url = "https://api.themoviedb.org/3/movie/{}?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(id)
        data = requests.get(url) 
        data = data.json()

        #fetch poster
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        l.append(full_path) 

        #fetch rating
        rating = data['vote_average']
        l.append(rating) 

        #fetch runtime
        runtime = data['runtime']
        l.append(runtime)

        #fetch genre
        genres_path = data['genres']
        genrelist = []
        for i in range(len(genres_path)):
            genrelist.append(genres_path[i]['name'])
        l.append(genrelist)

        #fetch overview
        overview = data['overview']
        l.append(overview)


        doc.append(l)
    print(doc)
    return doc

#GET English Movie by title
def get_movie_detail(moviel):
    doc = []


    for m in moviel:
        l = []
        id = get_movie_id(m)

        #fetch title
        l.append(m.title()) 

        #fetch data
        url = "https://api.themoviedb.org/3/movie/{}?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(id)
        data = requests.get(url) 
        data = data.json()

        #fetch poster
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        l.append(full_path) 

        #fetch rating
        rating = data['vote_average']
        l.append(rating) 

        #fetch runtime
        runtime = data['runtime']
        l.append(runtime)

        #fetch genre
        genres_path = data['genres']
        genrelist = []
        for i in range(len(genres_path)):
            genrelist.append(genres_path[i]['name'])
        l.append(genrelist)

        #fetch overview
        overview = data['overview']
        l.append(overview)


        doc.append(l)
    return doc

#GET English Movie by id ENG
def get_movie_detail_by_id(movie_id_list):
    doc = []
    for id in movie_id_list:

        l = []

        #fetch data
        url = "https://api.themoviedb.org/3/movie/{}?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(id)
        data = requests.get(url) 
        data = data.json()

        #fetch title - 0
        title = data["title"]
        l.append(title) 

        #fetch poster - 1
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        l.append(full_path) 

        #fetch rating - 2
        rating = data['vote_average']
        l.append(rating) 

        #fetch genre - 3
        genres_path = data['genres']
        genrelist = []
        for i in range(len(genres_path)):
            genrelist.append(genres_path[i]['name'])
        l.append(genrelist)

        #fetch overview
        overview = data['overview']
        l.append(overview)

        doc.append(l)
    return doc

#GET English Movie by id HI
def get_movie_detail_by_id_hi(movie_id_list):
    doc = []
    for id in movie_id_list:

        l = []

        #fetch data
        url = "https://api.themoviedb.org/3/movie/{}?api_key=946350b18b862d23ce1763b947a7e3e1&language=en-US".format(id)
        data = requests.get(url) 
        data = data.json()

        #fetch title - 0
        title = data["title"]
        l.append(title) 

        #fetch poster - 1
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        l.append(full_path) 

        #fetch rating - 2
        rating = data['vote_average']
        l.append(rating) 

        #fetch genre - 3
        genres_path = data['genres']
        genrelist = []
        for i in range(len(genres_path)):
            genrelist.append(genres_path[i]['name'])
        l.append(genrelist)

        #fetch overview - 4
        overview = data['overview']
        l.append(overview)

        doc.append(l)
    return doc

# similarity function ENG
def create_similarity():
    data = pd.read_csv('hollywood_data/hollywood_movie.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity

# similarity function HI
def create_similarity_hi():
    data = pd.read_csv('bollywood_data/bollywood_movie.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['describe'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity


#Normal Recommendation ENG
def rcmd(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:9] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

#Normal Recommendation HI
def rcmd_hi(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity_hi()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:9] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

#route Home ENGLISH
@app.route("/", methods=['POST','GET'])
def home_eng():
    data = pd.read_csv('hollywood_data/hollywood_movie.csv')
    data['movie_title'] = data['movie_title'].str.lower()

    high_rated_movies = data.sort_values(by=['vote_count'], ascending=False)
    top_8 = high_rated_movies.iloc[:8, :]
    top_8 = top_8['movie_title'].to_list()
    suggestions = get_movie_detail(top_8)

    oscar_movies = ["the exorcist", "good will hunting", "no country for old men", "the departed", "there will be blood", "schindler's list"]

    oscar = get_movie_detail(oscar_movies)
    return render_template("index_eng.html", suggestions=suggestions, oscar=oscar)

#route Home HINDI
@app.route("/hi", methods=['POST','GET'])
def home_hi():
    data_hi = pd.read_csv('bollywood_data/bollywood_movie.csv')
    data_hi['movie_title'] = data_hi['movie_title'].str.lower()

    high_rated_movies = data_hi.sort_values(by=['vote_count'], ascending=False)
    top_8 = high_rated_movies.iloc[:8, :]
    top_8 = top_8['movie_title'].to_list()
    suggestions = get_movie_detail_hi(top_8)

    most_wanted_movies = ["hera pheri", "taarzan: the wonder car", "barfi!", "baadshaho", "toilet: ek prem katha", "krrish 3"]
    wanted = get_movie_detail_hi(most_wanted_movies)
    return render_template("index_hi.html", suggestions=suggestions, wanted=wanted)


#route search function before signin ENG
@app.route("/normal_search", methods=['POST','GET'])
def search_normal():
    if request.method=="POST":
        try:
            movie = request.form.get("movie")
            # movie_list = movie_recommender(movie)
            movie_list = rcmd(movie)
            movie_list = np.insert (movie_list,0,movie)
            postsdata = get_movie_detail(movie_list)

            oscar_movies = ["the exorcist", "good will hunting", "no country for old men", "the departed", "there will be blood", "schindler's list"]

            oscar = get_movie_detail(oscar_movies)
            return render_template("index_eng.html", postsdata = postsdata, oscar = oscar)

        except:
            return render_template("404.html")
    return redirect(url_for('home_eng'))

#route search function before signin Hi
@app.route("/normal_search_hi", methods=['POST','GET'])
def search_normal_hi():
    if request.method=="POST":
        try:
            movie = request.form.get("movie")
            # movie_list = movie_recommender(movie)
            movie_list = rcmd_hi(movie)
            movie_list = np.insert (movie_list,0,movie)
            postsdata = get_movie_detail_hi(movie_list)

            most_wanted_movies = ["hera pheri", "taarzan: the wonder car", "barfi!", "baadshaho", "toilet: ek prem katha", "krrish 3"]

            wanted = get_movie_detail_hi(most_wanted_movies)
            return render_template("index_hi.html", postsdata = postsdata, wanted = wanted)

        except:
            return render_template("404_hi.html")
    return redirect(url_for('home_hi'))

#route dashboard after signin ENG
@app.route("/user_dashboard", methods=['POST','GET'])
@login_required
def user_dashboard():
    data = pd.read_csv('hollywood_data/hollywood_movie.csv')
    data['movie_title'] = data['movie_title'].str.lower()

    popular_movies = data.sort_values(by=['vote_count'], ascending=False)
    top_8 = popular_movies.iloc[:8, :]
    top_8 = top_8['movie_title'].to_list()
    suggestions = get_movie_detail(top_8)

    oscar_movies = ["the exorcist", "good will hunting", "no country for old men", "the departed", "there will be blood", "schindler's list"]

    oscar = get_movie_detail(oscar_movies)

    return render_template("user_dash.html", suggestions=suggestions, oscar = oscar)

#route dashboard after signin ENG
@app.route("/user_dashboard_hi", methods=['POST','GET'])
@login_required
def user_dashboard_hi():
    data = pd.read_csv('bollywood_data/bollywood_movie.csv')
    data['movie_title'] = data['movie_title'].str.lower()

    popular_movies = data.sort_values(by=['vote_count'], ascending=False)
    top_8 = popular_movies.iloc[:8, :]
    top_8 = top_8['movie_title'].to_list()
    suggestions = get_movie_detail_hi(top_8)

    most_wanted_movies = ["hera pheri", "taarzan: the wonder car", "barfi!", "baadshaho", "toilet: ek prem katha", "krrish 3"]

    wanted = get_movie_detail_hi(most_wanted_movies)

    return render_template("user_dash_hi.html", suggestions=suggestions, wanted = wanted)


#route search function after signin ENG
@app.route("/personalised_search", methods=['POST','GET'])
@login_required
def search_personalised():
    if request.method=="POST":
        try:
            user = current_user.id
            movie = request.form.get("movie").lower()
            movie_list = personalised_rcmd(user, movie)
            movie_list = np.insert (movie_list,0,movie)
            movie_list = [x.lower() for x in movie_list]
            postsdata = get_movie_detail(movie_list)

            oscar_movies = ["the exorcist", "good will hunting", "no country for old men", "the departed", "there will be blood", "schindler's list"]

            oscar = get_movie_detail(oscar_movies)
            return render_template("user_dash.html", postsdata = postsdata, oscar = oscar)

        except:
            return render_template("404_dashboard.html")

    return redirect(url_for('user_dashboard'))

#route search function after signin Hi
@app.route("/personalised_search_hi", methods=['POST','GET'])
def search_personalised_hi():
    if request.method=="POST":
        try:
            movie = request.form.get("movie")
            # movie_list = movie_recommender(movie)
            movie_list = rcmd_hi(movie)
            movie_list = np.insert (movie_list,0,movie)
            postsdata = get_movie_detail_hi(movie_list)

            most_wanted_movies = ["hera pheri", "taarzan: the wonder car", "barfi!", "baadshaho", "toilet: ek prem katha", "krrish 3"]

            wanted = get_movie_detail_hi(most_wanted_movies)
            return render_template("user_dash_hi.html", postsdata = postsdata, wanted = wanted)

        except:
            return render_template("404_dashboard_hi.html")
    return redirect(url_for('user_dashboard_hi'))

#route movie details before signin ENG
@app.route('/details1',  methods=['POST','GET'])
def movie_details_before_signin():
    if request.method == "POST":
        try:
            movie = request.form.get("movie").lower()
            movie_list = rcmd(movie)
            movie_list = np.insert (movie_list,0,movie)
            movieinfo = get_movie_info(movie)
            postsdata = get_movie_detail(movie_list)
            return render_template('movie_details1.html', movieinfo=movieinfo, postsdata = postsdata)
        except:
            return render_template('404.html')
    return redirect(url_for('home_eng'))
    

#route movie details before signin HI
@app.route('/details1_hi',  methods=['POST','GET'])
def movie_details_before_signin_hi():
    if request.method == "POST":
        try:
            movie = request.form.get("movie").lower()
            movie_list = rcmd_hi(movie)
            movie_list = np.insert (movie_list,0,movie)
            movieinfo = get_movie_info_hi(movie)
            postsdata = get_movie_detail_hi(movie_list)
            return render_template('movie_details1_hi.html', movieinfo=movieinfo, postsdata = postsdata)
        except:
            return render_template('404_hi.html')
    return redirect(url_for('home_hi'))


#route movie details after signin ENG
@app.route('/details2',  methods=['POST','GET'])
@login_required
def movie_details_after_signin():
    if request.method == "POST":
        try:
            movie = request.form.get("movie").lower()
            userid = current_user.id
            movie_list = personalised_rcmd(userid, movie)
            movie_list = np.insert (movie_list,0,movie)
            movieinfo = get_movie_info(movie)
            postsdata = get_movie_detail(movie_list)
            return render_template('movie_details2.html', movieinfo=movieinfo, postsdata = postsdata)
        except:
            return render_template('404_dashboard.html')
    return redirect(url_for('user_dashboard'))

#route movie details after signin HI
@app.route('/details2_hi',  methods=['POST','GET'])
@login_required
def movie_details_after_signin_hi():
    if request.method == "POST":
        try:
            movie = request.form.get("movie").lower()
            movie_list = rcmd_hi(movie)
            movie_list = np.insert (movie_list,0,movie)
            movieinfo = get_movie_info_hi(movie)
            postsdata = get_movie_detail_hi(movie_list)
            return render_template('movie_details2_hi.html', movieinfo=movieinfo, postsdata = postsdata)
        except:
            return render_template('404_dashboard_hi.html')
    return redirect(url_for('user_dashboard_hi'))

#route ratings to the movie ENG
@app.route('/ratings', methods=['POST','GET'])
@login_required
def give_ratings():
    if request.method == "POST":
        try:
            rate = request.form.get("rate")
            movie = request.form.get("movie").lower()
            movie_id = get_movie_id(movie)
            rating = db.engine.execute(f"INSERT INTO `movie_ratings` (`movie_no`, `user_id`, `movie_id`, `rating`, `timestamp`)  VALUES (NULL,'{current_user.id}','{movie_id}', '{rate}', NULL)")
            movie = request.form.get("movie").lower()
            userid = current_user.id
            movie_list = personalised_rcmd(userid, movie)
            movie_list = np.insert (movie_list,0,movie)
            movieinfo = get_movie_info(movie)
            postsdata = get_movie_detail(movie_list)
            flash("Rating successful!")
            return render_template('movie_details2.html', movieinfo=movieinfo, postsdata = postsdata)
        except:
            return render_template("404_server.html")
    return redirect(url_for('movie_details_after_signin'))

#route ratings to the movie HI
@app.route('/ratings_hi', methods=['POST','GET'])
@login_required
def give_ratings_hi():
    if request.method == "POST":
        try:
            rate = request.form.get("rate")
            movie = request.form.get("movie").lower()
            movie_id = get_movie_id_hi(movie)
            rating = db.engine.execute(f"INSERT INTO `movie_ratings` (`movie_no`, `user_id`, `movie_id`, `rating`, `timestamp`)  VALUES (NULL,'{current_user.id}','{movie_id}', '{rate}', NULL)")
            movie = request.form.get("movie").lower()
            movie_list = rcmd_hi(movie)
            movie_list = np.insert (movie_list,0,movie)
            movieinfo = get_movie_info_hi(movie)
            postsdata = get_movie_detail_hi(movie_list)
            flash("Rating successful!")
            return render_template('movie_details2_hi.html', movieinfo=movieinfo, postsdata = postsdata)
        except:
            return render_template("404_server_hi.html")

    return redirect(url_for('movie_details_after_signin_hi'))

#route add to wishlist ENG
@app.route('/wishlist',  methods=['POST','GET'])
@login_required
def add_to_wishlist():
    if request.method == "POST":
        try:
            movie = request.form.get("movie").lower()
            movie_id = get_movie_id(movie)

            wish = db.engine.execute(f"INSERT INTO `user_wishlist` (`movie_no`, `user_id`, `movie_id`)  VALUES (NULL,'{current_user.id}','{movie_id}')")
            userid = current_user.id
            movie = request.form.get("movie").lower()
            movie_list = personalised_rcmd(userid, movie)
            movie_list = np.insert (movie_list,0,movie)
            movieinfo = get_movie_info(movie)
            postsdata = get_movie_detail(movie_list)
            flash("Added to wishlist!")
            return render_template('movie_details2.html', movieinfo=movieinfo, postsdata = postsdata)
        except:
            return render_template("404_server.html")
    return redirect(url_for('movie_details_after_signin'))

#route add to wishlist HI
@app.route('/wishlist_hi',  methods=['POST','GET'])
@login_required
def add_to_wishlist_hi():
    if request.method == "POST":
        try:
            movie = request.form.get("movie").lower()
            movie_id = get_movie_id_hi(movie)
            wish = db.engine.execute(f"INSERT INTO `user_wishlist` (`movie_no`, `user_id`, `movie_id`)  VALUES (NULL,'{current_user.id}','{movie_id}')")
            movie = request.form.get("movie").lower()
            movie_list = rcmd_hi(movie)
            movie_list = np.insert (movie_list,0,movie)
            movieinfo = get_movie_info_hi(movie)
            postsdata = get_movie_detail_hi(movie_list)
            flash("Added to wishlist!")
            return render_template('movie_details2_hi.html', movieinfo=movieinfo, postsdata = postsdata)
        except:
            return render_template("404_server_hi.html")
    return redirect(url_for('movie_details_after_signin_hi'))

#route open wishlist ENG 
@app.route('/my_wishlist',  methods=['POST','GET'])
@login_required
def my_wishlist():
    user_id = current_user.id 
    data = user_wishlist.query.filter_by(user_id = user_id).all()

    movie_liked = []
    for i in data:
        movie_liked.append(i.movie_id)
    
    movie_liked = list(set(movie_liked))
    
    postsdata = get_movie_detail_by_id(movie_liked)
    return render_template('wishlist.html', postsdata = postsdata)

#route open wishlist HI
@app.route('/my_wishlist_hi',  methods=['POST','GET'])
@login_required
def my_wishlist_hi():
    user_id = current_user.id 
    data = user_wishlist.query.filter_by(user_id = user_id).all()

    movie_liked = []
    for i in data:
        movie_liked.append(i.movie_id)
    
    movie_liked = list(set(movie_liked))
    
    postsdata = get_movie_detail_by_id_hi(movie_liked)
    return render_template('wishlist_hi.html', postsdata = postsdata)


#route signup
@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == "POST":
        try:
            funame = request.form.get('username') 
            fumail = request.form.get('useremail')
            fupass = request.form.get('userpassword')
            user = User_details.query.filter_by(user_email = fumail).first()
            if user :
                return render_template("404_user_signup.html")
            new_user = db.engine.execute(f"INSERT INTO `user_details` (`id`, `user_name`, `user_email`, `user_password`)  VALUES (NULL, '{funame}','{fumail}','{fupass}');")

            flash("Signup Successful!")
            return render_template("signin.html")
        except:
            return render_template("404_user_signup.html")
    return render_template("signup.html")


#signin
@app.route("/signin", methods=['POST','GET'])
def signin():
    if request.method == "POST":
        try:
            uemail = request.form.get('useremail') 
            upass = request.form.get('userpassword')
            # dl  = request.form.get('ulabel')
            user = User_details.query.filter_by(user_email = uemail).first_or_404(description='There is no data with {}'.format(uemail))

            if user and user.user_password == upass:
                login_user(user)
                data = pd.read_csv('hollywood_data/hollywood_movie.csv')
                data['movie_title'] = data['movie_title'].str.lower()

                popular_movies = data.sort_values(by=['popularity'], ascending=False)
                top_8 = popular_movies.iloc[:8, :]
                top_8 = top_8['movie_title'].to_list()
                suggestions = get_movie_detail(top_8)
                flash("Signin Successful!")
                return redirect(url_for('user_dashboard'))
        except:
            return render_template("404_user_signin.html")

    return render_template("signin.html")

# signout 
@app.route('/signout')
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('home_eng'))

app.run(debug = True)