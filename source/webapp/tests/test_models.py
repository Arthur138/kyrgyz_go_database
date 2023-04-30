from django.test import TestCase
import accounts.models
from accounts.models import User
from django.core.exceptions import ValidationError
from webapp.models import Recommendation, Player, Country, Region, City
import time


class RecommendationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.player = Player.objects.create(first_name='Test player', country=Country.objects.create(country_code='kg'))
        cls.recommendation = Recommendation.objects.create(text='Test recommendation', author=cls.user,
                                                           player=cls.player)

    def test_str_method(self):
        expected_method = f'{self.recommendation.pk}. Test recommendation'
        self.assertEqual(str(self.recommendation), expected_method)

    def test_text_max_length(self):
        max_length = Recommendation._meta.get_field('text').max_length
        self.assertEqual(max_length, 400)

    def test_author_foreign_key(self):
        author_field = Recommendation._meta.get_field('author')
        self.assertEqual(author_field.related_model, accounts.models.User)

    def test_player_foreign_key(self):
        player_field = Recommendation._meta.get_field('player')
        self.assertEqual(player_field.related_model, Player)

    def test_created_at_auto_now_add(self):
        created_at_field = Recommendation._meta.get_field('created_at')
        self.assertTrue(created_at_field.auto_now_add)

    def test_updated_at_auto_now(self):
        updated_at_field = Recommendation._meta.get_field('updated_at')
        self.assertTrue(updated_at_field.auto_now)

    def test_object_creation(self):
        self.assertEqual(self.recommendation.text, 'Test recommendation')
        self.assertEqual(self.recommendation.author, self.user)
        self.assertEqual(self.recommendation.player, self.player)
        self.assertIsNotNone(self.recommendation.created_at)
        self.assertIsNotNone(self.recommendation.updated_at)

    def test_object_update(self):
        self.recommendation.text = 'Updated recommendation'
        self.recommendation.save()
        updated_recommendation = Recommendation.objects.get(pk=self.recommendation.pk)
        self.assertEqual(updated_recommendation.text, 'Updated recommendation')
        self.assertGreater(updated_recommendation.updated_at, self.recommendation.created_at)

    def test_player_deletion(self):
        self.player.delete()
        self.assertFalse(Recommendation.objects.filter(pk=self.recommendation.pk).exists())

    def test_author_default_value(self):
        recommendation = Recommendation.objects.create(
            text='Test recommendation',
            player=self.player
        )
        self.assertEqual(recommendation.author_id, 1)

    def test_related_name_parameter(self):
        self.assertIn(self.recommendation, self.user.author.all())
        self.assertIn(self.recommendation, self.player.player.all())


class CountryModelTest(TestCase):
    def test_create_country_with_right_country_code(self):
        country = Country.objects.create(country_code='kg')
        self.assertIsInstance(country, Country)
        self.assertEqual(len(Country.objects.all()), 1)
        self.assertEqual(str(country), 'kg')

    def test_create_country_with_wrong_parameters(self):
        with self.assertRaises(Exception):
            Country.objects.create(country_code='kgz')

    def test_update_country(self):
        country = Country.objects.create(country_code='us')
        self.assertEqual(len(Country.objects.all()), 1)

        country.country_code = 'ca'
        country.save()
        updated_country = Country.objects.get(pk=country.pk)
        self.assertEqual(updated_country.country_code, 'ca')

    def test_delete_country(self):
        country = Country.objects.create(country_code='kg')
        self.assertEqual(len(Country.objects.all()), 1)

        country.delete()
        self.assertEqual(len(Country.objects.all()), 0)


class CityModelTest(TestCase):
    def test_create_city_with_correct_parameters(self):
        country = Country.objects.create(country_code='kg')
        region = Region.objects.create(name='Chuy', country=country)
        city = City.objects.create(city='Bishkek', country=country, region=region)
        self.assertIsInstance(city, City)
        self.assertEqual(len(City.objects.all()), 1)
        self.assertEqual(str(city), 'Bishkek')
        self.assertLessEqual(len(city.city), 50)

    def test_create_city_with_incorrect_parameters(self):
        country = Country.objects.create(country_code='kg')
        region = Region.objects.create(name='Chuy', country=country)
        city = City(city='', country=country, region=region)
        with self.assertRaises(ValidationError):
            city.full_clean()
            city.save()
        city = City(city='a' * 51, country=country, region=region)
        with self.assertRaises(ValidationError):
            city.full_clean()
            city.save()
        self.assertEqual(len(City.objects.all()), 0)

    def test_update_city(self):
        country = Country.objects.create(country_code='kg')
        region = Region.objects.create(name='Chuy', country=country)
        city = City.objects.create(city='Bishkek', country=country, region=region)
        city.city = 'Osh'
        city.save()
        updated_city = City.objects.get(id=city.id)
        self.assertEqual(updated_city.city, 'Osh')

    def test_delete_city(self):
        country = Country.objects.create(country_code='kg')
        region = Region.objects.create(name='Chuy', country=country)
        city = City.objects.create(city='Bishkek', country=country, region=region)
        self.assertEqual(len(City.objects.all()), 1)
        city.delete()
        self.assertEqual(len(City.objects.all()), 0)
