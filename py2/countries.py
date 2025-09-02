"""
Countries Configuration for Looperphone
Contains dial tone and busy tone parameters for each country
"""

# Country database with dial and busy tones
COUNTRIES = {
    "7": {  # Russia
        "name": "Russia",
        "dial_tone": {
            "type": "single",
            "frequency": 425,
            "cadence": [0.8, 3.2]
        },
        "busy_tone": {
            "type": "single", 
            "frequency": 425,
            "cadence": [0.4, 0.4]
        }
    },
    
    "1": {  # Canada
        "name": "Canada",
        "dial_tone": {
            "type": "dual",
            "frequency": [440, 480],
            "cadence": [2.0, 4.0]
        },
        "busy_tone": {
            "type": "dual",
            "frequency": [480, 620],
            "cadence": [0.5, 0.5]
        }
    },
    
    "61": {  # Australia
        "name": "Australia",
        "dial_tone": {
            "type": "am",
            "frequency": 425,
            "mod_frequency": 25,
            "mod_index": 0.95,
            "cadence": [0.4, 0.2, 0.4, 2.0]  # Complex cadence: on-off-on-off
        },
        "busy_tone": {
            "type": "single",
            "frequency": 425,
            "cadence": [0.375, 0.375]
        }
    },
    
    "81": {  # Japan
        "name": "Japan",
        "dial_tone": {
            "type": "am",
            "frequency": 400,
            "mod_frequency": 16,
            "mod_index": 0.95,
            "cadence": [1.0, 2.0]
        },
        "busy_tone": {
            "type": "single",
            "frequency": 400,
            "cadence": [0.5, 0.5]
        }
    },
    
    "91": {  # India
        "name": "India",
        "dial_tone": {
            "type": "am",
            "frequency": 400,
            "mod_frequency": 25,
            "mod_index": 0.95,
            "cadence": [0.4, 0.2, 0.4, 2.6]  # Complex cadence
        },
        "busy_tone": {
            "type": "single",
            "frequency": 400,
            "cadence": [0.6, 0.6]
        }
    },
    
    "43": {  # Austria
        "name": "Austria",
        "dial_tone": {
            "type": "single",
            "frequency": 450,
            "cadence": [1.0, 5.0]
        },
        "busy_tone": {
            "type": "single",
            "frequency": 450,
            "cadence": [0.3, 0.3]
        }
    },
    
    "381": {  # Serbia
        "name": "Serbia",
        "dial_tone": {
            "type": "am",
            "frequency": 450,
            "mod_frequency": 25,
            "mod_index": 0.95,
            "cadence": [1.0, 9.0]
        },
        "busy_tone": {
            "type": "single",
            "frequency": 425,
            "cadence": [0.2, 0.4]
        }
    },
    
    "224": {  # Guinea
        "name": "Guinea",
        "dial_tone": {
            "type": "single",
            "frequency": 450,
            "cadence": [0.4, 0.2]
        },
        "busy_tone": {
            "type": "single",
            "frequency": 450,
            "cadence": [0.2, 0.2]
        }
    },
    
    "92": {  # Pakistan
        "name": "Pakistan",
        "dial_tone": {
            "type": "single",
            "frequency": 400,
            "cadence": [1.0, 2.0]
        },
        "busy_tone": {
            "type": "single",
            "frequency": 425,  # Default to Russia's busy tone
            "cadence": [0.4, 0.4]
        }
    }
}

# Default tones (Russia) for unknown countries
DEFAULT_COUNTRY = {
    "name": "Unknown",
    "dial_tone": {
        "type": "single",
        "frequency": 425,
        "cadence": [0.8, 3.2]
    },
    "busy_tone": {
        "type": "single",
        "frequency": 425,
        "cadence": [0.4, 0.4]
    }
}

def get_country_info(country_code):
    """Get country information by country code"""
    country_info = COUNTRIES.get(country_code, DEFAULT_COUNTRY.copy())
    
    # If country exists but no busy tone, use Russia's busy tone
    if country_code in COUNTRIES and "busy_tone" not in country_info:
        country_info["busy_tone"] = COUNTRIES["7"]["busy_tone"]
    
    return country_info

def list_supported_countries():
    """List all supported countries"""
    print("Supported countries:")
    for code, info in COUNTRIES.items():
        print(f"  +{code}: {info['name']}")

if __name__ == "__main__":
    # Test the country database
    list_supported_countries()
    
    # Test some lookups
    print("\nTesting lookups:")
    print(f"Russia (+7): {get_country_info('7')['name']}")
    print(f"Unknown (+999): {get_country_info('999')['name']}")
