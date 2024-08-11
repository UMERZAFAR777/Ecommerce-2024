from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save




# Create your models here.

class Slider(models.Model):
    DISCOUNT_DEAL = (
        ('new_arrival', 'New Arrival'),
        ('hot_deals', 'Hot Deals'),
    )

    img = models.ImageField(upload_to='media/slider_img/',max_length= 200)
    brand_name = models.CharField(max_length= 200)
    discount_deal = models.CharField(choices=DISCOUNT_DEAL,max_length= 200)
    sale = models.IntegerField()
    discount = models.IntegerField()
    link = models.CharField(max_length= 200)


    def __str__(self) -> str:
        return self.brand_name


class Main_category(models.Model):
    name = models.CharField(max_length= 200)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    main_category = models.ForeignKey(Main_category,on_delete=models.CASCADE)
    name = models.CharField(max_length= 200)

    def __str__(self) -> str:
        return self.name +'--'+ self.main_category.name

class Sub_category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length= 200)

    def __str__(self) -> str:
        return self.category.main_category.name +'--'+ self.category.name +'--'+ self.name



class Section(models.Model):
    name = models.CharField(max_length= 200)

    def __str__(self) -> str:
        return self.name
    
class Color(models.Model):
    color_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.color_name    

class Product(models.Model):
    color_name = models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
    section = models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    brand_name = models.CharField(max_length=200)
    img = models.CharField(max_length=200)
    total_quantity = models.IntegerField()
    availability = models.IntegerField()
    tax = models.IntegerField(null=True)
    packing_cost = models.IntegerField(null=True)
    price = models.IntegerField()
    discount = models.IntegerField()
    model_name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Product_information = RichTextField()
    Description = RichTextField()
    link = models.CharField(max_length=200)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)


    def __str__(self) -> str:
        return self.brand_name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.brand_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)



class Product_Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.CharField(max_length=200)

class Additional_Information(models.Model): 
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    specification = models.CharField(max_length=200)      
    detail = models.CharField(max_length=200)      





