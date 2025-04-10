import json
from django import template

register = template.Library()

@register.filter
def tojson_user(user):
    if not user.is_authenticated:
        return 'null'
    
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role":user.role
    }
    return json.dumps(user_data)
