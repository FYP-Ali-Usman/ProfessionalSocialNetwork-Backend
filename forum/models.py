from django.db import models
from django.conf import settings
from phone_field import PhoneField

# Create your models here.
def upload_article_image(instance , filename):
    return "forum/article/{user}/{filename}/".format(user=instance.user , filename=filename)
def upload_comment_image(instance , filename):
    return "forum/comment/{user}/{filename}/".format(user=instance.user , filename=filename)

class ArticleQuerySet(models.QuerySet):
    pass 

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model , using=self._db)

class CommentQuerySet(models.QuerySet):
    pass 

class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model , using=self._db)

# class TagQuerySet(models.QuerySet):
#     pass 

# class TagManager(models.Manager):
#     def get_queryset(self):
#         return TagQuerySet(self.model , using=self._db)


# class Tag(models.Model):
#     tag   =models.CharField(max_length = 50,blank=True, null=True)
#     searc_frequency = models.PositiveIntegerField(blank=True, null=True)
#     objects = TagManager()

#     # def __str__(self):
#     #     return str(self.about)[:50]

#     class Meta:
#         verbose_name = 'Tag post'
#         verbose_name_plural = 'Tag posts'

class Article(models.Model):
    user        =models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length = 150)
    discription = models.TextField(blank=True , null=True)
    image       =models.ImageField(upload_to=upload_article_image , blank=True , null=True)
    tags     =models.TextField(blank=True , null=True)
    favourites = models.PositiveIntegerField(blank=True , null=True)
    Updated_at = models.DateTimeField(auto_now=True)
    # def get_tags(self):
    #     return ",".join([str(p) for p in self.tags.all()])
    # objects = ArticleManager()

    # def __str__(self):
    #     return str(self.about)[:50]


    class Meta:
        verbose_name = 'Article post'
        verbose_name_plural = 'Article posts'

    @property
    def owner(self):
        return self.user


class Comment(models.Model):
    user        =models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, null=False)
    image       =models.ImageField(upload_to=upload_comment_image , blank=True , null=True)
    article        =models.ForeignKey(Article , on_delete=models.CASCADE, null=False)
    body   =models.TextField(blank=False, null=False)
    Updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    # def __str__(self):
    #     return str(self.about)[:50]

    class Meta:
        verbose_name = 'Comment post'
        verbose_name_plural = 'Comment posts'

    @property
    def owner(self):
        return self.user
    




    