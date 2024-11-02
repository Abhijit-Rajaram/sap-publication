from django.contrib.auth.models import User
from app.models import * 

def user_info(request):
    print('context processor')
    try:
        user = User.objects.get(id = request.user.id)
        print('user : ',user.username)
    except:
        user = []
    try:
        count = CartItem.objects.filter(user_id = request.user.id).count()
    except:
        count = 0
    return {
        'user': user,
        'count': count,
    }