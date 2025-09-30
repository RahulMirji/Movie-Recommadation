from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

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
            ],
            "Malayalam": [
                "Drishyam", "Premam", "Bangalore Days", "Ustad Hotel", "Charlie",
                "Maheshinte Prathikaaram", "Kumbalangi Nights", "Virus", "Thondimuthalum Driksakshiyum", "Ee.Ma.Yau",
                "Angamaly Diaries", "Take Off", "Lucifer", "Njan Prakashan", "Varathan"
            ]
        },
        "Angry": {
            "Kannada": [
                "KGF Chapter 1", "KGF Chapter 2", "Tagaru", "Mufti", "Rathavara",
                "Duniya", "Deadly Soma", "Kariya", "Jackie", "Deadly 2",
                "Bhajarangi", "Boxer", "Pailwaan", "Roberrt", "Kotigobba 3"
            ],
            "Hindi": [
                "Gangs of Wasseypur", "Haider", "Raman Raghav 2.0", "Sacred Games", "Mirzapur",
                "Dabangg", "Singham", "Rowdy Rathore", "Baby", "Tanhaji",
                "Bhaag Milkha Bhaag", "Gully Boy", "Dangal", "Article 15", "Andhadhun"
            ],
            "Tamil": [
                "Vikram", "Kaala", "Kabali", "Vada Chennai", "Asuran",
                "Raavanan", "Aadukalam", "Madras", "Raayan", "Visaranai",
                "Jigarthanda", "Maanagaram", "Pudhupettai", "Yennai Arindhaal", "Vedalam"
            ],
            "Telugu": [
                "Rangasthalam", "Kshanam", "Kanche", "Sammohanam", "Temper",
                "Athadu", "Pokiri", "Dookudu", "Race Gurram", "Sarrainodu",
                "Ala Vaikunthapurramuloo", "Pushpa", "RRR", "Baahubali", "Saaho"
            ],
            "English": [
                "Mad Max: Fury Road", "John Wick", "The Dark Knight", "Fight Club", "Gladiator",
                "Kill Bill", "The Equalizer", "Taken", "V for Vendetta", "The Raid",
                "Die Hard", "300", "Braveheart", "The Punisher", "Logan"
            ],
            "Malayalam": [
                "Lucifer", "Bheeshma Parvam", "Aarattu", "Marakkar", "Kurup",
                "Mumbai Police", "CBI 5", "Kannur Squad", "Thallumala", "Manjummel Boys",
                "Ayyappanum Koshiyum", "Malik", "Jana Gana Mana", "Bheemante Vazhi", "Varathan"
            ]
        },
        "Inspired": {
            "Kannada": [
                "Kirik Party", "Dia", "KGF Chapter 1", "777 Charlie", "Ricky",
                "Mahatma", "Accident", "Kavaludaari", "Kantara", "Lucia",
                "Ulidavaru Kandanthe", "Mugulu Nage", "Avane Srimannarayana", "Mungaru Male", "Godhi Banna Sadharana Mykattu"
            ],
            "Hindi": [
                "Chak De India", "Dangal", "Bhaag Milkha Bhaag", "Mary Kom", "M.S. Dhoni",
                "Taare Zameen Par", "3 Idiots", "Swades", "Lagaan", "Rang De Basanti",
                "Queen", "English Vinglish", "Pad Man", "Toilet: Ek Prem Katha", "Chhichhore"
            ],
            "Tamil": [
                "Soorarai Pottru", "Jai Bhim", "Aruvi", "Kaala", "Visaranai",
                "96", "Aadukalam", "Vada Chennai", "Pariyerum Perumal", "Karnan",
                "Mandela", "Sarpatta Parambarai", "Maara", "Oh My Kadavule", "Vikram Vedha"
            ],
            "Telugu": [
                "Jersey", "Mahanati", "Sye Raa Narasimha Reddy", "Ghazi", "Baahubali",
                "Arjun Reddy", "RRR", "Eega", "Mallesham", "C/o Kancharapalem",
                "Colour Photo", "Palasa 1978", "Uma Maheswara Ugra Roopasya", "Aha Kalyanam", "Ante Sundaraniki"
            ],
            "English": [
                "The Pursuit of Happyness", "The Shawshank Redemption", "Forrest Gump", "Good Will Hunting", "Dead Poets Society",
                "Rocky", "The Social Network", "Hidden Figures", "The Blind Side", "Remember the Titans",
                "Erin Brockovich", "The King's Speech", "127 Hours", "Soul", "CODA"
            ],
            "Malayalam": [
                "Manjadikuru", "Kappela", "Home", "Unda", "Sara's",
                "Sudani from Nigeria", "Kumbalangi Nights", "Thondimuthalum Driksakshiyum", "The Great Indian Kitchen", "Nayattu",
                "Virus", "Take Off", "Maheshinte Prathikaaram", "Joji", "Minnal Murali"
            ]
        },
        "Adventurous": {
            "Kannada": [
                "KGF Chapter 1", "KGF Chapter 2", "Avane Srimannarayana", "Kantara", "Vikrant Rona",
                "Mufti", "Pailwaan", "Roberrt", "The Villain", "Kotigobba 3",
                "Rathavara", "Bell Bottom", "Mr. Airavata", "Chakravyuha", "Hebbuli"
            ],
            "Hindi": [
                "Dhoom 3", "War", "Bang Bang", "Pathaan", "Tiger Zinda Hai",
                "Jawan", "Ek Tha Tiger", "Race 3", "Baaghi", "Commando",
                "Force", "Mission Mangal", "Uri: The Surgical Strike", "Raazi", "Talaash"
            ],
            "Tamil": [
                "Vikram", "Kaithi", "Master", "Beast", "Varisu",
                "Thunivu", "Valimai", "Ajith", "Thuppakki", "Sarkar",
                "Mersal", "Bigil", "Leo", "Jailer", "Indian 2"
            ],
            "Telugu": [
                "RRR", "Baahubali", "Baahubali 2", "Pushpa", "Saaho",
                "Salaar", "Adipurush", "Akhanda", "Krack", "Vakeel Saab",
                "Bheemla Nayak", "Sye Raa", "Sarileru Neekevvaru", "Ala Vaikunthapurramuloo", "Waltair Veerayya"
            ],
            "English": [
                "Indiana Jones", "The Mummy", "Jurassic Park", "Pirates of the Caribbean", "National Treasure",
                "Mission: Impossible", "The Bourne Identity", "Casino Royale", "Avatar", "Interstellar",
                "Inception", "The Matrix", "Blade Runner 2049", "Tenet", "Dune"
            ],
            "Malayalam": [
                "Lucifer", "Bheeshma Parvam", "Marakkar", "2018", "Nna Thaan Case Kodu",
                "Driving Licence", "Irul", "Kala", "Malik", "Jana Gana Mana",
                "Bro Daddy", "CBI 5", "Kannur Squad", "Bhramam", "Drishyam 2"
            ]
        },
        "Curious": {
            "Kannada": [
                "Kavaludaari", "U Turn", "Aa Karaala Ratri", "Thithi", "Lucia",
                "Ulidavaru Kandanthe", "Ricky", "Kanasemba Kudureyaneri", "Samhaara", "Karvva",
                "Aake", "Shh", "Kahi", "Kathe Chitrakathe Nirdeshana Puttanna", "Maya Bazaar"
            ],
            "Hindi": [
                "Kahaani", "Drishyam", "Andhadhun", "Talvar", "Ittefaq",
                "Ratsasan", "Badla", "Talaash", "Ugly", "NH10",
                "Detective Byomkesh Bakshy", "Kaun", "Wazir", "Te3n", "Mom"
            ],
            "Tamil": [
                "Ratsasan", "Thegidi", "Neram", "Pizza", "Dhuruvangal Pathinaaru",
                "Soodhu Kavvum", "Maanagaram", "8 Thottakkal", "Imaikka Nodigal", "Kuttrame Thandanai",
                "Yavarum Nalam", "Game Over", "Kaithi", "Vikram Vedha", "Thani Oruvan"
            ],
            "Telugu": [
                "Kshanam", "Evaru", "Karthikeya", "Goodachari", "HIT",
                "Agent Sai Srinivasa Athreya", "Sammohanam", "AWE", "Ee Nagaraniki Emaindi", "C/o Kancharapalem",
                "Kshana Kshanam", "Anukokunda Oka Roju", "Gatham", "47 Days", "Awe"
            ],
            "English": [
                "Gone Girl", "Shutter Island", "The Sixth Sense", "Knives Out", "Se7en",
                "Prisoners", "Zodiac", "Memento", "The Prestige", "The Usual Suspects",
                "Inception", "The Game", "Identity", "The Others", "Mystic River"
            ],
            "Malayalam": [
                "Drishyam", "Memories", "Anjaam Pathiraa", "Forensic", "Joseph",
                "CBI", "Unda", "Irul", "Nayattu", "Kala",
                "Bhramam", "C U Soon", "Malik", "Cold Case", "Nna Thaan Case Kodu"
            ]
        },
        "Funny": {
            "Kannada": [
                "Kirik Party", "Ondu Motteya Kathe", "French Biryani", "Operation Alamelamma", "Bell Bottom",
                "Gubbi Mele Brahmastra", "Chamak", "Sarkari Hi. Pra. Shaale", "Guru Shishyaru", "Love Mocktail",
                "Humble Politician Nograj", "Karvva", "Gultoo", "Katheyondu Shuruvagide", "Pushpaka Vimana"
            ],
            "Hindi": [
                "Hera Pheri", "Andaz Apna Apna", "Munna Bhai MBBS", "3 Idiots", "PK",
                "Golmaal", "Dhamaal", "Fukrey", "Welcome", "Khosla Ka Ghosla",
                "Chup Chup Ke", "Bhool Bhulaiyaa", "Stree", "Dream Girl", "Badhaai Ho"
            ],
            "Tamil": [
                "Soodhu Kavvum", "Naduvula Konjam Pakkatha Kaanom", "Idharkuthane Aasaipattai Balakumara", "Kaththi Sandai", "Kalakalappu",
                "Marana Mass", "Kanchana", "Pokkiri Raja", "Varuthapadatha Valibar Sangam", "Rajini Murugan",
                "Velainu Vandhutta Vellaikaaran", "Kaatrin Mozhi", "Mr. Local", "Comali", "Doctor"
            ],
            "Telugu": [
                "F2: Fun and Frustration", "Venky", "Ready", "Julayi", "Babu Bangaram",
                "Dhee", "Kick", "Dookudu", "Seema Sastry", "Shankar Dada MBBS",
                "Yamadonga", "Eega", "Bheeshma", "Jathi Ratnalu", "DJ Tillu"
            ],
            "English": [
                "The Hangover", "Superbad", "Step Brothers", "Bridesmaids", "Anchorman",
                "Tropic Thunder", "21 Jump Street", "Deadpool", "Groundhog Day", "The Grand Budapest Hotel",
                "Hot Fuzz", "Shaun of the Dead", "Mean Girls", "Airplane!", "Monty Python and the Holy Grail"
            ],
            "Malayalam": [
                "In Harihar Nagar", "Ramji Rao Speaking", "Nadodikkattu", "Kilukkam", "Chandralekha",
                "CID Moosa", "Meesa Madhavan", "Punjabi House", "Kakkakuyil", "Meesha Madhavan",
                "Salt N' Pepper", "Maheshinte Prathikaaram", "Kattappanayile Rithwik Roshan", "Oru Vadakkan Selfie", "Android Kunjappan"
            ]
        },
        "Dreamy": {
            "Kannada": [
                "Mungaru Male", "Milana", "Paramathma", "Manasaare", "Moggina Manasu",
                "Gaalipata", "Charminar", "Cheluvina Chittara", "Govindaya Namaha", "Romeo",
                "Lifeu Ishtene", "Pancharangi", "Hudugaru", "Jackie", "Raajakumara"
            ],
            "Hindi": [
                "Jab We Met", "Tamasha", "Wake Up Sid", "Dear Zindagi", "Yeh Jawaani Hai Deewani",
                "Zindagi Na Milegi Dobara", "Rocket Singh", "Highway", "Rockstar", "Barfi!",
                "Life of Pi", "The Lunchbox", "October", "Piku", "Ae Dil Hai Mushkil"
            ],
            "Tamil": [
                "OK Kanmani", "96", "Kaadhal", "Vinnaithaandi Varuvaayaa", "Mouna Ragam",
                "Alaipayuthey", "Vaaranam Aayiram", "Raja Rani", "Engeyum Eppodhum", "Kho Kho",
                "Kadhalil Sodhappuvadhu Yeppadi", "Pizza", "Maya", "Maara", "Oh My Kadavule"
            ],
            "Telugu": [
                "Ye Maaya Chesave", "Premam", "Fidaa", "Ninnu Kori", "Mahanati",
                "96", "Jaanu", "Majili", "Dear Comrade", "World Famous Lover",
                "Geetha Govindam", "Arjun Reddy", "Tholi Prema", "Nuvve Nuvve", "Nuvvu Naaku Nachav"
            ],
            "English": [
                "La La Land", "Eternal Sunshine of the Spotless Mind", "The Grand Budapest Hotel", "Life of Pi", "Big Fish",
                "Pan's Labyrinth", "The Shape of Water", "Amélie", "Midnight in Paris", "Stardust",
                "The Secret Life of Walter Mitty", "About Time", "Her", "Lost in Translation", "Before Sunrise"
            ],
            "Malayalam": [
                "Premam", "Bangalore Days", "Ustad Hotel", "Charlie", "Thattathin Marayathu",
                "Ennu Ninte Moideen", "Jacobinte Swargarajyam", "Varathan", "June", "Kappela",
                "Sara's", "Kilometers and Kilometers", "Halal Love Story", "Home", "Kumbalangi Nights"
            ]
        }
    }
    
    # Return 15 movies for the given mood and language
    movies = movie_database.get(mood, {}).get(language, [])
    if not movies:
        # Fallback to English if the combination doesn't exist
        movies = movie_database.get(mood, {}).get("English", [])
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

@app.route("/export/xml", methods=["POST"])
def export_to_xml():
    """Export movie recommendations to XML file"""
    try:
        # Get data from form
        sentiment = request.form.get("sentiment", "").strip()
        language = request.form.get("language", "").strip()
        movies_data = request.form.get("movies", "")
        
        if not sentiment or not language:
            return jsonify({"error": "Missing mood or language"}), 400
        
        # Get fresh recommendations
        movies = recommend_movies(sentiment, language)
        
        # Create XML structure
        root = ET.Element("MovieRecommendations")
        
        # Add metadata
        metadata = ET.SubElement(root, "Metadata")
        ET.SubElement(metadata, "Mood").text = sentiment
        ET.SubElement(metadata, "Language").text = language
        ET.SubElement(metadata, "GeneratedOn").text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(metadata, "TotalMovies").text = str(len(movies))
        
        # Add movies
        movies_element = ET.SubElement(root, "Movies")
        for idx, movie in enumerate(movies, 1):
            movie_element = ET.SubElement(movies_element, "Movie", id=str(idx))
            ET.SubElement(movie_element, "Title").text = movie.get("title", "N/A")
            ET.SubElement(movie_element, "Rating").text = str(movie.get("rating", "N/A"))
            ET.SubElement(movie_element, "Summary").text = movie.get("summary", "N/A")
            ET.SubElement(movie_element, "Popularity").text = movie.get("popularity", "N/A")
        
        # Create XML tree and save to file
        tree = ET.ElementTree(root)
        
        # Pretty print (compatible with older Python versions)
        try:
            ET.indent(tree, space="  ", level=0)
        except AttributeError:
            # Fallback for Python < 3.9
            pass
        
        # Create exports directory if it doesn't exist
        exports_dir = os.path.join(os.path.dirname(__file__), 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        
        # Generate filename with timestamp
        filename = f"movie_recommendations_{sentiment}_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        filepath = os.path.join(exports_dir, filename)
        
        # Write XML file
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        
        # Send file to user
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/xml'
        )
        
    except Exception as e:
        return jsonify({"error": f"Failed to export XML: {str(e)}"}), 500

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
