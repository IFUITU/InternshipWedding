from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django.utils.translation import gettext as _
from django.contrib.auth import logout

from .serializers import RegisterSerializer, UserSerializer, ChangePswrdSerializer
from .models import User
from .permissions import IsProfileOwnerOrReadOnly


@api_view(["POST"])
# @permission_classes([~IsAuthenticated])
def signup(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        # serializer.validated_data['is_active'] = False
        user = serializer.save()
        # send_confirmation_email.delay(UserSerializer(user, many=False).data)
        return Response({"data":serializer.data, "message":_('None')}, status=status.HTTP_200_OK)
    return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class SignInOutView(APIView):

    def get_permissions(self):
        method = self.request.method
        if method == 'DELETE':
            return  [IsAuthenticated()]
        return []

    def post(self, request):
        user = authenticate(username=request.data.get("phone"), password=request.data.get("password"))
        if user is None:
            return Response({'error':_("User or password is not valid!")}, status=status.HTTP_400_BAD_REQUEST)
        token, create = Token.objects.get_or_create(user=user)
        return Response({"token":token.key, "user":{'phone':user.phone,'id':user.id}}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        if request.user.is_authenticated:
            if request.auth != None:
                request.auth.delete()
            else:
                logout(request)
            return Response({"data":"Come back soon!"}, status=status.HTTP_200_OK)
        return Response({"data":"Something wrong!"}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]
    filter_backends = [SearchFilter]
    # filterset_fields = ['id', 'is_blocked', 'phone', 'first_name']
    search_fields = ['id', 'is_blocked', 'phone', 'first_name']

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer


class ChangePswrdView(APIView):
    permission_classes = [IsProfileOwnerOrReadOnly]

    def put(self, request):
        try:
            user_obj = request.user
        except:
            return Response({"error":"User not Found!"})

        serialized = ChangePswrdSerializer(instance=request.user, data=request.data, context={"request":request})
        if serialized.is_valid():
            user_obj.set_password(serialized.validated_data.get('new'))
            user_obj.save()
            return Response({"data":serialized.data}, status=200)
        return Response({"data":serialized.errors}, status=400)