from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from.utils import sendTransaction
import hashlib
from . import wallet

# Create your models here.

class Article(models.Model):
    DRAFT= 'DRRAFT'
    PUBLISHED='PUBLISHED'
    STATUS_CHOICES=(
        (DRAFT,'Draft'),
        (PUBLISHED,'Published')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default=PUBLISHED)

    TECNOLOGY = 'TC'
    BLOCKCHAIN='BC'
    SPORT = 'SP'
    GENERAL_CULTURE = 'GC'
    ANIME ='AN'
    FREE_TIME = 'FT'
    CATEGORIES = [
         (TECNOLOGY,'Technology'),
        (BLOCKCHAIN,'Blockchain'),
         ( SPORT,'Sport'),
        (GENERAL_CULTURE,'General culture'),
        (ANIME ,'Anime'),
        (FREE_TIME,'Free time')
    ]
    category= models.CharField(choices= CATEGORIES,default='FT',max_length=2)
    title= models.CharField(max_length=250)
    slug= models.SlugField(max_length=250,null=False, unique=True)
    img= models.ImageField(upload_to="images/", blank=True, null=True)
    content= models.TextField(max_length=5000)
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created= models.DateTimeField(default=timezone.now)
    published=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=66, default=None, null=True)
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)

    def writeOnChain(self):
        self.address = wallet.address
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()


    class Meta:
        ordering = ("-updated","-published")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article-detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article,self).save(*args, **kwargs)