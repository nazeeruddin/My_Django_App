from django.test import TestCase

# Create your tests here.

from catalog.models import Author
from django.urls import reverse

class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create 13 authors for pagination tests
        number_of_authors = 13
        for author_num in range(number_of_authors):
            Author.objects.create(first_name='Christian %s' % author_num, last_name = 'Surname %s' % author_num,)
           
    def test_view_url_exists_at_desired_location(self): 
        resp = self.client.get('/catalog/authors/') 
        self.assertEqual(resp.status_code, 200)  
           
    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)
        
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'catalog/author_list.html')
        
    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('authors'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['author_list']) == 10)

    def test_lists_all_authors(self):
        #Get second page and confirm it has (exactly) remaining 3 items
        resp = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['author_list']) == 3)
		
from django.contrib.auth.models import Permission # Required to grant the permission needed to set a book as returned.

class RenewBookInstancesViewTest(TestCase):

    def setUp(self):
        #Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        #Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(title='Book Title', summary = 'My book summary', isbn='ABCDEFG', author=test_author, language=test_language,)
        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

        #Create a BookInstance object for test_user1
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1=BookInstance.objects.create(book=test_book,imprint='Unlikely Imprint, 2016', due_back=return_date, borrower=test_user1, status='o')

        #Create a BookInstance object for test_user2
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2=BookInstance.objects.create(book=test_book,imprint='Unlikely Imprint, 2016', due_back=return_date, borrower=test_user2, status='o')