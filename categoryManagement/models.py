from django.db import models
from django.utils.text import slugify
# Create your models here.


class Category(models.Model):
    cat_name = models.CharField(max_length=50,unique=True)
    cat_slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    parent_cat = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.cat_slug:
            self.cat_slug = slugify(self.cat_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.cat_name
        