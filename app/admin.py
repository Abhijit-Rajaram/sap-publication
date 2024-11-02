from django.contrib import admin
from app.models import *

class BookTable(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price')
    
admin.site.register(Book,BookTable)
admin.site.register(Address)
admin.site.register(Degree)
admin.site.register(Department)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)