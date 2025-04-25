from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import os
import traceback
import json
from datetime import datetime, timedelta

# Load environment variables
if os.path.exists('.env'):
    load_dotenv()
elif not os.getenv('GEMINI_API_KEY'):
    # For PythonAnywhere deployment
    os.environ['GEMINI_API_KEY'] = 'AIzaSyCFkcVDnBXX123GCjEwV54IjXA1V8-1Vtg'

# Initialize Flask app
app = Flask(__name__)
CORS(app)

try:
    # Configure Google Generative AI
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error configuring Gemini AI: {str(e)}")
    print(f"Current environment variables: {os.environ.get('GEMINI_API_KEY', 'Not set')}")
    raise

def get_weather_recommendation(season):
    """
    Get weather-based recommendations
    """
    weather_tips = {
        "Summer": {
            "best_times": "Early morning (6-10 AM) or late afternoon (4-7 PM)",
            "what_to_wear": ["Light cotton clothes", "Sun hat", "Sunglasses", "Comfortable walking shoes"],
            "what_to_bring": ["Sunscreen", "Water bottle", "Light scarf", "Portable fan"],
            "health_tips": ["Stay hydrated", "Avoid peak sun hours", "Use sun protection", "Take breaks in shade"]
        },
        "Winter": {
            "best_times": "Late morning to early afternoon (10 AM-3 PM)",
            "what_to_wear": ["Light layers", "Light jacket", "Comfortable closed shoes", "Scarf for evenings"],
            "what_to_bring": ["Light jacket", "Camera", "Power bank", "Water bottle"],
            "health_tips": ["Stay warm in early morning", "Wear layers", "Protect from wind", "Stay hydrated"]
        },
        "Spring": {
            "best_times": "Throughout the day (8 AM-5 PM)",
            "what_to_wear": ["Light layers", "Comfortable clothes", "Walking shoes", "Light scarf"],
            "what_to_bring": ["Light jacket", "Camera", "Water bottle", "Snacks"],
            "health_tips": ["Check weather forecast", "Be prepared for temperature changes", "Stay hydrated"]
        },
        "Fall": {
            "best_times": "Throughout the day (8 AM-5 PM)",
            "what_to_wear": ["Light layers", "Light jacket", "Comfortable shoes", "Scarf"],
            "what_to_bring": ["Camera", "Water bottle", "Light jacket", "Power bank"],
            "health_tips": ["Check weather forecast", "Wear layers", "Stay hydrated"]
        }
    }
    return weather_tips.get(season, weather_tips["Spring"])

def get_cultural_etiquette():
    """
    Get cultural etiquette tips
    """
    return {
        "dress_code": [
            "Dress modestly in religious sites",
            "Cover shoulders and knees",
            "Bring a scarf for mosque visits",
            "Remove shoes when required"
        ],
        "social_customs": [
            "Greet with 'As-salaam-alaikum' (Peace be upon you)",
            "Use right hand for eating and passing items",
            "Ask permission before taking photos of people",
            "Respect prayer times"
        ],
        "dining_etiquette": [
            "Accept offered tea/coffee as a gesture of hospitality",
            "It's polite to try offered food",
            "Eat with right hand if eating traditionally",
            "Express gratitude for hospitality"
        ],
        "general_tips": [
            "Learn basic Arabic greetings",
            "Respect local customs during Ramadan",
            "Be mindful of photography in sensitive areas",
            "Show respect at religious and historical sites"
        ]
    }

def load_data():
    """
    Load data from Kemet_Data.xlsx file and clean it
    """
    try:
        current_dir = os.getcwd()
        data_path = os.path.join(current_dir, 'Kemet_Data.xlsx')

        print(f"Loading file from: {current_dir}")
        print(f"Data path: {data_path}")

        # Read the Excel file
        df = pd.read_excel(data_path)
        
        # Clean column names (remove extra spaces and standardize names)
        df.columns = df.columns.str.strip().str.lower()
        
        # Clean data in each column
        for column in df.columns:
            if df[column].dtype == 'object':  # Only clean string columns
                df[column] = df[column].astype(str).str.strip().replace('\n', '', regex=True)
        
        # Rename columns to match our expected format
        column_mapping = {
            'name': 'name',
            'cultural tip': 'cultural_tip',
            'description': 'description',
            'entry fee': 'entry_fee',
            'address': 'address',
            'location': 'location',
            'duration': 'duration',
            'open time': 'open_time',
            'close time': 'close_time',
            'category': 'category'
        }
        
        # Select and rename only the columns we need
        df = df[list(column_mapping.keys())].rename(columns=column_mapping)

        print("Successfully loaded and cleaned Kemet_Data.xlsx")
        print(f"Number of locations loaded: {len(df)}")
        return df

    except Exception as e:
        print(f"Error loading Excel file: {str(e)}")
        print(traceback.format_exc())
        return None

def format_list_items(items):
    """
    Format list items for the prompt
    """
    if isinstance(items, list):
        return ', '.join(items)
    return str(items)

def create_travel_prompt(answers, data_df):
    """
    Create structured prompt for travel itinerary
    """
    experiences = format_list_items(answers[0])
    duration = answers[1]
    places = format_list_items(answers[2])
    activities = format_list_items(answers[3])
    season = answers[4]
    budget = answers[5]

    prompt = f"""Create a {duration}-day travel itinerary based on these preferences:

User Preferences:
- Experiences: {experiences}
- Places: {places}
- Activities: {activities}
- Season: {season}
- Budget: {budget}

Available Places and Activities Data:
{data_df.to_string(index=False)}

Generate a response in exactly this JSON format:
{{
    "success": true,
    "travel_plan": {{
        "itinerary": {{
            "days": [
                {{
                    "day1": {{
                        "location": {{
                            "name": "place_name",
                            "description": "place_description",
                            "entry_fee": "cost_in_EGP",
                            "address": "location_address",
                            "duration": "duration_in_hours",
                            "open_time": "opening_time",
                            "close_time": "closing_time",
                            "category": "location_category"
                        }},
                        "cultural_tip": "relevant_tip_from_data",
                        "recommended_time": "best_time_to_visit",
                        "photo_spots": ["spot1", "spot2"],
                        "nearby_amenities": ["amenity1", "amenity2"]
                    }}
                }}
            ],
            "total_budget": "{budget}",
            "total_days": {duration},
            "budget_breakdown": {{
                "attractions": "X EGP",
                "estimated_transport": "Y EGP",
                "estimated_meals": "Z EGP",
                "contingency": "W EGP"
            }}
        }},
        "trip_tips": {{
            "weather": WEATHER_INFO,
            "cultural_etiquette": CULTURAL_INFO,
            "transportation": [
                "tip1",
                "tip2"
            ],
            "safety": [
                "tip1",
                "tip2"
            ]
        }}
    }}
}}

Requirements:
1. Use only locations from the provided data
2. Each day must have exactly one location with its complete details
3. Include accurate descriptions, entry fees, and durations from the data
4. Stay within the total budget of {budget}
5. All activities must be suitable for {season}
6. Follow the exact JSON format shown above
7. All costs must be in EGP
8. Ensure the suggested timings align with the location's open and close times
9. Include cultural tips and category information for each location
10. Provide detailed photo opportunity spots
11. List nearby amenities and facilities
12. Give time-specific recommendations based on weather and crowds"""

    return prompt

def parse_response(response_text):
    """
    Parse and validate the AI response
    """
    try:
        # Clean up the response
        cleaned_response = response_text.strip()

        # Extract JSON from response
        start_idx = cleaned_response.find('{')
        end_idx = cleaned_response.rfind('}') + 1

        if start_idx >= 0 and end_idx > start_idx:
            json_str = cleaned_response[start_idx:end_idx]
            parsed_json = json.loads(json_str)

            # Validate JSON structure
            if not all(key in parsed_json for key in ['success', 'travel_plan']):
                raise ValueError("Invalid response format - missing required keys")

            # Validate itinerary structure
            itinerary = parsed_json.get('travel_plan', {}).get('itinerary', {})
            if not all(key in itinerary for key in ['days', 'total_budget', 'total_days']):
                raise ValueError("Invalid itinerary format - missing required fields")

            return parsed_json

        raise ValueError("No valid JSON found in response")

    except Exception as e:
        print(f"Error parsing response: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to parse response: {str(e)}"
        }

def get_transportation_tips(locations):
    """
    Get transportation recommendations based on locations
    """
    return {
        "getting_around": [
            "Use official white taxis or ride-hailing apps",
            "Consider metro for avoiding traffic in Cairo",
            "Book private driver for day trips",
            "Use shuttle services for distant attractions"
        ],
        "tips": [
            "Agree on taxi fare before riding",
            "Keep small bills for transportation",
            "Download local transportation apps",
            "Consider guided tours for multiple locations"
        ],
        "safety": [
            "Use registered transportation services",
            "Keep valuables secure",
            "Share ride details with companions",
            "Have emergency contacts handy"
        ]
    }

def get_safety_tips():
    """
    Get general safety recommendations
    """
    return [
        "Keep important documents in hotel safe",
        "Stay aware of surroundings in crowded areas",
        "Carry only necessary valuables",
        "Keep emergency numbers handy",
        "Stay hydrated and protect from sun",
        "Use reliable transportation services",
        "Follow local customs and dress codes",
        "Keep digital copies of important documents"
    ]

@app.route('/')
def home():
    return jsonify({
        "status": "healthy",
        "message": "API is running",
        "environment": os.getenv('ENVIRONMENT', 'development')
    })

@app.route('/api/generate-travel-plan', methods=['POST'])
def generate_travel_plan():
    """
    Generate travel plan based on user preferences
    """
    try:
        # Load data
        data_df = load_data()
        if data_df is None:
            return jsonify({
                'success': False,
                'error': 'Failed to load data from Kemet_Data.xlsx'
            }), 500

        # Get request data
        data = request.get_json()
        if not data or 'answers' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing answers in request'
            }), 400

        answers_data = data['answers']
        
        # Validate and extract structured data
        try:
            answers = [
                answers_data.get('Experiences', []),
                str(answers_data.get('totalDays', '')),
                answers_data.get('Places U want', []),
                answers_data.get('activities', []),
                answers_data.get('season', ''),
                answers_data.get('budget', '')
            ]
            
            # Validate required fields
            if not all(answers):
                return jsonify({
                    'success': False,
                    'error': 'Missing required fields. Please provide: Experiences, totalDays, Places U want, activities, season, and budget'
                }), 400

            print(f"Received answers: {answers}")

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Invalid request format: {str(e)}'
            }), 400

        try:
            # Create prompt and generate response
            prompt = create_travel_prompt(answers, data_df)
            model = genai.GenerativeModel('gemini-2.0-flash')

            generation_config = {
                'temperature': 0.7,
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 2048,
            }

            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            # Parse and validate response
            parsed_response = parse_response(response.text)

            if not parsed_response.get('success'):
                return jsonify(parsed_response), 400

            # Enhance the response with additional information
            weather_info = get_weather_recommendation(answers[4])  # season
            cultural_info = get_cultural_etiquette()
            transport_info = get_transportation_tips(answers[2])  # places
            safety_info = get_safety_tips()

            # Add enhanced information to the response
            if 'travel_plan' not in parsed_response:
                parsed_response['travel_plan'] = {}
            
            parsed_response['travel_plan']['additional_info'] = {
                'weather_recommendations': weather_info,
                'cultural_etiquette': cultural_info,
                'transportation': transport_info,
                'safety_tips': safety_info,
                'emergency_contacts': {
                    'tourist_police': '126',
                    'ambulance': '123',
                    'general_emergency': '122'
                },
                'useful_phrases': {
                    'hello': 'As-salaam-alaikum',
                    'thank_you': 'Shukran',
                    'please': 'Min fadlak',
                    'excuse_me': 'Law samaht',
                    'good_morning': 'Sabah el-kheir',
                    'good_evening': 'Masaa el-kheir'
                }
            }

            return jsonify(parsed_response), 200

        except Exception as e:
            error_message = str(e)
            if "quota" in error_message.lower():
                return jsonify({
                    'success': False,
                    'error': 'API quota exceeded. Please try again later.'
                }), 429
            else:
                return jsonify({
                    'success': False,
                    'error': f'Error generating travel plan: {error_message}'
                }), 500

    except Exception as e:
        print(f"Error in generate_travel_plan: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Service is running'
    }), 200

@app.route('/api/weather-recommendations/<season>', methods=['GET'])
def weather_recommendations(season):
    """Get weather recommendations for a specific season"""
    try:
        season = season.capitalize()
        if season not in ["Summer", "Winter", "Spring", "Fall"]:
            return jsonify({
                "success": False,
                "error": "Invalid season. Please choose from: Summer, Winter, Spring, Fall"
            }), 400
            
        recommendations = get_weather_recommendation(season)
        return jsonify({
            "success": True,
            "season": season,
            "recommendations": recommendations
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/cultural-etiquette', methods=['GET'])
def cultural_etiquette():
    """Get cultural etiquette tips"""
    try:
        etiquette_tips = get_cultural_etiquette()
        return jsonify({
            "success": True,
            "etiquette_tips": etiquette_tips
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/transportation-tips', methods=['POST'])
def transportation_tips():
    """Get transportation tips for specific locations"""
    try:
        data = request.get_json()
        if not data or 'locations' not in data:
            return jsonify({
                "success": False,
                "error": "Please provide a list of locations"
            }), 400
            
        locations = data['locations']
        tips = get_transportation_tips(locations)
        return jsonify({
            "success": True,
            "transportation_tips": tips
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/safety-tips', methods=['GET'])
def safety_tips():
    """Get general safety tips"""
    try:
        tips = get_safety_tips()
        return jsonify({
            "success": True,
            "safety_tips": tips
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("Starting server...")
    print(f"Current directory: {os.getcwd()}")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    if os.getenv('PYTHONANYWHERE_SITE'):
        # Running on PythonAnywhere
        app.run()
    else:
        # Running locally
        port = int(os.getenv("PORT", 5000))
        app.run(debug=True, host="0.0.0.0", port=port)