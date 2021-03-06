from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import unittest
import time

MAX_WAIT = 10

class NewVisitorsTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    
    def tearDown(self):
        self.browser.quit()


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # User goes to checkout the homepage of the app.
        self.browser.get(self.live_server_url)

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

        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: Complete math homework' for row in rows),
        #     f"New to-do item did not appear in table. Contents were:\n{table.text}"
        # )
        # self.assertIn('1: Complete math homework', [row.text for row in rows])
        self.wait_for_row_in_list_table('1: Complete math homework')

        #There is still a text box inviting user to add another item
        #She enters "Complete history homework"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Complete history homework')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)

        self.wait_for_row_in_list_table('1: Complete math homework')
        self.wait_for_row_in_list_table('2: Complete history homework')

        #self.fail('Finish the test!')

        #The page updates again both items are in the list
        # User receives a link to visit the same web page
        # the to-do list is thus saved

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Edith start a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Complete math homework')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Complete math homework')

        #She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #Now a new user, Francis, comes along to the site.

        ##We use a new browser session to make sure that no information
        ##of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Francis visits the home page. there is no sign of Edith's
        #list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Complete math homework', page_text)
        self.assertNotIn('Complete history homework', page_text)

        #Francis starts a new list by entering a new item. He
        #is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #Francis gets his own unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #Again there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        #Satisfied, they both go to sleep.


    def test_layout_and_styling(self):
        #Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 786)

        #She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )

        #She starts a new list and sees the input is nicely
        #centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )


# if __name__ == '__main__':
#     unittest.main()