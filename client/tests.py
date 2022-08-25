from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import User

class UserTest(APITestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(username="ifuituS", password="123456S", email="ifuituS@gmail.com", phone="+998909009090")
        User.objects.create_user(username="ifuitu", password="123456", email="ifuitu@gmail.com", phone="+998908196858")
        self.username="ifuitu"
        self.password="123456"
        self.email="ifuitu@gmail.com"
        self.confirm = "123456"
        self.phone = '+998908196858'
    
    def test_authentication(self):
        #Registration test
        response_reg = self.client.post(reverse('client:signup'),
                                    {"phone":"+998996555555", 'password':"123", 'confirm':"123", "first_name":"Test name"},
                                    format='json')
        self.assertEqual(response_reg.status_code, 200)

        #Confirmation test
        confirm_test = self.client.post(reverse('client:signup'),
                                    {"phone":"+998996555556", 'password':"123", 'confirm':"1", "first_name":"Test name"},
                                    format='json')
        self.assertEqual(confirm_test.status_code, 400)

        #Login test
        response_login = self.client.post(reverse("client:log"),
                                    {'phone': self.phone, 'password': self.password},
                                    format='json')
        self.assertEqual(response_login.status_code, 200)

        #token for header
        token = response_login.data["token"]  
        header = {"HTTP_AUTHORIZATION":"Token " + token}    #header for permission views

        #Change-password test
        response_change_pswrd = self.client.put(reverse("client:change-pswrd"), 
                                            {"password":self.password, 'new':"123", "confirm":"123"}, **header, format="json")
        self.assertEqual(response_change_pswrd.status_code, 200)

        #logout test
        response_logout = self.client.delete(reverse("client:log"), {}, **header, format="json")
        self.assertEqual(response_logout.status_code, 200)
    
    def test_user(self):
         #Login test
        response_login = self.client.post(reverse("client:log"),
                                    {'phone': self.phone, 'password': self.password},
                                    format='json')
        self.assertEqual(response_login.status_code, 200)

        #token for header
        token = response_login.data["token"]  
        header = {"HTTP_AUTHORIZATION":"Token " + token}    #header for permission views

        #user list test
        response_user_list = self.client.get(reverse('client-viewset-list'), format='json')
        self.assertEqual(response_user_list.status_code, 200)

        #user profile get test
        response_profile = self.client.get(reverse("client-viewset-detail", 
                                        args=(response_login.data['user']['id'],)), format='json')
        self.assertEqual(response_profile.status_code, 200)

        #user profile update
        response_update_profile = self.client.put(reverse("client-viewset-detail",
                                            kwargs={"pk":response_login.data['user']['id']}), 
                                            {"first_name":"John"}, 
                                            **header, format="json")
        self.assertEqual(response_update_profile.status_code, 200)

        #test if the user is not profile owner or is_staff return 403 permission denied!
        test_user_is_owner = self.client.delete(reverse("client-viewset-detail", 
                                            kwargs={"pk":'4'}), # here can be any user's id!
                                            **header, format='json')
        self.assertEqual(test_user_is_owner.data['detail'].code, "permission_denied")

        #user profile delete
        response_delete_user = self.client.delete(reverse("client-viewset-detail", 
                                            kwargs={"pk":response_login.data['user']['id']}),
                                            **header, format='json')
        self.assertEqual(response_delete_user.status_code, 204) #if it returns 204 (no content) that means user deleted!

        
        