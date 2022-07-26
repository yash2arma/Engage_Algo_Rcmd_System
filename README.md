# Challenge-3 (Algorithm for Movie Recommendation)

## Overview: 

It is a personalised movie recommendation web application in which I implemented two recommendation models. Before signing in, it recommends movies using content-based filtering (used cosine similarity algorithm) which considers the cast, director, popularity, keywords, and genre of the movie. I used casts and directors for a fan-based audience. After signing in, the recommendation will be more personalised because I used a hybrid technique in which I implemented content-based and collaborative filtering (used co-clustering algorithm) together. Collaborative filtering is based on the idea that users similar to me can be used to predict how much I will like a particular product or service those users have used/experienced. Thus, recommendations will be different for different users.

## Functionalities and Features:

 * Recommendation without registration- In the application, users can search any movie without registration and get the recommendations but it is not personalised.

* Language preferences for movies- For hollywood fans, it recommends english movies and for bollywood fans, it recommends hindi movies.

* User Authentication- It uses the Flask-Login module to do access control and  authenticates user details. All the routes are secure and can only be accessed by authenticated users.

* Personalised Recommendation- For different users, recommendation will be different based on their genres interest, favourite actors and directors that  has been stored in the form of ratings.

* Movie Details- Users can see movie ratings, genres, release date, overview, casts, and read audience reviews and they can also see similar movies. All details are fetched using TMDB API keys.

* Personal Dashboard- Users can rate and add a movie to their wishlist and access all their favourite movies (Note: This option is only available after sign in).

## Tech Stack:

* Frontend- HTML, CSS, and JavaScript

* Backend- Flask Web Framework (Python)

* Database- Xampp(for storing user data on local server)

* APIs Used- TMDB API

* Libraries and Modules- Surprise scikit (for building recommender systems that deal with explicit rating data), Sklearn cosine similarity (for calculating cosine angle between the two movies), Sklearn count vectorizer (convert a collection of text documents to a matrix of token counts). 

## Algorithm Used:

I implemented cosine similariy for general recommendation and co-clustering algorithm for sorting and getting recommended movies based on users ratings i.e. collaborative filtering because it is efficient and has less RMSE, MAE, and execution time.

Average RMSE, MAE and total execution time of algorithms supported by surprise scikit library.

<img width="586" alt="Co-clustering algo" src="https://user-images.githubusercontent.com/63293447/171032769-f97e4f83-30c2-4276-b0af-37cc3cbcf6e3.png">

## Requirements:

You should have pycharm/Visual Studio IDE for running all the files and you need to import all the dependencies mention in requirements.txt file and create a database using xampp/postgresql with the name user_detail and create tables using user_detail.sql file (attached), you just need to create a server with Server and URI given below...

### 127.0.0.3:4306 and mysql://root:@127.0.0.3:4306/user_detail



