from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserInfo(User):
    phone = models.CharField(max_length=11)
    avatar = models.FileField(
        upload_to='/static/img/avatar/', default='/static/img/avatar/default.png')
    blog = models.OneToOneField(
        to='Blog', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Blog(models.Model):
    title = models.CharField(verbose_name='Blog Title', max_length=64)
    site_name = models.CharField(verbose_name='Site Name', max_length=64)
    theme = models.CharField(verbose_name='Blog Theme', max_length=64)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(verbose_name='Article Title', max_length=128)
    content = models.TextField(verbose_name='Article Content')
    date = models.DateTimeField(verbose_name='Create Time',)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    user = models.ForeignKey(verbose_name='Author',
                             to='UserInfo', to_field='id', on_delete=models.CASCADE)
    blog = models.ForeignKey(
        to='Blog', to_field='id', on_delete=models.CASCADE)
    category = models.ForeignKey(
        to='Categorys', to_field='id', on_delete=models.CASCADE)
    tag = models.ManyToManyField(to='Tag', through='Article2Tag')

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(verbose_name='Content')
    data = models.DateTimeField(verbose_name='Time', auto_now_add=True)
    article = models.ForeignKey(verbose_name='For Article',
                                to='Articles', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='Contenter',
                             to='UserInfo', to_field='id', on_delete=models.CASCADE)
    pid = models.ForeignKey(to='Comments', to_field='id',
                            null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Category(models.Model):
    name = models.CharField(verbose_name='Cate Name', max_length=16)
    blog = models.ForeignKey(verbose_name='For Blog',
                             to='Blog', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag Name', max_length=16)
    blog = models.ForeignKey(verbose_name='For Blog',
                             to='Blog', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Article2Tag(models.Model):
    article = models.ForeignKey(
        verbose_name='Article', to='Articles', to_field='id', on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='Tag', to='Tags',
                            to_field='id', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('article', 'tag')]

    def __str__(self):
        return self.article.name + ' & ' + self.tag.name


class ArticleUpDown(models.Model):
    article = models.ForeignKey(
        to='Articles', to_field='id', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        to='UserInfo', to_field='id', null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [('article', 'user')]

    def __str__(self):
        return self.article.title
