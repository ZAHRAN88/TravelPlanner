# Kemet Travel API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Generate Travel Plan
Generate a personalized travel itinerary based on user preferences.

**Endpoint:** `/generate-travel-plan`  
**Method:** `POST`  
**Content-Type:** `application/json`

#### Request Body
```json
{
    "answers": {
        "Experiences": ["historical", "cultural"],
        "totalDays": "3",
        "Places U want": ["Giza", "Cairo"],
        "activities": ["sightseeing", "museum visits"],
        "season": "Winter",
        "budget": "5000 EGP"
    }
}
```

#### Response
```json
{
    "success": true,
    "travel_plan": {
        "itinerary": {
            "days": [
                {
                    "day1": {
                        "location": {
                            "name": "place_name",
                            "description": "place_description",
                            "entry_fee": "cost_in_EGP",
                            "address": "location_address",
                            "duration": "duration_in_hours",
                            "open_time": "opening_time",
                            "close_time": "closing_time",
                            "category": "location_category"
                        },
                        "cultural_tip": "relevant_tip_from_data",
                        "recommended_time": "best_time_to_visit",
                        "photo_spots": ["spot1", "spot2"],
                        "nearby_amenities": ["amenity1", "amenity2"]
                    }
                }
            ],
            "total_budget": "5000 EGP",
            "total_days": 3,
            "budget_breakdown": {
                "attractions": "X EGP",
                "estimated_transport": "Y EGP",
                "estimated_meals": "Z EGP",
                "contingency": "W EGP"
            }
        },
        "additional_info": {
            "weather_recommendations": {},
            "cultural_etiquette": {},
            "transportation": {},
            "safety_tips": [],
            "emergency_contacts": {
                "tourist_police": "126",
                "ambulance": "123",
                "general_emergency": "122"
            },
            "useful_phrases": {
                "hello": "As-salaam-alaikum",
                "thank_you": "Shukran",
                "please": "Min fadlak",
                "excuse_me": "Law samaht",
                "good_morning": "Sabah el-kheir",
                "good_evening": "Masaa el-kheir"
            }
        }
    }
}
```

### 2. Weather Recommendations
Get weather-based recommendations for a specific season.

**Endpoint:** `/weather-recommendations/<season>`  
**Method:** `GET`  
**Parameters:**
- `season` (path parameter): One of "Summer", "Winter", "Spring", "Fall" (case-insensitive)

#### Response
```json
{
    "success": true,
    "season": "Summer",
    "recommendations": {
        "best_times": "Early morning (6-10 AM) or late afternoon (4-7 PM)",
        "what_to_wear": [
            "Light cotton clothes",
            "Sun hat",
            "Sunglasses",
            "Comfortable walking shoes"
        ],
        "what_to_bring": [
            "Sunscreen",
            "Water bottle",
            "Light scarf",
            "Portable fan"
        ],
        "health_tips": [
            "Stay hydrated",
            "Avoid peak sun hours",
            "Use sun protection",
            "Take breaks in shade"
        ]
    }
}
```

### 3. Cultural Etiquette
Get comprehensive cultural etiquette tips.

**Endpoint:** `/cultural-etiquette`  
**Method:** `GET`

#### Response
```json
{
    "success": true,
    "etiquette_tips": {
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
}
```

### 4. Transportation Tips
Get transportation recommendations for specific locations.

**Endpoint:** `/transportation-tips`  
**Method:** `POST`  
**Content-Type:** `application/json`

#### Request Body
```json
{
    "locations": ["Giza", "Cairo"]
}
```

#### Response
```json
{
    "success": true,
    "transportation_tips": {
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
}
```

### 5. Safety Tips
Get general safety recommendations.

**Endpoint:** `/safety-tips`  
**Method:** `GET`

#### Response
```json
{
    "success": true,
    "safety_tips": [
        "Keep important documents in hotel safe",
        "Stay aware of surroundings in crowded areas",
        "Carry only necessary valuables",
        "Keep emergency numbers handy",
        "Stay hydrated and protect from sun",
        "Use reliable transportation services",
        "Follow local customs and dress codes",
        "Keep digital copies of important documents"
    ]
}
```

### 6. Health Check
Check if the service is running.

**Endpoint:** `/health`  
**Method:** `GET`

#### Response
```json
{
    "status": "healthy",
    "message": "Service is running"
}
```

## Error Responses
All endpoints return error responses in the following format:

```json
{
    "success": false,
    "error": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `429`: Too Many Requests (API quota exceeded)
- `500`: Internal Server Error

## Rate Limiting
The API uses Google's Generative AI API which has its own rate limiting. If you exceed the quota, you'll receive a 429 status code.

## Authentication
Currently, the API does not require authentication. However, it should only be used in a development environment as indicated by the warning message when starting the server.

## Notes
1. All monetary values are in Egyptian Pounds (EGP)
2. The server runs in debug mode and is not suitable for production use
3. The API uses CORS (Cross-Origin Resource Sharing) and accepts requests from all origins
4. Emergency contact numbers are specific to Egypt 