"""Generate nine-language disease guidance and Streamlit UI strings."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import CLASS_NAMES_PATH, DISEASE_INFO_PATH

UI_STRINGS_PATH = DISEASE_INFO_PATH.parent / "ui_strings.json"


LANGUAGE_NAMES = {
    "en": "English",
    "kn": "ಕನ್ನಡ",
    "hi": "हिन्दी",
    "ta": "தமிழ்",
    "te": "తెలుగు",
    "ml": "മലയാളം",
    "mr": "मराठी",
    "bn": "বাংলা",
    "gu": "ગુજરાતી",
}

INFO_TEXT = {
    "en": {
        "healthy": "Healthy",
        "diseased": "Possible disease",
        "description": "This PlantVillage class represents {name}. The result is a possibility based on leaf appearance, not a laboratory diagnosis.",
        "symptoms": "Look for unusual leaf spots, discoloration, curling, or damage. Compare with healthy leaves from the same crop.",
        "precautions": "Keep plants clean, avoid excess leaf wetness, and clean tools between plants. Remove affected material only when appropriate.",
        "treatment": "Use a control method only after the problem is confirmed locally. Ask an agriculture officer before applying chemicals.",
    },
    "kn": {
        "healthy": "ಆರೋಗ್ಯಕರ",
        "diseased": "ಸಂಭಾವ್ಯ ರೋಗ",
        "description": "ಈ PlantVillage ವರ್ಗವು {name} ಅನ್ನು ಸೂಚಿಸುತ್ತದೆ. ಇದು ಎಲೆಯ ರೂಪದ ಆಧಾರದ ಅಂದಾಜು ಮಾತ್ರ; ಪ್ರಯೋಗಾಲಯದ ನಿರ್ಣಯವಲ್ಲ.",
        "symptoms": "ಎಲೆಯ ಮೇಲಿನ ಕಲೆಗಳು, ಬಣ್ಣ ಬದಲಾವಣೆ, ಮುದುಡುವಿಕೆ ಅಥವಾ ಹಾನಿಯನ್ನು ಗಮನಿಸಿ. ಅದೇ ಬೆಳೆಯ ಆರೋಗ್ಯಕರ ಎಲೆಗಳೊಂದಿಗೆ ಹೋಲಿಸಿ.",
        "precautions": "ಗಿಡಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ, ಎಲೆಗಳು ಹೆಚ್ಚು ಹೊತ್ತು ತೇವವಾಗದಂತೆ ನೋಡಿಕೊಳ್ಳಿ ಮತ್ತು ಗಿಡಗಳ ನಡುವೆ ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ.",
        "treatment": "ಸ್ಥಳೀಯವಾಗಿ ಸಮಸ್ಯೆ ದೃಢಪಟ್ಟ ನಂತರವೇ ನಿಯಂತ್ರಣ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ. ರಾಸಾಯನಿಕ ಬಳಸುವ ಮೊದಲು ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    },
    "hi": {
        "healthy": "स्वस्थ",
        "diseased": "संभावित रोग",
        "description": "यह PlantVillage श्रेणी {name} को दर्शाती है। यह पत्ती के रूप पर आधारित संभावना है, प्रयोगशाला का निदान नहीं।",
        "symptoms": "पत्ती पर असामान्य धब्बे, रंग बदलना, मुड़ना या नुकसान देखें। उसी फसल की स्वस्थ पत्तियों से तुलना करें।",
        "precautions": "पौधों को साफ रखें, पत्तियों को लंबे समय तक गीला न रहने दें और पौधों के बीच औजार साफ करें।",
        "treatment": "स्थानीय पुष्टि के बाद ही नियंत्रण उपाय अपनाएँ। रसायन लगाने से पहले कृषि अधिकारी से सलाह लें।",
    },
    "ta": {
        "healthy": "ஆரோக்கியமானது",
        "diseased": "சாத்தியமான நோய்",
        "description": "இந்த PlantVillage வகுப்பு {name} என்பதை குறிக்கிறது. இது இலை தோற்றத்தின் அடிப்படையிலான சாத்தியம் மட்டுமே; ஆய்வகத் தீர்வு அல்ல.",
        "symptoms": "இலையில் புள்ளிகள், நிறமாற்றம், சுருட்டல் அல்லது சேதம் உள்ளதா கவனிக்கவும். அதே பயிரின் ஆரோக்கியமான இலைகளுடன் ஒப்பிடவும்.",
        "precautions": "செடிகளை சுத்தமாக வைத்துக் கொள்ளவும், இலைகள் நீண்ட நேரம் ஈரமாக இருக்காமல் பார்த்துக் கொள்ளவும், கருவிகளை சுத்தம் செய்யவும்.",
        "treatment": "உள்ளூரில் உறுதி செய்த பிறகே கட்டுப்பாட்டு முறையைப் பயன்படுத்தவும். இரசாயனம் பயன்படுத்தும் முன் வேளாண் அலுவலரை அணுகவும்.",
    },
    "te": {
        "healthy": "ఆరోగ్యకరం",
        "diseased": "సంభావ్య వ్యాధి",
        "description": "ఈ PlantVillage తరగతి {name}ను సూచిస్తుంది. ఇది ఆకు రూపం ఆధారంగా వచ్చిన అవకాశం మాత్రమే; ప్రయోగశాల నిర్ధారణ కాదు.",
        "symptoms": "ఆకుపై మచ్చలు, రంగు మారడం, ముడుచుకోవడం లేదా నష్టం ఉందా చూడండి. అదే పంటలోని ఆరోగ్యకరమైన ఆకులతో పోల్చండి.",
        "precautions": "మొక్కలను శుభ్రంగా ఉంచండి, ఆకులు ఎక్కువసేపు తడిగా ఉండనివ్వకండి, మొక్కల మధ్య పనిముట్లను శుభ్రం చేయండి.",
        "treatment": "స్థానికంగా సమస్యను నిర్ధారించిన తర్వాతే నియంత్రణ చర్యలు తీసుకోండి. రసాయనాలు వాడే ముందు వ్యవసాయ అధికారిని సంప్రదించండి.",
    },
    "ml": {
        "healthy": "ആരോഗ്യമുള്ളത്",
        "diseased": "സാധ്യമായ രോഗം",
        "description": "ഈ PlantVillage വിഭാഗം {name}നെ സൂചിപ്പിക്കുന്നു. ഇലയുടെ രൂപത്തെ അടിസ്ഥാനമാക്കിയുള്ള സാധ്യത മാത്രമാണിത്; ലാബ് പരിശോധനയല്ല.",
        "symptoms": "ഇലയിൽ പാടുകൾ, നിറമാറ്റം, ചുരുളൽ, കേടുപാടുകൾ എന്നിവയുണ്ടോ നോക്കുക. അതേ വിളയിലെ ആരോഗ്യകരമായ ഇലകളുമായി താരതമ്യം ചെയ്യുക.",
        "precautions": "ചെടികൾ വൃത്തിയായി സൂക്ഷിക്കുക, ഇലകൾ ഏറെ നേരം നനഞ്ഞിരിക്കാതിരിക്കുക, ചെടികൾക്കിടയിൽ ഉപകരണങ്ങൾ വൃത്തിയാക്കുക.",
        "treatment": "പ്രാദേശികമായി രോഗം സ്ഥിരീകരിച്ചശേഷം മാത്രം നിയന്ത്രണ മാർഗം സ്വീകരിക്കുക. രാസവസ്തുക്കൾ ഉപയോഗിക്കുന്നതിന് മുമ്പ് കൃഷി ഉദ്യോഗസ്ഥനോട് ചോദിക്കുക.",
    },
    "mr": {
        "healthy": "निरोगी",
        "diseased": "संभाव्य रोग",
        "description": "हा PlantVillage वर्ग {name} दर्शवतो. हा पानाच्या दिसण्यावर आधारित अंदाज आहे; प्रयोगशाळेतील निदान नाही.",
        "symptoms": "पानांवरील डाग, रंग बदल, वाकणे किंवा नुकसान तपासा. त्याच पिकाच्या निरोगी पानांशी तुलना करा.",
        "precautions": "झाडे स्वच्छ ठेवा, पाने जास्त वेळ ओली राहू देऊ नका आणि झाडांमधील साधने स्वच्छ करा.",
        "treatment": "स्थानिक पातळीवर खात्री झाल्यानंतरच नियंत्रण उपाय करा. रसायने वापरण्यापूर्वी कृषी अधिकाऱ्यांचा सल्ला घ्या.",
    },
    "bn": {
        "healthy": "সুস্থ",
        "diseased": "সম্ভাব্য রোগ",
        "description": "এই PlantVillage শ্রেণিটি {name} বোঝায়। এটি পাতার চেহারার ভিত্তিতে একটি সম্ভাবনা, পরীক্ষাগারের রোগনির্ণয় নয়।",
        "symptoms": "পাতায় অস্বাভাবিক দাগ, রঙের পরিবর্তন, কুঁকড়ে যাওয়া বা ক্ষতি দেখুন। একই ফসলের সুস্থ পাতার সঙ্গে তুলনা করুন।",
        "precautions": "গাছ পরিষ্কার রাখুন, পাতা দীর্ঘক্ষণ ভেজা থাকতে দেবেন না এবং গাছের মধ্যে সরঞ্জাম পরিষ্কার করুন।",
        "treatment": "স্থানীয়ভাবে সমস্যা নিশ্চিত হওয়ার পরেই নিয়ন্ত্রণের ব্যবস্থা নিন। রাসায়নিক ব্যবহারের আগে কৃষি কর্মকর্তার পরামর্শ নিন।",
    },
    "gu": {
        "healthy": "તંદુરસ્ત",
        "diseased": "સંભવિત રોગ",
        "description": "આ PlantVillage વર્ગ {name} દર્શાવે છે. આ પાનના દેખાવ પર આધારિત સંભાવના છે, પ્રયોગશાળાનું નિદાન નથી.",
        "symptoms": "પાન પર અસામાન્ય ડાઘ, રંગમાં ફેરફાર, વળાંક અથવા નુકસાન જુઓ. એ જ પાકનાં તંદુરસ્ત પાન સાથે સરખાવો.",
        "precautions": "છોડ સ્વચ્છ રાખો, પાન લાંબા સમય સુધી ભીના ન રહેવા દો અને છોડ વચ્ચે સાધનો સાફ કરો.",
        "treatment": "સ્થાનિક રીતે સમસ્યાની ખાતરી થયા પછી જ નિયંત્રણનો ઉપાય કરો. રસાયણ વાપરતાં પહેલાં કૃષિ અધિકારીની સલાહ લો.",
    },
}

UI_TEXT = {
    "en": {
        "title": "AI Crop Disease Detection System", "subtitle": "AMC Engineering College | Department of ISE",
        "about": "About", "how_to": "How to use", "supported": "Supported crops",
        "about_text": "Upload a clear leaf photo to receive a possible disease prediction.",
        "step1": "1. Choose a JPG, JPEG, or PNG leaf image.", "step2": "2. Preview the image.",
        "step3": "3. Select Detect Disease.", "crop_list": "Apple, tomato, potato, grape, corn, pepper, peach, blueberry, cherry and more.",
        "threshold": "Confidence threshold", "language": "Language", "upload": "Choose a crop leaf image",
        "detect": "Detect Disease", "analyzing": "Analyzing the leaf...", "healthy": "HEALTHY LEAF",
        "diseased": "DISEASED LEAF", "uncertain": "NOT SURE - CLEARER PHOTO NEEDED",
        "crop": "Crop", "confidence": "Confidence", "top3": "Top 3 predictions",
        "description": "Description", "symptoms": "Symptoms", "precautions": "Precautions",
        "treatment": "Treatment", "audio": "Audio explanation", "download": "Download audio",
        "too_large": "This image is larger than 20 MB. Please resize it and try again.",
        "corrupt": "The image is corrupted or cannot be opened.",
        "model_missing": "Model file not found. Run python src/train.py first.",
        "not_sure": "Not sure, please upload a clearer leaf photo.",
        "footer": "Team: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | Guide: Prof. Tejashree",
    },
    "kn": {
        "title": "AI ಬೆಳೆ ರೋಗ ಪತ್ತೆ ವ್ಯವಸ್ಥೆ", "subtitle": "AMC ಎಂಜಿನಿಯರಿಂಗ್ ಕಾಲೇಜು | ISE ವಿಭಾಗ",
        "about": "ವಿವರ", "how_to": "ಬಳಸುವ ವಿಧಾನ", "supported": "ಬೆಂಬಲಿತ ಬೆಳೆಗಳು",
        "about_text": "ರೋಗದ ಸಾಧ್ಯತೆಯನ್ನು ತಿಳಿಯಲು ಎಲೆಯ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
        "step1": "1. JPG, JPEG ಅಥವಾ PNG ಎಲೆಯ ಚಿತ್ರ ಆಯ್ಕೆಮಾಡಿ.", "step2": "2. ಚಿತ್ರವನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "step3": "3. ರೋಗ ಪತ್ತೆಮಾಡಿ ಆಯ್ಕೆಮಾಡಿ.", "crop_list": "ಸೇಬು, ಟೊಮೇಟೊ, ಆಲೂಗಡ್ಡೆ, ದ್ರಾಕ್ಷಿ, ಜೋಳ, ಮೆಣಸು, ಪೀಚ್ ಮತ್ತು ಇತರೆ.",
        "threshold": "ವಿಶ್ವಾಸ ಮಿತಿ", "language": "ಭಾಷೆ", "upload": "ಬೆಳೆ ಎಲೆಯ ಚಿತ್ರ ಆಯ್ಕೆಮಾಡಿ",
        "detect": "ರೋಗ ಪತ್ತೆಮಾಡಿ", "analyzing": "ಎಲೆಯನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...", "healthy": "ಆರೋಗ್ಯಕರ ಎಲೆ",
        "diseased": "ರೋಗದ ಸಾಧ್ಯತೆ", "uncertain": "ಖಚಿತವಿಲ್ಲ - ಸ್ಪಷ್ಟ ಚಿತ್ರ ನೀಡಿ",
        "crop": "ಬೆಳೆ", "confidence": "ವಿಶ್ವಾಸ", "top3": "ಅಗ್ರ 3 ಫಲಿತಾಂಶಗಳು",
        "description": "ವಿವರಣೆ", "symptoms": "ಲಕ್ಷಣಗಳು", "precautions": "ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು",
        "treatment": "ಚಿಕಿತ್ಸೆ", "audio": "ಧ್ವನಿ ವಿವರಣೆ", "download": "ಧ್ವನಿ ಡೌನ್‌ಲೋಡ್",
        "too_large": "ಚಿತ್ರ 20 MB ಗಿಂತ ದೊಡ್ಡದು. ದಯವಿಟ್ಟು ಚಿಕ್ಕದಾಗಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "corrupt": "ಚಿತ್ರ ತೆರೆಯಲಾಗಲಿಲ್ಲ ಅಥವಾ ಹಾನಿಗೊಂಡಿದೆ.",
        "model_missing": "ಮಾದರಿ ಇಲ್ಲ. ಮೊದಲು python src/train.py ಚಲಾಯಿಸಿ.",
        "not_sure": "ಖಚಿತವಿಲ್ಲ; ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟ ಎಲೆಯ ಚಿತ್ರ ನೀಡಿ.",
        "footer": "ತಂಡ: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | ಮಾರ್ಗದರ್ಶಕಿ: Prof. Tejashree",
    },
    "hi": {
        "title": "एआई फसल रोग पहचान प्रणाली", "subtitle": "एएमसी इंजीनियरिंग कॉलेज | आईएसई विभाग",
        "about": "परिचय", "how_to": "उपयोग कैसे करें", "supported": "समर्थित फसलें",
        "about_text": "संभावित रोग पहचान के लिए पत्ती की साफ तस्वीर अपलोड करें।",
        "step1": "1. JPG, JPEG या PNG पत्ती की तस्वीर चुनें।", "step2": "2. तस्वीर देखें।",
        "step3": "3. रोग पहचानें चुनें।", "crop_list": "सेब, टमाटर, आलू, अंगूर, मक्का, मिर्च, आड़ू, ब्लूबेरी, चेरी आदि।",
        "threshold": "विश्वास सीमा", "language": "भाषा", "upload": "फसल के पत्ते की तस्वीर चुनें",
        "detect": "रोग पहचानें", "analyzing": "पत्ती की जाँच हो रही है...", "healthy": "स्वस्थ पत्ती",
        "diseased": "संभावित रोगग्रस्त पत्ती", "uncertain": "निश्चित नहीं - स्पष्ट तस्वीर दें",
        "crop": "फसल", "confidence": "विश्वास", "top3": "शीर्ष 3 अनुमान",
        "description": "विवरण", "symptoms": "लक्षण", "precautions": "सावधानियाँ",
        "treatment": "उपचार", "audio": "ऑडियो विवरण", "download": "ऑडियो डाउनलोड करें",
        "too_large": "तस्वीर 20 MB से बड़ी है। कृपया इसे छोटा करके फिर प्रयास करें.",
        "corrupt": "तस्वीर खराब है या खुल नहीं सकी।",
        "model_missing": "मॉडल नहीं मिला। पहले python src/train.py चलाएँ।",
        "not_sure": "निश्चित नहीं; कृपया पत्ती की स्पष्ट तस्वीर दें।",
        "footer": "टीम: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | मार्गदर्शक: Prof. Tejashree",
    },
    "ta": {
        "title": "AI பயிர் நோய் கண்டறிதல் அமைப்பு", "subtitle": "AMC பொறியியல் கல்லூரி | ISE துறை",
        "about": "பற்றி", "how_to": "பயன்படுத்துவது எப்படி", "supported": "ஆதரிக்கப்படும் பயிர்கள்",
        "about_text": "சாத்தியமான நோய் கணிப்பைப் பெற தெளிவான இலைப் படத்தைப் பதிவேற்றவும்.",
        "step1": "1. JPG, JPEG அல்லது PNG இலைப் படத்தைத் தேர்ந்தெடுக்கவும்.", "step2": "2. படத்தைப் பார்க்கவும்.",
        "step3": "3. நோயைக் கண்டறி என்பதைத் தேர்ந்தெடுக்கவும்.", "crop_list": "ஆப்பிள், தக்காளி, உருளைக்கிழங்கு, திராட்சை, சோளம், மிளகு மற்றும் பல.",
        "threshold": "நம்பிக்கை வரம்பு", "language": "மொழி", "upload": "பயிர் இலைப் படத்தைத் தேர்ந்தெடுக்கவும்",
        "detect": "நோயைக் கண்டறி", "analyzing": "இலை ஆய்வு செய்யப்படுகிறது...", "healthy": "ஆரோக்கியமான இலை",
        "diseased": "நோய் இருக்கலாம்", "uncertain": "உறுதி இல்லை - தெளிவான படத்தைத் தரவும்",
        "crop": "பயிர்", "confidence": "நம்பிக்கை", "top3": "முதல் 3 கணிப்புகள்",
        "description": "விளக்கம்", "symptoms": "அறிகுறிகள்", "precautions": "முன்னெச்சரிக்கைகள்",
        "treatment": "சிகிச்சை", "audio": "ஒலி விளக்கம்", "download": "ஒலியைப் பதிவிறக்கவும்",
        "too_large": "படம் 20 MB-ஐ விட பெரியது. சிறியதாக்கி மீண்டும் முயற்சிக்கவும்.",
        "corrupt": "படம் சேதமடைந்துள்ளது அல்லது திறக்க முடியவில்லை.",
        "model_missing": "மாதிரி இல்லை. முதலில் python src/train.py இயக்கவும்.",
        "not_sure": "உறுதி இல்லை; தெளிவான இலைப் படத்தைப் பதிவேற்றவும்.",
        "footer": "குழு: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | வழிகாட்டி: Prof. Tejashree",
    },
    "te": {
        "title": "AI పంట వ్యాధి గుర్తింపు వ్యవస్థ", "subtitle": "AMC ఇంజినీరింగ్ కళాశాల | ISE విభాగం",
        "about": "గురించి", "how_to": "ఎలా ఉపయోగించాలి", "supported": "మద్దతు ఉన్న పంటలు",
        "about_text": "సంభావ్య వ్యాధి అంచనా కోసం స్పష్టమైన ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి.",
        "step1": "1. JPG, JPEG లేదా PNG ఆకు చిత్రాన్ని ఎంచుకోండి.", "step2": "2. చిత్రాన్ని చూడండి.",
        "step3": "3. వ్యాధిని గుర్తించండి ఎంచుకోండి.", "crop_list": "ఆపిల్, టమాటా, బంగాళాదుంప, ద్రాక్ష, మొక్కజొన్న, మిరియాలు మరియు ఇతరాలు.",
        "threshold": "నమ్మక పరిమితి", "language": "భాష", "upload": "పంట ఆకు చిత్రాన్ని ఎంచుకోండి",
        "detect": "వ్యాధిని గుర్తించండి", "analyzing": "ఆకును పరిశీలిస్తోంది...", "healthy": "ఆరోగ్యకరమైన ఆకు",
        "diseased": "సంభావ్య వ్యాధి", "uncertain": "నిర్ధారణ కాలేదు - స్పష్టమైన చిత్రం ఇవ్వండి",
        "crop": "పంట", "confidence": "నమ్మకం", "top3": "మొదటి 3 అంచనాలు",
        "description": "వివరణ", "symptoms": "లక్షణాలు", "precautions": "జాగ్రత్తలు",
        "treatment": "చికిత్స", "audio": "ఆడియో వివరణ", "download": "ఆడియోను డౌన్‌లోడ్ చేయండి",
        "too_large": "చిత్రం 20 MB కంటే పెద్దది. చిన్నదిగా చేసి మళ్లీ ప్రయత్నించండి.",
        "corrupt": "చిత్రం పాడైంది లేదా తెరవలేకపోయాం.",
        "model_missing": "మోడల్ లేదు. ముందుగా python src/train.py నడపండి.",
        "not_sure": "నిర్ధారణ కాలేదు; స్పష్టమైన ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి.",
        "footer": "బృందం: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | మార్గదర్శి: Prof. Tejashree",
    },
    "ml": {
        "title": "AI വിളരോഗ നിർണയ സംവിധാനം", "subtitle": "AMC എഞ്ചിനീയറിംഗ് കോളേജ് | ISE വിഭാഗം",
        "about": "വിവരം", "how_to": "ഉപയോഗിക്കുന്ന വിധം", "supported": "പിന്തുണയുള്ള വിളകൾ",
        "about_text": "സാധ്യമായ രോഗ പ്രവചനം ലഭിക്കാൻ ഇലയുടെ വ്യക്തമായ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക.",
        "step1": "1. JPG, JPEG അല്ലെങ്കിൽ PNG ഇല ചിത്രം തിരഞ്ഞെടുക്കുക.", "step2": "2. ചിത്രം പരിശോധിക്കുക.",
        "step3": "3. രോഗം കണ്ടെത്തുക തിരഞ്ഞെടുക്കുക.", "crop_list": "ആപ്പിൾ, തക്കാളി, ഉരുളക്കിഴങ്ങ്, മുന്തിരി, ചോളം, മുളക് എന്നിവ.",
        "threshold": "വിശ്വാസ പരിധി", "language": "ഭാഷ", "upload": "വിളയുടെ ഇല ചിത്രം തിരഞ്ഞെടുക്കുക",
        "detect": "രോഗം കണ്ടെത്തുക", "analyzing": "ഇല പരിശോധിക്കുന്നു...", "healthy": "ആരോഗ്യമുള്ള ഇല",
        "diseased": "സാധ്യമായ രോഗം", "uncertain": "ഉറപ്പില്ല - വ്യക്തമായ ചിത്രം നൽകുക",
        "crop": "വിള", "confidence": "വിശ്വാസം", "top3": "മികച്ച 3 പ്രവചനങ്ങൾ",
        "description": "വിവരണം", "symptoms": "ലക്ഷണങ്ങൾ", "precautions": "മുൻകരുതലുകൾ",
        "treatment": "ചികിത്സ", "audio": "ശബ്ദ വിശദീകരണം", "download": "ഓഡിയോ ഡൗൺലോഡ് ചെയ്യുക",
        "too_large": "ചിത്രം 20 MB-ൽ കൂടുതലാണ്. വലുപ്പം കുറച്ച് വീണ്ടും ശ്രമിക്കുക.",
        "corrupt": "ചിത്രം കേടായിരിക്കുന്നു അല്ലെങ്കിൽ തുറക്കാനായില്ല.",
        "model_missing": "മോഡൽ കണ്ടെത്തിയില്ല. ആദ്യം python src/train.py പ്രവർത്തിപ്പിക്കുക.",
        "not_sure": "ഉറപ്പില്ല; വ്യക്തമായ ഇല ചിത്രം അപ്‌ലോഡ് ചെയ്യുക.",
        "footer": "ടീം: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | ഗൈഡ്: Prof. Tejashree",
    },
    "mr": {
        "title": "एआय पीक रोग ओळख प्रणाली", "subtitle": "एएमसी अभियांत्रिकी महाविद्यालय | आयएसई विभाग",
        "about": "माहिती", "how_to": "वापरण्याची पद्धत", "supported": "समर्थित पिके",
        "about_text": "संभाव्य रोगाचा अंदाज मिळवण्यासाठी पानाचा स्पष्ट फोटो अपलोड करा.",
        "step1": "1. JPG, JPEG किंवा PNG पानाचा फोटो निवडा.", "step2": "2. फोटो पाहा.",
        "step3": "3. रोग ओळखा निवडा.", "crop_list": "सफरचंद, टोमॅटो, बटाटा, द्राक्ष, मका, मिरची, पीच आणि इतर.",
        "threshold": "विश्वास मर्यादा", "language": "भाषा", "upload": "पिकाच्या पानाचा फोटो निवडा",
        "detect": "रोग ओळखा", "analyzing": "पान तपासत आहे...", "healthy": "निरोगी पान",
        "diseased": "संभाव्य रोग", "uncertain": "खात्री नाही - स्पष्ट फोटो द्या",
        "crop": "पीक", "confidence": "विश्वास", "top3": "पहिले 3 अंदाज",
        "description": "वर्णन", "symptoms": "लक्षणे", "precautions": "काळजी",
        "treatment": "उपचार", "audio": "ध्वनी स्पष्टीकरण", "download": "ऑडिओ डाउनलोड करा",
        "too_large": "फोटो 20 MB पेक्षा मोठा आहे. आकार कमी करून पुन्हा प्रयत्न करा.",
        "corrupt": "फोटो खराब आहे किंवा उघडता आला नाही.",
        "model_missing": "मॉडेल सापडले नाही. आधी python src/train.py चालवा.",
        "not_sure": "खात्री नाही; कृपया पानाचा स्पष्ट फोटो अपलोड करा.",
        "footer": "संघ: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | मार्गदर्शक: Prof. Tejashree",
    },
    "bn": {
        "title": "এআই ফসল রোগ শনাক্তকরণ ব্যবস্থা", "subtitle": "এএমসি ইঞ্জিনিয়ারিং কলেজ | আইএসই বিভাগ",
        "about": "পরিচিতি", "how_to": "ব্যবহারের নিয়ম", "supported": "সমর্থিত ফসল",
        "about_text": "সম্ভাব্য রোগের অনুমান পেতে পাতার পরিষ্কার ছবি আপলোড করুন।",
        "step1": "১. JPG, JPEG বা PNG পাতার ছবি বেছে নিন।", "step2": "২. ছবিটি দেখুন।",
        "step3": "৩. রোগ শনাক্ত করুন নির্বাচন করুন।", "crop_list": "আপেল, টমেটো, আলু, আঙুর, ভুট্টা, মরিচ, পিচ, ব্লুবেরি, চেরি ইত্যাদি।",
        "threshold": "বিশ্বাসের সীমা", "language": "ভাষা", "upload": "ফসলের পাতার ছবি বেছে নিন",
        "detect": "রোগ শনাক্ত করুন", "analyzing": "পাতা পরীক্ষা করা হচ্ছে...", "healthy": "সুস্থ পাতা",
        "diseased": "সম্ভাব্য রোগ", "uncertain": "নিশ্চিত নয় - পরিষ্কার ছবি দিন",
        "crop": "ফসল", "confidence": "বিশ্বাস", "top3": "সেরা ৩টি অনুমান",
        "description": "বিবরণ", "symptoms": "লক্ষণ", "precautions": "সতর্কতা",
        "treatment": "চিকিৎসা", "audio": "অডিও বিবরণ", "download": "অডিও ডাউনলোড করুন",
        "too_large": "ছবিটি ২০ MB-এর বেশি। ছোট করে আবার চেষ্টা করুন।",
        "corrupt": "ছবিটি নষ্ট বা খোলা যাচ্ছে না।",
        "model_missing": "মডেল পাওয়া যায়নি। আগে python src/train.py চালান।",
        "not_sure": "নিশ্চিত নয়; পাতার পরিষ্কার ছবি আপলোড করুন।",
        "footer": "দল: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | নির্দেশক: Prof. Tejashree",
    },
    "gu": {
        "title": "AI પાક રોગ ઓળખ પ્રણાલી", "subtitle": "AMC એન્જિનિયરિંગ કોલેજ | ISE વિભાગ",
        "about": "વિશે", "how_to": "ઉપયોગ કેવી રીતે કરવો", "supported": "સમર્થિત પાક",
        "about_text": "સંભવિત રોગનું અનુમાન મેળવવા પાનનો સ્પષ્ટ ફોટો અપલોડ કરો.",
        "step1": "1. JPG, JPEG અથવા PNG પાનનો ફોટો પસંદ કરો.", "step2": "2. ફોટો જુઓ.",
        "step3": "3. રોગ ઓળખો પસંદ કરો.", "crop_list": "સફરજન, ટામેટાં, બટાકા, દ્રાક્ષ, મકાઈ, મરચાં, પીચ અને અન્ય.",
        "threshold": "વિશ્વાસ મર્યાદા", "language": "ભાષા", "upload": "પાકના પાનનો ફોટો પસંદ કરો",
        "detect": "રોગ ઓળખો", "analyzing": "પાન તપાસી રહ્યા છીએ...", "healthy": "તંદુરસ્ત પાન",
        "diseased": "સંભવિત રોગ", "uncertain": "ખાતરી નથી - સ્પષ્ટ ફોટો આપો",
        "crop": "પાક", "confidence": "વિશ્વાસ", "top3": "ટોચના 3 અનુમાન",
        "description": "વર્ણન", "symptoms": "લક્ષણો", "precautions": "સાવચેતીઓ",
        "treatment": "સારવાર", "audio": "ઓડિયો સમજણ", "download": "ઓડિયો ડાઉનલોડ કરો",
        "too_large": "ફોટો 20 MB કરતાં મોટો છે. નાનો કરીને ફરી પ્રયાસ કરો.",
        "corrupt": "ફોટો બગડેલો છે અથવા ખોલી શકાયો નથી.",
        "model_missing": "મોડેલ મળ્યું નથી. પહેલાં python src/train.py ચલાવો.",
        "not_sure": "ખાતરી નથી; કૃપા કરીને પાનનો સ્પષ્ટ ફોટો અપલોડ કરો.",
        "footer": "ટીમ: Muskan Gupta P, Priyanka P, Punya H N, Thanushree G M | માર્ગદર્શક: Prof. Tejashree",
    },
}

GENERAL_NOTES = {
    "en": "General educational guidance only. Ask a local agriculture officer for diagnosis and treatment.",
    "kn": "ಇದು ಸಾಮಾನ್ಯ ಶೈಕ್ಷಣಿಕ ಮಾರ್ಗದರ್ಶನ ಮಾತ್ರ. ನಿರ್ಣಯ ಮತ್ತು ಚಿಕಿತ್ಸೆಗೆ ಸ್ಥಳೀಯ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
    "hi": "यह केवल सामान्य शैक्षिक जानकारी है। निदान और उपचार के लिए स्थानीय कृषि अधिकारी से सलाह लें।",
    "ta": "இது பொதுவான கல்வி வழிகாட்டுதல் மட்டுமே. நோயறிதல் மற்றும் சிகிச்சைக்கு உள்ளூர் வேளாண் அலுவலரை அணுகவும்.",
    "te": "ఇది సాధారణ విద్యా మార్గదర్శకం మాత్రమే. నిర్ధారణ, చికిత్స కోసం స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి.",
    "ml": "ഇത് പൊതുവായ വിദ്യാഭ്യാസ മാർഗനിർദേശം മാത്രമാണ്. രോഗനിർണയത്തിനും ചികിത്സയ്ക്കും പ്രാദേശിക കൃഷി ഉദ്യോഗസ്ഥനെ സമീപിക്കുക.",
    "mr": "ही केवळ सामान्य शैक्षणिक माहिती आहे. निदान आणि उपचारासाठी स्थानिक कृषी अधिकाऱ्यांचा सल्ला घ्या.",
    "bn": "এটি কেবল সাধারণ শিক্ষামূলক নির্দেশনা। রোগ নির্ণয় ও চিকিৎসার জন্য স্থানীয় কৃষি কর্মকর্তার পরামর্শ নিন।",
    "gu": "આ માત્ર સામાન્ય શૈક્ષણિક માર્ગદર્શન છે. નિદાન અને સારવાર માટે સ્થાનિક કૃષિ અધિકારીની સલાહ લો.",
}


def readable_class_name(class_name: str) -> tuple[str, str]:
    """Make a readable label and crop name from a PlantVillage folder."""
    crop_part, _, disease_part = class_name.partition("___")
    crop = crop_part.replace("_", " ").replace(",", "").strip().title()
    display = " ".join(
        part.strip().title()
        for part in (crop_part.replace("_", " ").replace(",", ""), disease_part.replace("_", " "))
        if part.strip()
    )
    return display, crop


def generate_disease_information(class_names: list[str]) -> dict:
    """Create entries in every requested language for all model labels."""
    result = {}
    for class_name in class_names:
        display_name, crop = readable_class_name(class_name)
        healthy = "healthy" in class_name.lower()
        localized = {}
        for language, text in INFO_TEXT.items():
            localized[language] = {
                "display_name": display_name,
                "crop": crop,
                "status": text["healthy"] if healthy else text["diseased"],
                "description": text["description"].format(name=display_name),
                "symptoms": text["symptoms"],
                "precautions": text["precautions"],
                "treatment": text["treatment"],
            }
        entry = dict(localized["en"])
        entry["status"] = "healthy" if healthy else "diseased"
        entry["translations"] = localized
        result[class_name] = entry
    result["_general_note"] = GENERAL_NOTES
    return result


def generate_localization_files(class_names: list[str]) -> dict:
    """Write multilingual disease information and UI labels for class names."""
    if not isinstance(class_names, list) or not class_names:
        raise ValueError("The class name list is empty.")
    if len(class_names) != len(set(class_names)):
        raise ValueError("class_names.json contains duplicate class names.")
    if set(INFO_TEXT) != set(LANGUAGE_NAMES) or set(UI_TEXT) != set(LANGUAGE_NAMES):
        raise ValueError("Disease and UI translations must cover the same languages.")

    disease_info = generate_disease_information(class_names)
    if set(disease_info) - {"_general_note"} != set(class_names):
        raise ValueError("Disease information keys do not match class names.")

    DISEASE_INFO_PATH.parent.mkdir(parents=True, exist_ok=True)
    DISEASE_INFO_PATH.write_text(
        json.dumps(disease_info, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    UI_STRINGS_PATH.write_text(
        json.dumps(
            {
                language: {
                    "language_name": LANGUAGE_NAMES[language],
                    **strings,
                }
                for language, strings in UI_TEXT.items()
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return disease_info


def main() -> None:
    if not CLASS_NAMES_PATH.is_file():
        raise FileNotFoundError(
            "Class names are not available. Run python src/inspect_data.py first."
        )
    class_names = json.loads(CLASS_NAMES_PATH.read_text(encoding="utf-8"))
    generate_localization_files(class_names)

    print(f"Class names loaded: {len(class_names)}")
    print(f"Languages generated: {', '.join(INFO_TEXT)}")
    print(f"Disease information: {DISEASE_INFO_PATH}")
    print(f"UI strings: {UI_STRINGS_PATH}")


if __name__ == "__main__":
    main()
