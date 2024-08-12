from django.contrib import admin
from app.models import Slider,Sub_category,Category,Main_category
from app.models import Section,Product,Product_Image,Additional_Information,Color,Order
# Register your models here.




class Product_Images(admin.TabularInline):
    model = Product_Image



class Additional_Informations(admin.TabularInline):
    model = Additional_Information



class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images,Additional_Informations)










admin.site.register(Slider)
admin.site.register(Main_category)
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Color)




admin.site.register(Section)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)





admin.site.register(Order)
