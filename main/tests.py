from io import BytesIO
from PIL import Image
from datetime import datetime

from rest_framework.test import APITestCase
from django.urls import reverse

from client.models import User
from .models import City, Event, EventPlace, Service, Order

class ApiTest(APITestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(username="ifuituS", password="1234567", email="ifuituS@gmail.com", phone="+998909009090")
        self.user = User.objects.create_user(username="ifuitu", password="123456", email="ifuitu@gmail.com", phone="+998908196858")
        self.password="123456"
        self.superuser_password='1234567'

    
    def header(self, user_phone, pswrd):
        response_login = self.client.post(reverse("client:log"),
                                    {'phone': user_phone, 'password': pswrd},
                                    format='json')
        token = response_login.data["token"]  
        header = {"HTTP_AUTHORIZATION":"Token " + token}#header for permission views
        return header

    @property
    def generate_photo_file(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
    
    def test_event(self):
        #test event list
        response_list = self.client.get(reverse("event-list"), format='json')
        self.assertEqual(response_list.status_code, 200)

        #if user is not staff can't create event
        response_create = self.client.post(reverse("event-list"), 
                                        {"name":"wedding", "image":self.generate_photo_file}, 
                                        **self.header(self.user.phone, self.password), foramt='multipart/form-data')
        self.assertEqual(response_create.data['detail'].code, 'permission_denied')

        #test create with staff user
        response_create_byStaff = self.client.post(reverse("event-list"), 
                                        {"name":"wedding", "image":self.generate_photo_file}, 
                                        **self.header(self.superuser.phone, self.superuser_password), foramt='multipart/form-data')
        self.assertEqual(response_create_byStaff.status_code , 201) #201 created!

        #test retrieve event
        event_ID = response_create_byStaff.data['id'] #we'll use this ID for put & delete too!
        response_retrive = self.client.get(reverse("event-detail", kwargs={'pk':event_ID}), format='json')
        self.assertEqual(response_retrive.status_code, 200)

        #test update event
        response_put_byStaff = self.client.put(reverse('event-detail', kwargs={"pk":event_ID}),
                                        {"name":"Wedding Part"}, 
                                        **self.header(self.superuser.phone, self.superuser_password), format='json')
        self.assertEqual(response_put_byStaff.status_code, 200)

        #test delete event by ordinary user
        response_delete = self.client.delete(reverse('event-detail', kwargs={'pk':event_ID}),
                                        **self.header(self.user.phone, self.password), format="json")
        self.assertEqual(response_delete.data['detail'].code, 'permission_denied')

        #test delete by staff user
        response_delete = self.client.delete(reverse('event-detail', kwargs={'pk':event_ID}),
                                        **self.header(self.superuser.phone, self.superuser_password), format="json")
        self.assertEqual(response_delete.status_code, 204) #204(no content) when deleted
    
    def test_eventPlace(self):
        event = Event.objects.create(name='wedding')
        city = City.objects.create(name="Tashkent")
    
        #test eventPlace list
        response_list = self.client.get(reverse("event-place-list"), format='json')
        self.assertEqual(response_list.status_code, 200)

        #if user is not staff can't create event
        response_create = self.client.post(reverse("event-place-list"), 
                                        {"name":"Restaurant", "image":self.generate_photo_file}, 
                                        **self.header(self.user.phone, self.password), foramt='multipart/form-data')
        self.assertEqual(response_create.data['detail'].code, 'permission_denied')

        #test create by staff user
        response_create_byStaff = self.client.post(reverse("event-place-list"), 
                                        {"name":"Restaurant","address":"Street 5/100", 
                                        "image":self.generate_photo_file,'event':[event.id], 'city':city.id}, 
                                        **self.header(self.superuser.phone, self.superuser_password),
                                         foramt='multipart/form-data')
        self.assertEqual(response_create_byStaff.status_code , 201) #201 created!

        #test retrieve eventPlace
        eventPlace_ID = response_create_byStaff.data['id'] #we'll use this ID for put & delete too!
        response_retrive = self.client.get(reverse("event-place-detail", kwargs={'pk':eventPlace_ID}), format='json')
        self.assertEqual(response_retrive.status_code, 200)

        #test update eventPlace
        response_put_byStaff = self.client.put(reverse('event-place-detail', kwargs={"pk":eventPlace_ID}),
                                        {"name":"Grand Hotel","event":[event.id]}, 
                                        **self.header(self.superuser.phone, self.superuser_password), format='json')
        self.assertEqual(response_put_byStaff.status_code, 200)

        #test delete eventPlace by ordinary user
        response_delete = self.client.delete(reverse('event-place-detail', kwargs={'pk':eventPlace_ID}),
                                        **self.header(self.user.phone, self.password), format="json")
        self.assertEqual(response_delete.data['detail'].code, 'permission_denied')

        #test delete by staff user
        response_delete = self.client.delete(reverse('event-place-detail', kwargs={'pk':eventPlace_ID}),
                                        **self.header(self.superuser.phone, self.superuser_password), format="json")
        self.assertEqual(response_delete.status_code, 204) #204(no content) when deleted
    
    def test_service(self):
        event = Event.objects.create(name='wedding')
    
        #test service list
        response_list = self.client.get(reverse("service-list"), format='json')
        self.assertEqual(response_list.status_code, 200)

        #if user is not staff can't create event
        response_create = self.client.post(reverse("service-list"), 
                                        {"name":"Any service",'event':[event.id], "image":self.generate_photo_file, "price":"10000"}, 
                                        **self.header(self.user.phone, self.password), foramt='multipart/form-data')
        self.assertEqual(response_create.data['detail'].code, 'permission_denied')

        #test create by staff user
        response_create_byStaff = self.client.post(reverse("service-list"), 
                                        {"name":"Any service name",
                                        "price":"10000", 
                                        "desc":"about service",
                                        "image":self.generate_photo_file, 
                                        'event':[event.id]}, 
                                        **self.header(self.superuser.phone, self.superuser_password),
                                         foramt='multipart/form-data')
        self.assertEqual(response_create_byStaff.status_code , 201) #201 created!

        #test retrieve service
        service_ID = response_create_byStaff.data['id'] #we'll use this ID for put & delete too!
        response_retrive = self.client.get(reverse("service-detail", kwargs={'pk':service_ID}), format='json')
        self.assertEqual(response_retrive.status_code, 200)

        #test update service
        response_put_byStaff = self.client.put(reverse('service-detail', kwargs={"pk":service_ID}),
                                        {"name":"Any service name PUT",
                                        "price":"10000", 
                                        "desc":"about service",
                                        "image":self.generate_photo_file, 
                                        'event':[event.id]}, 
                                        **self.header(self.superuser.phone, self.superuser_password), format='multipart')
        self.assertEqual(response_put_byStaff.status_code, 200)

        #test delete service by ordinary user
        response_delete = self.client.delete(reverse('service-detail', kwargs={'pk':service_ID}),
                                        **self.header(self.user.phone, self.password), format="json")
        self.assertEqual(response_delete.data['detail'].code, 'permission_denied')

        #test delete by staff user
        response_delete = self.client.delete(reverse('service-detail', kwargs={'pk':service_ID}),
                                        **self.header(self.superuser.phone, self.superuser_password), format="json")
        self.assertEqual(response_delete.status_code, 204) #204(no content) when deleted
    
    def test_order(self):
        #this models created as test  to create new order object
        event = Event.objects.create(name='wedding')
        event_place = EventPlace.objects.create(name="Cafe")
        service = Service.objects.create(name="Service name",  
                                desc="some desc", 
                                price="80000")
        location_wedding = City.objects.create(name="Tashkent")

        #test service list
        response_list = self.client.get(reverse("order-list"), format='json')
        self.assertEqual(response_list.status_code, 200)

        #test create by Staff
        response_create_byStaff = self.client.post(reverse("order-list"), 
                                {"author":self.superuser.id, 
                                "event":event.id,
                                "event_place":event_place.id,
                                "services":[service.id],
                                "total_price":"8000000",
                                "date_wedding":datetime.now().date(),
                                "location_wedding":location_wedding.id
                                }, **self.header(self.superuser.phone, self.superuser_password), format="json")

        self.assertEqual(response_create_byStaff.status_code, 201) #201 (created)

        #test retrieve
        order_ID = response_create_byStaff.data['id']
        response_retrieve = self.client.get(reverse("order-detail", kwargs={"pk":order_ID}))
        self.assertEqual(response_retrieve.status_code , 200)

        #test put by staff user
        response_put_byStaff = self.client.put(reverse("order-detail", kwargs={"pk":order_ID}), 
                                {
                                "services":[service.id],
                                "total_price":"8000000",
                                "date_wedding":datetime.now().date(),
                                }, **self.header(self.superuser.phone, self.superuser_password), format="json")
        self.assertEqual(response_put_byStaff.status_code, 200)

        #test delete by staff user
        response_delete = self.client.delete(reverse("order-detail", kwargs={"pk":order_ID}),
                                **self.header(self.superuser.phone, self.superuser_password), format="json")
        self.assertEqual(response_delete.status_code, 204)