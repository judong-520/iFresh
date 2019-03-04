from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    type_choices = ((1, "普通用户"), (2, "VIP"), (3, "SVIP"))
    user_type = models.IntegerField(choices=type_choices, default=1)

    class Meta:
        db_table = "demo_user"


class Token(models.Model):
    user = models.OneToOneField("User")
    token = models.CharField(max_length=128)

    def __str__(self):
        return self.token

    class Meta:
        db_table = 'demo_token'


class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.IntegerField()
    pub_date = models.DateField()
    publish = models.ForeignKey(to="Publish", related_name="book", related_query_name="book_query",
                                on_delete=models.CASCADE)
    authors = models.ManyToManyField(to="Author")  # 多对多字段

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'demo_book'


class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'demo_publish'


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'demo_author'

