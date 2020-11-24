import json

def get_text(request):
    text = request.text
    if text is None:
        return None
    
    try:
        return json.loads(text)
    except ValueError:
        return None
    return None