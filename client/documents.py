# from .models import User
# from django_elasticsearch_dsl import Document, fields
# from django_elasticsearch_dsl.registries import registry


# @registry.register_document
# class UserDocument(Document):
#     class Index:
#         name = 'users'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }
    
#     class Django:
#         model = User
#         fields = ['id', 'phone', 'first_name']
