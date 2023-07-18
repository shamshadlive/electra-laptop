from django.db import models

# Create your models here.


class Banner(models.Model):
    banner_name = models.CharField(max_length=100)
    banner_image = models.ImageField(upload_to='banner/images/')
    banner_url = models.URLField(blank=True,null=True)
    button_text = models.CharField(max_length=10,default='Buy Now')
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.banner_name
