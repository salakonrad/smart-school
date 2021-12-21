from django.test import TestCase, Client
from school.models import User


class TestViews(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'konradsala',
            'password': 'test12345'
        }
        User.objects.create_user(**self.credentials)

    def test_message_list_view(self):
        client = Client()
        client.login(username='konradsala', password='test12345')

        response = client.get("/message/list", follow=True)

        self.assertTemplateUsed(response, 'messages/messages_list.html')

    def test_attendance_list_view(self):
        client = Client()
        client.login(username='konradsala', password='test12345')

        response = client.get("/attendance", follow=True)

        self.assertTemplateUsed(response, 'attendance/class_list.html')

    def test_message_send(self):
        response = self.client.post("/message/send", {
            'sender': 1,
            'recipient': 2,
            'message': "test"
        })

        self.assertEquals(response.status_code, 302)

    # def test_messages_view(self):
    #     client = Client()
    #     client.login(username='konradsala', password='test12345')
    #
    #     response = client.get("/messages", follow=True)
    #
    #     self.assertTemplateUsed(response, 'messages/messages.html')
