from io import BytesIO
from django.core.files import File
from PIL import Image
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Categories' # Plural Name Categories
        ordering = ('name',)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) # FK Category
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
   

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.name
    
    def price_display(self):
        return self.price / 100 # Price divide by 100

    def get_thumbnail(self): # gwt thumbnail of image if any
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_tbn(self.image) # call make thubnial funtiona and pass image 
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/350x150' # default Image

    # Make Thubnail Function
    def make_tbn(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        tbn_io = BytesIO()
        img.save(tbn_io, 'JPEG', quality=85)

        thumbnail = File(tbn_io, name=image.name)

        return thumbnail

        