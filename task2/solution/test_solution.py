import unittest
from unittest.mock import patch, MagicMock

from solution import has_cyrillic, return_verified_animal_titles, get_animals_wiki_letters_stats


class TestWikiFunctions(unittest.TestCase):
    def test_has_cyrillic_true(self):
        self.assertTrue(has_cyrillic("Животные"))

    def test_has_cyrillic_false(self):
        self.assertFalse(has_cyrillic("Animals"))

    def test_return_verified_animal_titles(self):
        animals = [
            {'title': 'Слон'},
            {'title': 'Rhizostoma pulmo'},
            {'title': 'Жираф'},
            {'title': 'Giraffe'}
        ]
        result, should_stop = return_verified_animal_titles(animals)
        self.assertEqual(result, ['Слон', 'Жираф'])
        self.assertTrue(should_stop)

    @patch('httpx.get')
    def test_get_animals_wiki_letters_stats(self, mock_get):
        fake_link_1 = MagicMock()
        fake_link_1.__getitem__.return_value = 'Слон'
        fake_link_1.get = lambda attr: 'Слон'
        fake_link_1['title'] = 'Слон'
        fake_link_2 = MagicMock()
        fake_link_2.__getitem__.return_value = 'Жираф'
        fake_link_2.get = lambda attr: 'Жираф'
        fake_link_2['title'] = 'Жираф'
        animal_group = MagicMock()
        animal_group.select.return_value = [fake_link_1, fake_link_2]
        mock_soup = MagicMock()
        mock_soup.select.return_value = [None, None, animal_group]
        mock_soup.find.return_value = None
        result = get_animals_wiki_letters_stats(mock_soup)
        self.assertEqual(result['С'], 1)
        self.assertEqual(result['Ж'], 1)


if __name__ == '__main__':
    unittest.main()
