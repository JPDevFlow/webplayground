from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

# Pruebas para el modelo Profile

class ProfileTestCase(TestCase):
    def setUp(self):
        # Crea un usuario de prueba antes de cada test
        User.objects.create_user('test', 'test@test.com', 'test1234')

    def test_profile_exists(self):
        # Verifica que el perfil se haya creado automáticamente para el usuario de prueba
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)


