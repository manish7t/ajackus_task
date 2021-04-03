from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File as DjangoFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .serializers import *
from .models import *


class RegistrationTest(APITestCase):

    def setUp(self):
        # create user
        self.user = AppUser.objects.create_user(username='user@user.com', email='user@user.com',
                                                phone=8421602297, pincode=413706)
        # set password
        self.user.set_password('Msdks7777')
        self.user.save()

        # validate response
        self.assertTrue(self.client.login(username='user@user.com', password='Msdks7777'))

    def test_register_user(self):
        # user data
        data = {'email': 'user@user.com', 'username': 'user@user.com', 'password': 'Msdks7777', 'phone': 8408839917,
                'pincode': 413706}

        # user register post request
        response = self.client.post(reverse('user-registration'), data=data, format='multipart')

        # get user
        user = AppUser.objects.get(email=data['email'])

        # validate data
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.phone, data['phone'])
        self.assertEqual(user.pincode, data['pincode'])

        # validate response
        self.assertEqual(response.status_code, 200)

        print("")
        print("Test : Register User : ", " Successfully Register User !!!")

    def test_login_user(self):
        # login credential
        data = {'username': 'user@user.com', 'password': 'Msdks7777'}

        # post request
        login_response = self.client.post(reverse('login'), data=data, format='multipart')
        # validate login request
        self.assertEqual(login_response.status_code, 200)

        print("")
        print("Test : Login User : ", " Successfully Logged In !!!")


class ContentTest(APITestCase):

    def setUp(self):
        # create user
        self.user = AppUser.objects.create_user(username='user@user.com', email='user@user.com', phone=8421602297,
                                                pincode=413706)

        # set password
        self.user.set_password('Msdks7777')
        self.user.save()

        self.assertTrue(self.client.login(username='user@user.com', password='Msdks7777'))

        # create content

        # Get pdf from local storage    
        pdf_object = DjangoFile(open('files/Backtracking.pdf', mode='rb'), name='PDF')
        # pdf name
        filename = 'tested.pdf'

        # file read
        uploaded_file = SimpleUploadedFile(filename, pdf_object.read(), content_type='multipart/form-data')

        self.content = Content.objects.create(title="Imagination",
                                              body="Don't forget that gifts often come with costs that go beyond "
                                                   "their purchase price", summary="Dont forget",
                                              document=uploaded_file, app_user=self.user, categories=['test'])

    # create content
    def test_create_content(self):
        # authenticate user
        self.assertTrue(self.client.login(username='user@user.com', password='Msdks7777'))

        # Get pdf from local storage    
        pdf_object = DjangoFile(open('files/Backtracking.pdf', mode='rb'), name='PDF')

        # PDF name    
        filename = 'tested.pdf'

        uploaded_file = SimpleUploadedFile(
            filename, pdf_object.read(), content_type='multipart/form-data')

        data = {"title": "Imagination",
                "body": "Don't forget that gifts often come with costs that go beyond their purchase price",
                "summary": "Dont forget", "document": uploaded_file, "app_user": self.user.id, 'categories': ['test']}

        # content post request   
        response = self.client.post(reverse('create-content'), data=data, format='multipart')

        response_data = response.data

        # validate data
        self.assertEqual(response_data['title'], data['title'])
        self.assertEqual(response_data['body'], data['body'])
        self.assertEqual(response_data['summary'], data['summary'])

        # validate response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("")
        print("Test: Create Content: ", " Successfully content created !!!")

    # get all content
    def test_get_all_content(self):
        # authenticate user
        self.assertTrue(self.client.login(username='user@user.com', password='Msdks7777'))

        # content get request
        response = self.client.get(reverse('GetAllContentAPI'))

        # validate response
        self.assertEqual(response.status_code, 200)

        print("")
        print("Test : Get All Content : ", " Successfully Get All Content !!!")

    # get individual content
    def test_get_single_content(self):
        # authenticate user
        self.assertTrue(self.client.login(username='user@user.com', password='Msdks7777'))

        # content get request
        response = self.client.get(reverse('retrieve-content', kwargs={'pk': self.content.id}))

        # get content
        content = Content.objects.get(id=self.content.id)

        # validate data
        data = response.data
        self.assertEqual(data['title'], content.title)
        self.assertEqual(data['summary'], content.summary)

        # validate response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print("")
        print("Test : Get Individual Content : ", " Successfully Get Individual Content !!!")

    # content update test
    def test_update_content(self):
        # authenticate user
        self.assertTrue(self.client.login(username='user@user.com', password='Msdks7777'))

        # Get pdf from local storage    
        pdf_object = DjangoFile(open('files/Backtracking.pdf', mode='rb'), name='PDF')

        # pdf file name 
        filename = 'tested.pdf'

        uploaded_file = SimpleUploadedFile(filename, pdf_object.read(), content_type='multipart/form-data')

        data = {"title": "test-update",
                "body": "Don't forget that gifts often come with costs that go beyond their purchase price",
                "summary": "update Dont forget"}

        # content put request
        response = self.client.put(reverse('update-content', kwargs={'pk': self.content.id}), data=data,
                                   format='multipart')

        # validate data
        response_data = response.data
        self.assertEqual(response_data['title'], data['title'])
        self.assertEqual(response_data['summary'], data['summary'])

        # validate response    
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print("")
        print("Test : Update Content : ", " Successfully Updated Content !!!")

    # content delete test
    def test_content_delete(self):
        # authenticate user
        self.assertTrue(self.client.login(username='user@user.com', password='Msdks7777'))

        # content delete request    
        response = self.client.delete(reverse('delete-content', kwargs={'pk': self.content.id}))
        # validate response
        self.assertEqual(response.status_code, 200)

        print("")
        print("Test : Delete Content : ", " Successfully Deleted Content !!!")
