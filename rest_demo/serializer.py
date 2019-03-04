from rest_framework import serializers
from rest_demo.models import Book, Author, Publish


class BookSerializers_(serializers.Serializer):
    title = serializers.CharField(max_length=32)
    price = serializers.IntegerField()
    pub_date = serializers.DateField()
    publish_name = serializers.CharField(max_length=32, read_only=True, source="publish.name")  # 外键字段, 显示__str__方法的返回值
    publish_email = serializers.CharField(max_length=32, read_only=True, source="publish.email")  # 外键字段, 显示__str__方法的返回值
    authors = serializers.SerializerMethodField()  # 多对多字段需要自己手动获取数据，SerializerMethodField()

    def get_authors(self, book_obj):  # 'get_'固定格式,后面要与上面变量一直,这里指的是authors
        author_list = []
        for author in book_obj.authors.all():
            author_list.append(author.name)
        return author_list


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    publish = serializers.CharField(source="publish.pk")

    # 序列化超链接字段
    # publish = serializers.HyperlinkedIdentityField(
    #     view_name="detailpublish",
    #     lookup_field="publish_id",
    #     lookup_url_kwarg="pk",
    #
    # )

    # authors = serializers.SerializerMethodField(source="authors.all")
    # authors = serializers.SerializerMethodField()
    #
    # def get_authors(self, obj):
    #     name_list = []
    #     for obj in obj.authors.all():
    #         name_list.append(obj.name)
    #     return name_list

    def create(self, validated_data):
        book = Book.objects.create(title=validated_data["title"], price=validated_data["price"],
                                   pub_date=validated_data["pub_date"], publish_id=validated_data["publish"]["pk"])
        book.authors.add(*validated_data["authors"])
        return book

    def update(self, instance, validated_data):
        title = validated_data['title']
        price = validated_data['price']
        pub_date = validated_data["pub_date"]
        publish_id = validated_data["publish"]["pk"]
        instance.title = title
        instance.price = price
        instance.pub_date = pub_date
        instance.publish_id = publish_id
        instance.authors = validated_data["authors"]
        instance.save()
        return instance


class AuthorSerializers(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"


class PublishSerializers(serializers.ModelSerializer):

    class Meta:
        model = Publish
        fields = "__all__"
