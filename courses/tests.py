from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com')
        self.user.set_password('test')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Test course',
            description='Test course description',
            owner_id=self.user.id
        )

        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test lesson description',
            video_url='http://www.youtube.com/watch&123',
            course=self.course,
            owner_id=self.user.id
        )

    def test_create_lesson(self):
        """Lesson creation testing"""

        data = {
            'title': 'Lesson creation',
            'description': 'Lesson creation description',
            'video_url': 'http://youtu.be/watch&456',
            'course': self.lesson.course
        }

        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id + 1,
                'title': 'Lesson creation',
                'description': 'Lesson creation description',
                'preview': None,
                'video_url': 'http://youtu.be/watch&456',
                'course': 'Test course', 'owner': self.lesson.owner.id
            }
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_list_lesson(self):
        """List lessons testing"""

        response = self.client.get(
            '/lesson/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [{
                'id': self.lesson.id,
                'course': 'Test course',
                'title': 'Test lesson',
                'preview': None,
                'description': 'Test lesson description',
                'video_url': 'http://www.youtube.com/watch&123',
                'owner': self.lesson.owner.id
            }]
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            1
        )

    def test_retrieve_lesson(self):
        """Retrieve lesson testing"""

        response = self.client.get(
            f'/lesson/{self.lesson.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'course': 'Test course',
                'title': 'Test lesson',
                'preview': None,
                'description': 'Test lesson description',
                'video_url': 'http://www.youtube.com/watch&123',
                'owner': self.lesson.owner.id
            }
        )

    def test_update_lesson(self):
        """Update lesson testing"""

        data = {
            'title': 'Test updated lesson',
        }

        response = self.client.patch(
            f'/lesson/update/{self.lesson.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['title'],
            'Test updated lesson'
        )

    def test_destroy_lesson(self):
        """Delete lesson testing"""

        response = self.client.delete(
            f'/lesson/delete/{self.lesson.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com')
        self.user.set_password('test')
        self.user.save()

        # Использую второй способ авторизации на тестовой БД через токен
        # Первый был при тестировании CRUD уроков:
        # self.client.force_authenticate(user=self.user)
        response = self.client.post('/users/token/', {'email': 'user@test.com', 'password': 'test'})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course.objects.create(
            title='Test course',
            description='Test course description',
            owner_id=self.user.id
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

    def test_create_subscription(self):
        """Subscription creation testing"""

        response = self.client.post(
            f'/subscribe/{self.course.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            ['You have subscribed for the course']
        )

        self.assertEqual(
            Subscription.objects.get(id=self.subscription.id + 1).user.email,
            'user@test.com'
        )

        self.assertEqual(
            Subscription.objects.get(id=self.subscription.id + 1).course.title,
            'Test course'
        )

    def test_delete_subscription(self):
        """Subscription deleting testing"""

        response = self.client.delete(
            f'/unsubscribe/{self.course.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        with self.assertRaises(ObjectDoesNotExist):
            Subscription.objects.get(id=self.subscription.id + 1)
