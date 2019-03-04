from haystack import indexes
from user.models import Goods


class GoodsIndex(indexes.SearchIndex, indexes.Indexable):
    """
    创建索引类
    """

    text = indexes.CharField(document=True, use_template=True)  # text索引字段，use_template=True根据表中的字段建立索引文件
    # author = indexes.CharField(model_attr='user')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        # 返回模型类
        return Goods

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.all()

# 万事俱备后在虚拟环境输入命令：python manage.py rebuild_index，会自动生成索引文件whoosh_index
