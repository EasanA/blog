import os
import unittest
import multiprocessing
import time
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user1 = User(name="Alice", email="alice@example.com",
                         password=generate_password_hash("test"))
        session.add(self.user1)
        session.commit()
        
        # Create an second user
        self.user2 = User(name="Alice2", email="alice2@example.com",
                         password=generate_password_hash("test"))
        session.add(self.user2)
        session.commit()
        
        # Create an entry 
        #self.entry = Entry(title = "Test Entry", content = "Test content", author = self.user1)
        #session.add(self.entry)
        #session.commit()
        
        self.process = multiprocessing.Process(target=app.run,
                                               kwargs={"port": 8080})
        self.process.start()
        time.sleep(1)


    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()

    def test_login_correct(self):
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")

    def test_login_incorrect(self):
        self.browser.visit("http://127.0.0.1:8080/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:8080/login")
        
    def test_restricted_access(self):
        self.browser.visit("http://127.0.0.1:8080/entry/add")
        #self.assertEqual(self.browser.url, "http://127.0.0.1:8080/login")
        self.assertTrue(self.browser.url.startswith("http://127.0.0.1:8080/login"))
        
    #def test_restricted_author(self):
        #self.browser.visit("http://127.0.0.1:8080/login")
        #self.browser.fill("email", "alice2@example.com")
        #self.browser.fill("password", "test")
        #button = self.browser.find_by_css("button[type=submit]")
        #button.click()
        #self.browser.visit("http://127.0.0.1:8080/entry/add")
        #self.browser.fill("title", "test entry")
        #button = self.browser.find_by_css("button[type=submit]")
        #button.click()
        #self.browser.visit("http://127.0.0.1:8080")
        #print(session.query(Entry).all())
        #links_found = self.browser.find_link_by_href('http://127.0.0.1:8080/entry/0/edit')
        #print(links_found)
        #links_found.click()
        #self.assertEqual(self.browser.url, "http://127.0.0.1:8080/")
        
if __name__ == "__main__":
    unittest.main()