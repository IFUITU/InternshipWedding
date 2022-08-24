import abc

from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError

from main.documents import OrderDocument
from main.serializers import OrderSerializer

from datetime import datetime

class PaginatedESKAPIView(APIView, LimitOffsetPagination):
    serializer_class =  None
    document_class = None

    @abc.abstractclassmethod
    def generate_q_expression(self, query):
        """ This method should be overriden 
            and return Q() expression """

    def get(self, request, query):
        try:
            q = self.generate_Q_expression(query)
            search = self.document_class.search().filter('range', date_wedding={'lte':query})
            response = search.execute()
            for i in search:
                print(i)
            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            raise ValidationError(e)


class OrderELKView(PaginatedESKAPIView):
    serializer_class = OrderSerializer
    document_class = OrderDocument

    def generate_Q_expression(self, query):
        print(type(datetime.strptime(query, "%d-%m-%Y").date()))
        return Q(
            'multi_match', query=query,
            fields=[
                'date_wedding',
            ], fuzziness='auto')


