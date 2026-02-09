"""
Country and Region Extraction from Singapore Budget Speeches
Extracts mentions of countries and regions from parquet files
"""

import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

# Comprehensive list of countries with aliases and ISO codes
# Organized by region for analysis
COUNTRIES = {
    # ===== ASIA-PACIFIC =====
    # East Asia
    "China": {
        "iso": "CHN",
        "region": "East Asia",
        "aliases": [
            "China",
            "Chinese",
            "PRC",
            "People's Republic of China",
            "Beijing",
            "Shanghai",
            "Shenzhen",
            "Guangzhou",
            "Hong Kong",  # Often mentioned separately
        ],
    },
    "Japan": {
        "iso": "JPN",
        "region": "East Asia",
        "aliases": ["Japan", "Japanese", "Tokyo", "Osaka"],
    },
    "South Korea": {
        "iso": "KOR",
        "region": "East Asia",
        "aliases": [
            "South Korea",
            "Korea",
            "Korean",
            "Seoul",
            "Republic of Korea",
            "ROK",
        ],
    },
    "North Korea": {
        "iso": "PRK",
        "region": "East Asia",
        "aliases": ["North Korea", "DPRK", "Pyongyang"],
    },
    "Taiwan": {
        "iso": "TWN",
        "region": "East Asia",
        "aliases": ["Taiwan", "Taiwanese", "Taipei", "ROC"],
    },
    "Mongolia": {
        "iso": "MNG",
        "region": "East Asia",
        "aliases": ["Mongolia", "Mongolian"],
    },
    # Southeast Asia (ASEAN)
    "Malaysia": {
        "iso": "MYS",
        "region": "Southeast Asia",
        "aliases": [
            "Malaysia",
            "Malaysian",
            "Kuala Lumpur",
            "Malaya",
            "Johor",
            "Penang",
            "KL",
        ],
    },
    "Indonesia": {
        "iso": "IDN",
        "region": "Southeast Asia",
        "aliases": [
            "Indonesia",
            "Indonesian",
            "Jakarta",
            "Batam",
            "Riau",
            "Java",
            "Sumatra",
        ],
    },
    "Thailand": {
        "iso": "THA",
        "region": "Southeast Asia",
        "aliases": ["Thailand", "Thai", "Bangkok", "Siam"],
    },
    "Vietnam": {
        "iso": "VNM",
        "region": "Southeast Asia",
        "aliases": [
            "Vietnam",
            "Vietnamese",
            "Hanoi",
            "Ho Chi Minh",
            "Saigon",
            "Viet Nam",
        ],
    },
    "Philippines": {
        "iso": "PHL",
        "region": "Southeast Asia",
        "aliases": ["Philippines", "Filipino", "Philippine", "Manila"],
    },
    "Myanmar": {
        "iso": "MMR",
        "region": "Southeast Asia",
        "aliases": ["Myanmar", "Burma", "Burmese", "Yangon", "Rangoon"],
    },
    "Cambodia": {
        "iso": "KHM",
        "region": "Southeast Asia",
        "aliases": ["Cambodia", "Cambodian", "Phnom Penh", "Kampuchea"],
    },
    "Laos": {
        "iso": "LAO",
        "region": "Southeast Asia",
        "aliases": ["Laos", "Laotian", "Vientiane", "Lao PDR"],
    },
    "Brunei": {
        "iso": "BRN",
        "region": "Southeast Asia",
        "aliases": ["Brunei", "Bruneian", "Bandar Seri Begawan"],
    },
    "Timor-Leste": {
        "iso": "TLS",
        "region": "Southeast Asia",
        "aliases": ["Timor-Leste", "East Timor", "Timorese"],
    },
    # South Asia
    "India": {
        "iso": "IND",
        "region": "South Asia",
        "aliases": [
            "India",
            "Indian",
            "New Delhi",
            "Delhi",
            "Mumbai",
            "Bombay",
            "Bangalore",
            "Chennai",
        ],
    },
    "Pakistan": {
        "iso": "PAK",
        "region": "South Asia",
        "aliases": ["Pakistan", "Pakistani", "Islamabad", "Karachi"],
    },
    "Bangladesh": {
        "iso": "BGD",
        "region": "South Asia",
        "aliases": ["Bangladesh", "Bangladeshi", "Dhaka", "East Pakistan"],
    },
    "Sri Lanka": {
        "iso": "LKA",
        "region": "South Asia",
        "aliases": ["Sri Lanka", "Sri Lankan", "Ceylon", "Colombo"],
    },
    "Nepal": {
        "iso": "NPL",
        "region": "South Asia",
        "aliases": ["Nepal", "Nepalese", "Nepali", "Kathmandu"],
    },
    "Bhutan": {
        "iso": "BTN",
        "region": "South Asia",
        "aliases": ["Bhutan", "Bhutanese", "Thimphu"],
    },
    "Maldives": {
        "iso": "MDV",
        "region": "South Asia",
        "aliases": ["Maldives", "Maldivian", "Male"],
    },
    "Afghanistan": {
        "iso": "AFG",
        "region": "South Asia",
        "aliases": ["Afghanistan", "Afghan", "Kabul"],
    },
    # Central Asia
    "Kazakhstan": {
        "iso": "KAZ",
        "region": "Central Asia",
        "aliases": ["Kazakhstan", "Kazakh", "Astana", "Almaty"],
    },
    "Uzbekistan": {
        "iso": "UZB",
        "region": "Central Asia",
        "aliases": ["Uzbekistan", "Uzbek", "Tashkent"],
    },
    "Turkmenistan": {
        "iso": "TKM",
        "region": "Central Asia",
        "aliases": ["Turkmenistan", "Turkmen", "Ashgabat"],
    },
    "Kyrgyzstan": {
        "iso": "KGZ",
        "region": "Central Asia",
        "aliases": ["Kyrgyzstan", "Kyrgyz", "Bishkek"],
    },
    "Tajikistan": {
        "iso": "TJK",
        "region": "Central Asia",
        "aliases": ["Tajikistan", "Tajik", "Dushanbe"],
    },
    # Oceania
    "Australia": {
        "iso": "AUS",
        "region": "Oceania",
        "aliases": ["Australia", "Australian", "Sydney", "Melbourne", "Canberra"],
    },
    "New Zealand": {
        "iso": "NZL",
        "region": "Oceania",
        "aliases": ["New Zealand", "NZ", "Kiwi", "Auckland", "Wellington"],
    },
    "Papua New Guinea": {
        "iso": "PNG",
        "region": "Oceania",
        "aliases": ["Papua New Guinea", "PNG", "Port Moresby"],
    },
    "Fiji": {
        "iso": "FJI",
        "region": "Oceania",
        "aliases": ["Fiji", "Fijian", "Suva"],
    },
    # ===== EUROPE =====
    # Western Europe
    "United Kingdom": {
        "iso": "GBR",
        "region": "Western Europe",
        "aliases": [
            "United Kingdom",
            "UK",
            "Britain",
            "British",
            "England",
            "English",
            "Scotland",
            "Scottish",
            "Wales",
            "Welsh",
            "London",
            "Great Britain",
        ],
    },
    "Germany": {
        "iso": "DEU",
        "region": "Western Europe",
        "aliases": [
            "Germany",
            "German",
            "Berlin",
            "Frankfurt",
            "Munich",
            "West Germany",
            "East Germany",
        ],
    },
    "France": {
        "iso": "FRA",
        "region": "Western Europe",
        "aliases": ["France", "French", "Paris", "Lyon"],
    },
    "Netherlands": {
        "iso": "NLD",
        "region": "Western Europe",
        "aliases": ["Netherlands", "Dutch", "Holland", "Amsterdam", "Rotterdam"],
    },
    "Belgium": {
        "iso": "BEL",
        "region": "Western Europe",
        "aliases": ["Belgium", "Belgian", "Brussels"],
    },
    "Luxembourg": {
        "iso": "LUX",
        "region": "Western Europe",
        "aliases": ["Luxembourg", "Luxembourgish"],
    },
    "Switzerland": {
        "iso": "CHE",
        "region": "Western Europe",
        "aliases": ["Switzerland", "Swiss", "Geneva", "Zurich", "Bern"],
    },
    "Austria": {
        "iso": "AUT",
        "region": "Western Europe",
        "aliases": ["Austria", "Austrian", "Vienna"],
    },
    "Ireland": {
        "iso": "IRL",
        "region": "Western Europe",
        "aliases": ["Ireland", "Irish", "Dublin", "Eire"],
    },
    # Northern Europe
    "Sweden": {
        "iso": "SWE",
        "region": "Northern Europe",
        "aliases": ["Sweden", "Swedish", "Stockholm"],
    },
    "Norway": {
        "iso": "NOR",
        "region": "Northern Europe",
        "aliases": ["Norway", "Norwegian", "Oslo"],
    },
    "Denmark": {
        "iso": "DNK",
        "region": "Northern Europe",
        "aliases": ["Denmark", "Danish", "Copenhagen"],
    },
    "Finland": {
        "iso": "FIN",
        "region": "Northern Europe",
        "aliases": ["Finland", "Finnish", "Helsinki"],
    },
    "Iceland": {
        "iso": "ISL",
        "region": "Northern Europe",
        "aliases": ["Iceland", "Icelandic", "Reykjavik"],
    },
    # Southern Europe
    "Italy": {
        "iso": "ITA",
        "region": "Southern Europe",
        "aliases": ["Italy", "Italian", "Rome", "Milan", "Venice"],
    },
    "Spain": {
        "iso": "ESP",
        "region": "Southern Europe",
        "aliases": ["Spain", "Spanish", "Madrid", "Barcelona"],
    },
    "Portugal": {
        "iso": "PRT",
        "region": "Southern Europe",
        "aliases": ["Portugal", "Portuguese", "Lisbon"],
    },
    "Greece": {
        "iso": "GRC",
        "region": "Southern Europe",
        "aliases": ["Greece", "Greek", "Athens", "Grecian"],
    },
    "Cyprus": {
        "iso": "CYP",
        "region": "Southern Europe",
        "aliases": ["Cyprus", "Cypriot", "Nicosia"],
    },
    "Malta": {
        "iso": "MLT",
        "region": "Southern Europe",
        "aliases": ["Malta", "Maltese", "Valletta"],
    },
    # Eastern Europe
    "Russia": {
        "iso": "RUS",
        "region": "Eastern Europe",
        "aliases": [
            "Russia",
            "Russian",
            "Moscow",
            "Soviet",
            "USSR",
            "Soviet Union",
            "St Petersburg",
        ],
    },
    "Poland": {
        "iso": "POL",
        "region": "Eastern Europe",
        "aliases": ["Poland", "Polish", "Warsaw"],
    },
    "Ukraine": {
        "iso": "UKR",
        "region": "Eastern Europe",
        "aliases": ["Ukraine", "Ukrainian", "Kyiv", "Kiev"],
    },
    "Czech Republic": {
        "iso": "CZE",
        "region": "Eastern Europe",
        "aliases": [
            "Czech Republic",
            "Czech",
            "Czechia",
            "Prague",
            "Czechoslovakia",
        ],
    },
    "Hungary": {
        "iso": "HUN",
        "region": "Eastern Europe",
        "aliases": ["Hungary", "Hungarian", "Budapest"],
    },
    "Romania": {
        "iso": "ROU",
        "region": "Eastern Europe",
        "aliases": ["Romania", "Romanian", "Bucharest"],
    },
    "Bulgaria": {
        "iso": "BGR",
        "region": "Eastern Europe",
        "aliases": ["Bulgaria", "Bulgarian", "Sofia"],
    },
    "Serbia": {
        "iso": "SRB",
        "region": "Eastern Europe",
        "aliases": ["Serbia", "Serbian", "Belgrade", "Yugoslavia"],
    },
    "Croatia": {
        "iso": "HRV",
        "region": "Eastern Europe",
        "aliases": ["Croatia", "Croatian", "Zagreb"],
    },
    "Slovenia": {
        "iso": "SVN",
        "region": "Eastern Europe",
        "aliases": ["Slovenia", "Slovenian", "Ljubljana"],
    },
    "Slovakia": {
        "iso": "SVK",
        "region": "Eastern Europe",
        "aliases": ["Slovakia", "Slovak", "Bratislava"],
    },
    "Belarus": {
        "iso": "BLR",
        "region": "Eastern Europe",
        "aliases": ["Belarus", "Belarusian", "Minsk"],
    },
    "Moldova": {
        "iso": "MDA",
        "region": "Eastern Europe",
        "aliases": ["Moldova", "Moldovan", "Chisinau"],
    },
    "Estonia": {
        "iso": "EST",
        "region": "Eastern Europe",
        "aliases": ["Estonia", "Estonian", "Tallinn"],
    },
    "Latvia": {
        "iso": "LVA",
        "region": "Eastern Europe",
        "aliases": ["Latvia", "Latvian", "Riga"],
    },
    "Lithuania": {
        "iso": "LTU",
        "region": "Eastern Europe",
        "aliases": ["Lithuania", "Lithuanian", "Vilnius"],
    },
    # ===== AMERICAS =====
    # North America
    "United States": {
        "iso": "USA",
        "region": "North America",
        "aliases": [
            "United States",
            "USA",
            "US",
            "America",
            "American",
            "Washington",
            "New York",
            "California",
            "Silicon Valley",
            "Wall Street",
            "Texas",
            "U.S.",
            "U.S.A.",
        ],
    },
    "Canada": {
        "iso": "CAN",
        "region": "North America",
        "aliases": ["Canada", "Canadian", "Ottawa", "Toronto", "Vancouver"],
    },
    "Mexico": {
        "iso": "MEX",
        "region": "North America",
        "aliases": ["Mexico", "Mexican", "Mexico City"],
    },
    # Central America & Caribbean
    "Cuba": {
        "iso": "CUB",
        "region": "Central America",
        "aliases": ["Cuba", "Cuban", "Havana"],
    },
    "Jamaica": {
        "iso": "JAM",
        "region": "Central America",
        "aliases": ["Jamaica", "Jamaican", "Kingston"],
    },
    "Panama": {
        "iso": "PAN",
        "region": "Central America",
        "aliases": ["Panama", "Panamanian", "Panama City", "Panama Canal"],
    },
    "Costa Rica": {
        "iso": "CRI",
        "region": "Central America",
        "aliases": ["Costa Rica", "Costa Rican", "San Jose"],
    },
    # South America
    "Brazil": {
        "iso": "BRA",
        "region": "South America",
        "aliases": ["Brazil", "Brazilian", "Sao Paulo", "Rio", "Brasilia"],
    },
    "Argentina": {
        "iso": "ARG",
        "region": "South America",
        "aliases": ["Argentina", "Argentine", "Buenos Aires"],
    },
    "Chile": {
        "iso": "CHL",
        "region": "South America",
        "aliases": ["Chile", "Chilean", "Santiago"],
    },
    "Colombia": {
        "iso": "COL",
        "region": "South America",
        "aliases": ["Colombia", "Colombian", "Bogota"],
    },
    "Peru": {
        "iso": "PER",
        "region": "South America",
        "aliases": ["Peru", "Peruvian", "Lima"],
    },
    "Venezuela": {
        "iso": "VEN",
        "region": "South America",
        "aliases": ["Venezuela", "Venezuelan", "Caracas"],
    },
    "Ecuador": {
        "iso": "ECU",
        "region": "South America",
        "aliases": ["Ecuador", "Ecuadorian", "Quito"],
    },
    "Bolivia": {
        "iso": "BOL",
        "region": "South America",
        "aliases": ["Bolivia", "Bolivian", "La Paz"],
    },
    "Uruguay": {
        "iso": "URY",
        "region": "South America",
        "aliases": ["Uruguay", "Uruguayan", "Montevideo"],
    },
    "Paraguay": {
        "iso": "PRY",
        "region": "South America",
        "aliases": ["Paraguay", "Paraguayan", "Asuncion"],
    },
    # ===== MIDDLE EAST =====
    "Saudi Arabia": {
        "iso": "SAU",
        "region": "Middle East",
        "aliases": ["Saudi Arabia", "Saudi", "Riyadh", "Mecca", "Jeddah"],
    },
    "United Arab Emirates": {
        "iso": "ARE",
        "region": "Middle East",
        "aliases": ["UAE", "United Arab Emirates", "Dubai", "Abu Dhabi", "Emirates"],
    },
    "Israel": {
        "iso": "ISR",
        "region": "Middle East",
        "aliases": ["Israel", "Israeli", "Tel Aviv", "Jerusalem"],
    },
    "Turkey": {
        "iso": "TUR",
        "region": "Middle East",
        "aliases": ["Turkey", "Turkish", "Istanbul", "Ankara"],
    },
    "Iran": {
        "iso": "IRN",
        "region": "Middle East",
        "aliases": ["Iran", "Iranian", "Tehran", "Persia", "Persian"],
    },
    "Iraq": {
        "iso": "IRQ",
        "region": "Middle East",
        "aliases": ["Iraq", "Iraqi", "Baghdad"],
    },
    "Kuwait": {
        "iso": "KWT",
        "region": "Middle East",
        "aliases": ["Kuwait", "Kuwaiti"],
    },
    "Qatar": {
        "iso": "QAT",
        "region": "Middle East",
        "aliases": ["Qatar", "Qatari", "Doha"],
    },
    "Bahrain": {
        "iso": "BHR",
        "region": "Middle East",
        "aliases": ["Bahrain", "Bahraini", "Manama"],
    },
    "Oman": {
        "iso": "OMN",
        "region": "Middle East",
        "aliases": ["Oman", "Omani", "Muscat"],
    },
    "Jordan": {
        "iso": "JOR",
        "region": "Middle East",
        "aliases": ["Jordan", "Jordanian", "Amman"],
    },
    "Lebanon": {
        "iso": "LBN",
        "region": "Middle East",
        "aliases": ["Lebanon", "Lebanese", "Beirut"],
    },
    "Syria": {
        "iso": "SYR",
        "region": "Middle East",
        "aliases": ["Syria", "Syrian", "Damascus"],
    },
    "Yemen": {
        "iso": "YEM",
        "region": "Middle East",
        "aliases": ["Yemen", "Yemeni", "Sanaa"],
    },
    "Palestine": {
        "iso": "PSE",
        "region": "Middle East",
        "aliases": ["Palestine", "Palestinian", "Gaza", "West Bank"],
    },
    # ===== AFRICA =====
    # North Africa
    "Egypt": {
        "iso": "EGY",
        "region": "North Africa",
        "aliases": ["Egypt", "Egyptian", "Cairo", "Suez"],
    },
    "Morocco": {
        "iso": "MAR",
        "region": "North Africa",
        "aliases": ["Morocco", "Moroccan", "Rabat", "Casablanca"],
    },
    "Algeria": {
        "iso": "DZA",
        "region": "North Africa",
        "aliases": ["Algeria", "Algerian", "Algiers"],
    },
    "Tunisia": {
        "iso": "TUN",
        "region": "North Africa",
        "aliases": ["Tunisia", "Tunisian", "Tunis"],
    },
    "Libya": {
        "iso": "LBY",
        "region": "North Africa",
        "aliases": ["Libya", "Libyan", "Tripoli"],
    },
    "Sudan": {
        "iso": "SDN",
        "region": "North Africa",
        "aliases": ["Sudan", "Sudanese", "Khartoum"],
    },
    # Sub-Saharan Africa
    "South Africa": {
        "iso": "ZAF",
        "region": "Sub-Saharan Africa",
        "aliases": [
            "South Africa",
            "South African",
            "Johannesburg",
            "Cape Town",
            "Pretoria",
        ],
    },
    "Nigeria": {
        "iso": "NGA",
        "region": "Sub-Saharan Africa",
        "aliases": ["Nigeria", "Nigerian", "Lagos", "Abuja"],
    },
    "Kenya": {
        "iso": "KEN",
        "region": "Sub-Saharan Africa",
        "aliases": ["Kenya", "Kenyan", "Nairobi"],
    },
    "Ethiopia": {
        "iso": "ETH",
        "region": "Sub-Saharan Africa",
        "aliases": ["Ethiopia", "Ethiopian", "Addis Ababa"],
    },
    "Ghana": {
        "iso": "GHA",
        "region": "Sub-Saharan Africa",
        "aliases": ["Ghana", "Ghanaian", "Accra"],
    },
    "Tanzania": {
        "iso": "TZA",
        "region": "Sub-Saharan Africa",
        "aliases": ["Tanzania", "Tanzanian", "Dar es Salaam"],
    },
    "Rwanda": {
        "iso": "RWA",
        "region": "Sub-Saharan Africa",
        "aliases": ["Rwanda", "Rwandan", "Kigali"],
    },
    "Uganda": {
        "iso": "UGA",
        "region": "Sub-Saharan Africa",
        "aliases": ["Uganda", "Ugandan", "Kampala"],
    },
    "Zimbabwe": {
        "iso": "ZWE",
        "region": "Sub-Saharan Africa",
        "aliases": ["Zimbabwe", "Zimbabwean", "Harare", "Rhodesia"],
    },
    "Senegal": {
        "iso": "SEN",
        "region": "Sub-Saharan Africa",
        "aliases": ["Senegal", "Senegalese", "Dakar"],
    },
    "Ivory Coast": {
        "iso": "CIV",
        "region": "Sub-Saharan Africa",
        "aliases": ["Ivory Coast", "Cote d'Ivoire", "Ivorian", "Abidjan"],
    },
    "Angola": {
        "iso": "AGO",
        "region": "Sub-Saharan Africa",
        "aliases": ["Angola", "Angolan", "Luanda"],
    },
    "Mozambique": {
        "iso": "MOZ",
        "region": "Sub-Saharan Africa",
        "aliases": ["Mozambique", "Mozambican", "Maputo"],
    },
    "Zambia": {
        "iso": "ZMB",
        "region": "Sub-Saharan Africa",
        "aliases": ["Zambia", "Zambian", "Lusaka"],
    },
    "Botswana": {
        "iso": "BWA",
        "region": "Sub-Saharan Africa",
        "aliases": ["Botswana", "Batswana", "Gaborone"],
    },
    "Namibia": {
        "iso": "NAM",
        "region": "Sub-Saharan Africa",
        "aliases": ["Namibia", "Namibian", "Windhoek"],
    },
    "Mauritius": {
        "iso": "MUS",
        "region": "Sub-Saharan Africa",
        "aliases": ["Mauritius", "Mauritian", "Port Louis"],
    },
}

# Regional groupings for analysis
REGIONS = {
    "East Asia": ["China", "Japan", "South Korea", "North Korea", "Taiwan", "Mongolia"],
    "Southeast Asia": [
        "Malaysia",
        "Indonesia",
        "Thailand",
        "Vietnam",
        "Philippines",
        "Myanmar",
        "Cambodia",
        "Laos",
        "Brunei",
        "Timor-Leste",
    ],
    "South Asia": [
        "India",
        "Pakistan",
        "Bangladesh",
        "Sri Lanka",
        "Nepal",
        "Bhutan",
        "Maldives",
        "Afghanistan",
    ],
    "Central Asia": [
        "Kazakhstan",
        "Uzbekistan",
        "Turkmenistan",
        "Kyrgyzstan",
        "Tajikistan",
    ],
    "Oceania": ["Australia", "New Zealand", "Papua New Guinea", "Fiji"],
    "Western Europe": [
        "United Kingdom",
        "Germany",
        "France",
        "Netherlands",
        "Belgium",
        "Luxembourg",
        "Switzerland",
        "Austria",
        "Ireland",
    ],
    "Northern Europe": ["Sweden", "Norway", "Denmark", "Finland", "Iceland"],
    "Southern Europe": ["Italy", "Spain", "Portugal", "Greece", "Cyprus", "Malta"],
    "Eastern Europe": [
        "Russia",
        "Poland",
        "Ukraine",
        "Czech Republic",
        "Hungary",
        "Romania",
        "Bulgaria",
        "Serbia",
        "Croatia",
        "Slovenia",
        "Slovakia",
        "Belarus",
        "Moldova",
        "Estonia",
        "Latvia",
        "Lithuania",
    ],
    "North America": ["United States", "Canada", "Mexico"],
    "Central America": ["Cuba", "Jamaica", "Panama", "Costa Rica"],
    "South America": [
        "Brazil",
        "Argentina",
        "Chile",
        "Colombia",
        "Peru",
        "Venezuela",
        "Ecuador",
        "Bolivia",
        "Uruguay",
        "Paraguay",
    ],
    "Middle East": [
        "Saudi Arabia",
        "United Arab Emirates",
        "Israel",
        "Turkey",
        "Iran",
        "Iraq",
        "Kuwait",
        "Qatar",
        "Bahrain",
        "Oman",
        "Jordan",
        "Lebanon",
        "Syria",
        "Yemen",
        "Palestine",
    ],
    "North Africa": ["Egypt", "Morocco", "Algeria", "Tunisia", "Libya", "Sudan"],
    "Sub-Saharan Africa": [
        "South Africa",
        "Nigeria",
        "Kenya",
        "Ethiopia",
        "Ghana",
        "Tanzania",
        "Rwanda",
        "Uganda",
        "Zimbabwe",
        "Senegal",
        "Ivory Coast",
        "Angola",
        "Mozambique",
        "Zambia",
        "Botswana",
        "Namibia",
        "Mauritius",
    ],
}

# Words to exclude (common false positives)
EXCLUDE_PATTERNS = [
    r"\bchina\s+(?:clay|town|ware|shop|syndrome)\b",  # china as material
    r"\bturkey\b(?!\s+(?:and|or|is|has|was|will|'s))",  # turkey the bird in some contexts
    r"\bjordan\s+(?:river|valley|shoes?|brand)\b",  # Jordan as name or brand
    r"\bgeorgia\s+(?:font|style|peach)\b",  # Georgia font/US state context
    r"\bparis\s+(?:fashion|agreement|accords?)\b",  # Paris Agreement is fine to keep
]


def build_search_patterns():
    """Build compiled regex patterns for efficient searching."""
    patterns = {}
    for country, info in COUNTRIES.items():
        # Create pattern that matches any alias as whole word
        alias_patterns = []
        for alias in info["aliases"]:
            # Escape special chars and make case-insensitive
            escaped = re.escape(alias)
            alias_patterns.append(escaped)

        # Combine into single pattern with word boundaries
        combined = r"\b(" + "|".join(alias_patterns) + r")\b"
        patterns[country] = re.compile(combined, re.IGNORECASE)

    return patterns


def extract_country_mentions(text: str, patterns: dict) -> dict[str, list[str]]:
    """Extract all country mentions from text with matched terms."""
    mentions = {}

    for country, pattern in patterns.items():
        matches = pattern.findall(text)
        if matches:
            # Deduplicate while preserving order
            unique_matches = list(dict.fromkeys(matches))
            mentions[country] = unique_matches

    return mentions


def process_parquet_files(parquet_dir: Path, patterns: dict) -> dict:
    """Process all parquet files and extract country mentions."""
    results = {
        "by_year": defaultdict(lambda: defaultdict(list)),
        "by_country": defaultdict(lambda: defaultdict(list)),
        "totals": defaultdict(int),
        "year_totals": defaultdict(lambda: defaultdict(int)),
        "sentences": [],  # For expandable context
    }

    parquet_files = sorted(parquet_dir.glob("*.parquet"))
    print(f"Found {len(parquet_files)} parquet files")

    for pf in parquet_files:
        year = int(pf.stem)
        print(f"Processing {year}...")

        df = pd.read_parquet(pf)

        for _, row in df.iterrows():
            text = row["sentence_text"]
            sentence_id = row["sentence_id"]
            section = row.get("section_title", None)

            mentions = extract_country_mentions(text, patterns)

            if mentions:
                for country, matched_terms in mentions.items():
                    # Store by year
                    results["by_year"][year][country].append(
                        {
                            "sentence_id": sentence_id,
                            "text": text,
                            "section": section,
                            "matched_terms": matched_terms,
                        }
                    )

                    # Store by country
                    results["by_country"][country][year].append(
                        {
                            "sentence_id": sentence_id,
                            "text": text,
                            "section": section,
                            "matched_terms": matched_terms,
                        }
                    )

                    # Update counts
                    results["totals"][country] += 1
                    results["year_totals"][year][country] += 1

    return results


def generate_output_json(results: dict, output_dir: Path):
    """Generate JSON files for the website."""

    # 1. Overview file with totals and regional aggregates
    overview = {
        "total_mentions": sum(results["totals"].values()),
        "countries_mentioned": len(results["totals"]),
        "by_region": {},
        "country_totals": dict(
            sorted(results["totals"].items(), key=lambda x: -x[1])[:50]
        ),
        "years": sorted(results["by_year"].keys()),
    }

    # Calculate regional totals
    for region, countries in REGIONS.items():
        region_total = sum(results["totals"].get(c, 0) for c in countries)
        if region_total > 0:
            overview["by_region"][region] = {
                "total": region_total,
                "countries": {c: results["totals"].get(c, 0) for c in countries if results["totals"].get(c, 0) > 0},
            }

    # 2. Time series data for charts
    time_series = {"years": [], "countries": {}}

    all_years = sorted(results["by_year"].keys())
    time_series["years"] = all_years

    # Get top 20 most mentioned countries for time series
    top_countries = sorted(results["totals"].items(), key=lambda x: -x[1])[:20]

    for country, _ in top_countries:
        time_series["countries"][country] = {
            "iso": COUNTRIES[country]["iso"],
            "region": COUNTRIES[country]["region"],
            "yearly_counts": [results["year_totals"].get(y, {}).get(country, 0) for y in all_years],
            "total": results["totals"][country],
        }

    # 3. Country details with sentences for expandable view
    country_details = {}

    for country, yearly_data in results["by_country"].items():
        if results["totals"][country] >= 5:  # Only include countries with 5+ mentions
            country_details[country] = {
                "iso": COUNTRIES[country]["iso"],
                "region": COUNTRIES[country]["region"],
                "total_mentions": results["totals"][country],
                "by_year": {},
            }

            for year, sentences in yearly_data.items():
                country_details[country]["by_year"][year] = [
                    {"text": s["text"], "section": s["section"], "terms": s["matched_terms"]}
                    for s in sentences[:10]  # Limit to 10 per year for file size
                ]

    # 4. Map data with ISO codes for choropleth
    map_data = {}
    for country, total in results["totals"].items():
        if total > 0:
            iso = COUNTRIES[country]["iso"]
            map_data[iso] = {
                "country": country,
                "total": total,
                "region": COUNTRIES[country]["region"],
            }

    # Write files
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "global_overview.json", "w") as f:
        json.dump(overview, f, indent=2)

    with open(output_dir / "global_time_series.json", "w") as f:
        json.dump(time_series, f, indent=2)

    with open(output_dir / "global_country_details.json", "w") as f:
        json.dump(country_details, f, indent=2)

    with open(output_dir / "global_map_data.json", "w") as f:
        json.dump(map_data, f, indent=2)

    print(f"\nGenerated files in {output_dir}:")
    print(f"  - global_overview.json ({overview['total_mentions']} total mentions)")
    print(f"  - global_time_series.json ({len(time_series['countries'])} countries)")
    print(f"  - global_country_details.json ({len(country_details)} countries with details)")
    print(f"  - global_map_data.json ({len(map_data)} countries for map)")


def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent
    parquet_dir = base_dir / "output_processor"
    output_dir = base_dir / "docs" / "data" / "summary"

    print("Building search patterns...")
    patterns = build_search_patterns()

    print("\nExtracting country mentions from parquet files...")
    results = process_parquet_files(parquet_dir, patterns)

    print("\nGenerating JSON output files...")
    generate_output_json(results, output_dir)

    # Print summary statistics
    print("\n" + "=" * 50)
    print("TOP 20 MOST MENTIONED COUNTRIES")
    print("=" * 50)
    for country, count in sorted(results["totals"].items(), key=lambda x: -x[1])[:20]:
        region = COUNTRIES[country]["region"]
        print(f"{country:25} {count:5} mentions  ({region})")


if __name__ == "__main__":
    main()
