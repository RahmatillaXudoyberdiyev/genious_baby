import json

# path for example: "user_side/translations/relation_to_baby.json"
# key for example: "relation_to_baby_label"

def translate_into(path, data, key=None):
    with open(path, "r", encoding="utf-8") as f:
        translations = json.load(f)
        language = data.get('current_language', 'Uzbek')  
        if key:
            return translations[key][language]
        return translations      

