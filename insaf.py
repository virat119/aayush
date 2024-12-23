
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Website URL
base_url = "https://www.movieshdbox.site"

# Function to get movie categories
def get_movie_categories():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    category_links = []
    folders = soup.find_all("div", class_="folder")
    
    for folder in folders:
        link = folder.find("a")["href"]
        category_links.append(link)
    
    return category_links

# Function to scrape movies from a category
def scrape_movies_from_category(category_url):
    full_url = base_url + "/" + category_url
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    movie_cards = soup.find_all("div", class_="movie-card")
    movies = []
    
    for card in movie_cards:
        title = card.find("div", class_="movie-title").text.strip()
        poster = card.find("img")["src"]
        file_size = card.find("div", class_="file-size").text.strip()
        download_link = card.find("a", class_="download-button")["href"]
        
        movies.append({
            "title": title,
            "poster": poster,
            "file_size": file_size,
            "download_link": download_link
        })
    
    return movies

# API to search movies
@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')  # Search query ko get kar rahe hain
    all_movies = []
    
    # Har category se movies ko scrape kar rahe hain
    categories = get_movie_categories()
    for category in categories:
        movies = scrape_movies_from_category(category)
        all_movies.extend(movies)
    
    # Movies ko search query ke hisaab se filter kar rahe hain
    filtered_movies = [movie for movie in all_movies if query.lower() in movie["title"].lower()]
    
    return jsonify(filtered_movies)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Flask ko 0.0.0.0 
