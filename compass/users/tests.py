import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


@pytest.mark.django_db
def test_user_detail(client, django_user_model):
   user = django_user_model.objects.create(
       username='someone', password='password'
   )
   assert user
   url = reverse('partners:index')
   response = client.get(url)
   assert response.status_code == 200
   #assert 'someone' in response.content