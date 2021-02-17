from selenium import webdriver

browser = webdriver.Firefox()
browser.get(r'http://localhost:8000')

assert 'Django' in browser.title