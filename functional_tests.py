from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import time


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

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrive_it_later(self):
        # User goes to checkout the homepage of the app.
        self.browser.get(r'http://localhost:8000')

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        

        #User is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User enters "Complete math homework"
        inputbox.send_keys('Complete math homework')
        #When user hits enter, page updates
        #There is an item in the to-do list now
        #1: Complete math homework
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: Complete math homework' for row in rows),
        #     f"New to-do item did not appear in table. Contents were:\n{table.text}"
        # )
        # self.assertIn('1: Complete math homework', [row.text for row in rows])
        self.check_for_row_in_list_table('1: Complete math homework')

        #There is still a text box inviting user to add another item
        #She enters "Complete history homework"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Complete history homework')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Complete math homework')
        self.check_for_row_in_list_table('2: Complete history homework')

        self.fail('Finish the test!')

        #The page updates again both items are in the list
        # User receives a link to visit the same web page
        # the to-do list is thus saved

if __name__ == '__main__':
    unittest.main()