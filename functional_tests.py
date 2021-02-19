from selenium import webdriver
import unittest

# browser = webdriver.Firefox()

# # Edith has heard about a cool new online to-do app. She goes
# # to check out its homepage
# browser.get(r'http://localhost:8000')

# # She notices the page title and header mention to-do lists
# assert 'To-Do' in browser.title

# # She is invited to enter a to-do item strainght away

# # She types "Buy peacock feathers" into a text box (Edith's hobby
# # is tying fly-fishing lures)

# # When she hits enter, the page updates, and now the page lists
# # "1: Buy peacock feathers" as an item in a to-do list

# # There is still a text box inviting her to add another item. She
# # enters "Use peacock feathers to make a fly" (Edith is very methodical)

# # The page updates again, and now shows both items on her list

# # Edith wonders whether the site will remember her list. Then she sees
# # that the site has generated a unique URL for her -- there is some
# # explanatory text to that effect.

# # She visits that URL - her to-do list is still there.

# # Satisfied, she goes back to sleep.

# browser.quit()

class NewVisitorsTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        # User goes to checkout the homepage of the app.
        self.browser.get(r'http://localhost:8000')

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # User is invited to enter a to-do item straight away
        # User enters "Complete math homework"
        # Web page displays:-
        # "1: Complete math homework"
        # User receives a link to visit the same web page
        # the to-do list is thus saved

if __name__ == '__main__':
    unittest.main()