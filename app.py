from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load API keys from .env
load_dotenv()

# OMDb API configuration
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
OMDB_BASE_URL = "http://www.omdbapi.com/"

# Check if API key is loaded
if not OMDB_API_KEY:
    raise ValueError("OMDB_API_KEY not found in environment variables. Please check your .env file or set it in your deployment platform.")

app = Flask(__name__)

# Configure Flask for production
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_ENV') != 'production'

# Movie database organized by mood and language
def get_movie_titles_by_mood_and_language(mood, language):
    """Get 15 movie titles based on mood and language"""
    
    movie_database = {
        "Sad": {
            "Kannada": [
                "U Turn", "Thithi", "Godhi Banna Sadharana Mykattu", "Lucia", "RangiTaranga",
                "Shuddhi", "Nathicharami", "Aa Karaala Ratri", "Kanoora Heggadati", "Hejjegalu",
                "Rama Rama Re", "Mani", "Ondanondu Kaladalli", "Ghatashraddha", "Chomana Dudi"
            ],
            "Hindi": [
                "Taare Zameen Par", "My Name is Khan", "Anand", "Sadma", "Masaan",
                "The Lunchbox", "October", "Tumhari Sulu", "Hindi Medium", "Piku",
                "Margarita with a Straw", "Shubh Mangal Saavdhan", "Bareilly Ki Barfi", "Kapoor & Sons", "Dear Zindagi"
            ],
            "Tamil": [
                "Kaaka Muttai", "Visaranai", "Aruvi", "96", "Super Deluxe",
                "Pariyerum Perumal", "Joker", "Aaranya Kaandam", "Subramaniapuram", "Vada Chennai",
                "Peranbu", "Aadukalam", "Paradesi", "Kuttrame Thandanai", "Kayal"
            ],
            "Telugu": [
                "Arjun Reddy", "Jersey", "Mahanati", "C/o Kancharapalem", "Bharat Ane Nenu",
                "Pellichoopulu", "Pittagoda", "Ee Nagaraniki Emaindi", "Brochevarevarura", "Mallesham",
                "Uma Maheswara Ugra Roopasya", "Colour Photo", "Middle Class Melodies", "Jathi Ratnalu", "Minnal Murali"
            ],
            "English": [
                "The Pursuit of Happyness", "Schindler's List", "The Green Mile", "Forrest Gump", "A Beautiful Mind",
                "Manchester by the Sea", "Room", "Her", "Lost in Translation", "Eternal Sunshine of the Spotless Mind",
                "The Fault in Our Stars", "Inside Out", "Up", "CODA", "Sound of Metal"
            ]
        },
        "Romantic": {
            "Kannada": [
                "Mungaru Male", "Sanju Weds Geetha", "Simple Agi Ondh Love Story", "Galipata", "Mr. and Mrs. Ramachari",
                "Milana", "Cheluvina Chittara", "Hudugaru", "Love Guru", "Pancharangi",
                "Myna", "Paramathma", "Johnny Mera Naam Preethi Mera Kaam", "Gaalipata 2", "Drama"
            ],
            "Hindi": [
                "Dilwale Dulhania Le Jayenge", "Kuch Kuch Hota Hai", "Jab We Met", "Zindagi Na Milegi Dobara", "Yeh Jawaani Hai Deewani",
                "Dil To Pagal Hai", "Hum Dil De Chuke Sanam", "Kabhi Khushi Kabhie Gham", "Kal Ho Naa Ho", "Veer-Zaara",
                "Tamasha", "Ae Dil Hai Mushkil", "Bareilly Ki Barfi", "Shubh Mangal Saavdhan", "Badhaai Ho"
            ],
            "Tamil": [
                "Alaipayuthey", "Vinnaithaandi Varuvaayaa", "OK Kanmani", "Raja Rani", "96",
                "Mouna Ragam", "Roja", "Bombay", "Dil Se", "Kadhalar Diyari",
                "Thulladha Manamum Thullum", "Minnale", "Ghajini", "Vaaranam Aayiram", "Engeyum Eppodhum"
            ],
            "Telugu": [
                "Geetha Govindam", "Arjun Reddy", "Ye Maaya Chesave", "Fidaa", "Dear Comrade",
                "Premam", "Ninnu Kori", "Hello Guru Prema Kosame", "Jaanu", "World Famous Lover",
                "Love Story", "Most Eligible Bachelor", "Bheeshma", "Ala Vaikunthapurramuloo", "Sarileru Neekevvaru"
            ],
            "English": [
                "Titanic", "The Notebook", "Casablanca", "When Harry Met Sally", "La La Land",
                "Pretty Woman", "You've Got Mail", "Sleepless in Seattle", "The Princess Bride", "Ghost",
                "Dirty Dancing", "Roman Holiday", "Before Sunrise", "Silver Linings Playbook", "The Holiday"
            ]
        },
        "Happy": {
            "Kannada": [
                "Kirik Party", "Ulidavaru Kandanthe", "Godhi Banna Sadharana Mykattu", "Operation Alamelamma", "Ondu Motteya Kathe",
                "KGF Chapter 1", "Kantara", "777 Charlie", "Rakshit Shetty", "Bell Bottom",
                "French Biryani", "Dia", "Kavaludaari", "Pushpaka Vimana", "Avane Srimannarayana"
            ],
            "Hindi": [
                "3 Idiots", "Queen", "Zindagi Na Milegi Dobara", "Dangal", "Badhaai Ho",
                "Golmaal", "Hera Pheri", "Andaz Apna Apna", "Munna Bhai MBBS", "Lage Raho Munna Bhai",
                "Fukrey", "Hindi Medium", "Toilet: Ek Prem Katha", "Stree", "Dream Girl"
            ],
            "Tamil": [
                "Chennai Express", "Naanum Rowdy Dhaan", "Comali", "Doctor", "Master",
                "Singam", "Ghilli", "Pokkiri", "Thuppakki", "Mersal",
                "Bigil", "Sarkar", "Kaththi", "Theri", "Beast"
            ],
            "Telugu": [
                "Baahubali", "Eega", "Arjun Reddy", "Jersey", "F2: Fun and Frustration",
                "Dookudu", "Gabbar Singh", "Attarintiki Daredi", "S/O Satyamurthy", "A Aa",
                "Fidaa", "Geetha Govindam", "Ala Vaikunthapurramuloo", "Sarileru Neekevvaru", "Pushpa"
            ],
            "English": [
                "The Avengers", "Toy Story", "Finding Nemo", "The Lion King", "Up",
                "Guardians of the Galaxy", "Spider-Man: Into the Spider-Verse", "The Incredibles", "Shrek", "Despicable Me",
                "Moana", "Frozen", "Zootopia", "Big Hero 6", "Coco"
            ]
        }
    }
    
    # Return 15 movies for the given mood and language
    movies = movie_database.get(mood, {}).get(language, movie_database[mood]["English"])
    return movies[:15]  # Ensure we return exactly 15 movies

def fetch_movie_details_from_omdb(movie_title):
    """Fetch movie details from OMDb API"""
    try:
        params = {
            'apikey': OMDB_API_KEY,
            't': movie_title
        }
        
        response = requests.get(OMDB_BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('Response') == 'True':
            return {
                "title": data.get('Title', movie_title),
                "rating": data.get('imdbRating', 'N/A'),
                "summary": data.get('Plot', 'No plot summary available')[:100] + "..." if len(data.get('Plot', '')) > 100 else data.get('Plot', 'No plot summary available'),
                "popularity": f"{data.get('imdbVotes', '0')} votes" if data.get('imdbVotes') != 'N/A' else "No votes data"
            }
        else:
            # Return fallback data if movie not found in OMDb
            return {
                "title": movie_title,
                "rating": "7.5",
                "summary": f"A compelling {movie_title} that matches your mood perfectly.",
                "popularity": "Popular among viewers"
            }
    except Exception as e:
        # Return fallback data
        return {
            "title": movie_title,
            "rating": "7.5", 
            "summary": f"A compelling {movie_title} that matches your mood perfectly.",
            "popularity": "Popular among viewers"
        }

def recommend_movies(mood, language):
    """Main function to recommend 5 movies with OMDb API details"""
    
    # Get 5 movie titles based on mood and language
    movie_titles = get_movie_titles_by_mood_and_language(mood, language)
    
    # Fetch details for each movie from OMDb API
    recommendations = []
    for title in movie_titles:
        movie_details = fetch_movie_details_from_omdb(title)
        recommendations.append(movie_details)
    
    return recommendations




# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sentiment = request.form["sentiment"].strip()
        language = request.form.get("language", "").strip()

        if not sentiment or not language:
            error = "Please select both Mood and Language."
            return render_template("index.html", error=error)

        movies = recommend_movies(sentiment, language)
        return render_template(
            "result.html",
            movies=movies,
            sentiment=sentiment,
            language=language,
        )
    return render_template("index.html")

@app.route("/api/recommendations", methods=["POST"])
def api_recommendations():
    """API endpoint that returns movie recommendations in JSON format"""
    data = request.get_json()
    
    if not data or 'mood' not in data or 'language' not in data:
        return jsonify({"error": "Please provide both 'mood' and 'language' in JSON format"}), 400
    
    mood = data['mood'].strip()
    language = data['language'].strip()
    
    if not mood or not language:
        return jsonify({"error": "Both mood and language must be non-empty"}), 400
    
    # Get movie recommendations
    recommendations = recommend_movies(mood, language)
    
    return jsonify(recommendations)

# Health check endpoint for Render
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "movie-recommender"}), 200

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    # For local development only
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
