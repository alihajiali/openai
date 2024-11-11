import requests



# gemini

headers = {
    'Content-Type': 'application/json',
}

params = {
    'key': 'AIzaSyBRcAVfNZJZcSuOLndUyXEbuWC6_QYMFe8',
}

json_data = {
    'contents': [
        {
            'parts': [
                {
                    'text': 'دمای هوای قم در ۷ روز آینده',
                },
            ],
        },
    ],
}

response = requests.post(
    'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent',
    params=params,
    headers=headers,
    json=json_data,
)
