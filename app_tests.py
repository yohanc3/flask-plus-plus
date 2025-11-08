import os
import app as flaskr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_add_entry(self):
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            category='A category'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        assert b'A category' in rv.data

    def test_delete_entry(self):
        # First add an entry then delete it to ensure the state remains unchanged
        self.app.post('/add', data=dict(
            title='Test Entry',
            text='Test Text',
            category='Test Category'
        ), follow_redirects=True)

        rv = self.app.post('/delete', data=dict(
            id='1'
        ), follow_redirects=True)
        assert b'Entry deleted' in rv.data
        assert b'Test Entry' not in rv.data

    def test_update_entry(self):
        # First add an entry then update it
        self.app.post('/add', data=dict(
            title='Original Title',
            text='Original Text',
            category='Original Category'
        ), follow_redirects=True)

        rv = self.app.post('/update', data=dict(
            id='1',
            title='Updated Title',
            text='Updated Text',
            category='Updated Category'
        ), follow_redirects=True)
        assert b'Entry updated' in rv.data
        assert b'Updated Title' in rv.data
        assert b'Updated Text' in rv.data
        assert b'Updated Category' in rv.data
        assert b'Original Title' not in rv.data


if __name__ == '__main__':
    unittest.main()
