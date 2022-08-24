from .models import Order
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class OrderDocument(Document):
    author = fields.ObjectField(properties={
        'id':fields.IntegerField(),
        'first_name':fields.TextField(),
        'phone':fields.TextField()
    })

    class Index:
        name = 'orders'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
    
    class Django:
        model = Order
        fields = ['id', 'date_wedding']
