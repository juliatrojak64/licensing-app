import unittest
from app import app, study_materials

class CMSTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_file_upload(self):
        # Test uploading a valid file
        with open('testfile.pdf', 'wb') as f:
            f.write(b"%PDF-1.4 test PDF content")
        with open('testfile.pdf', 'rb') as f:
            data = {
                'file': (f, 'testfile.pdf'),
                'title': 'Test File',
                'description': 'A test file for unit testing',
                'category': 'Documents'
            }
            response = self.app.post('/api/materials', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 201)
            self.assertIn('Material uploaded successfully', response.json['message'])

    def test_metadata_validation(self):
        # Test missing title
        data = {
            'file': None,
            'title': '',
            'description': 'Missing title test',
            'category': 'Test'
        }
        response = self.app.post('/api/materials', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Title is required.', response.json['errors'])

    def test_review_approval(self):
        # Add a mock material
        material = {
            'id': 1,
            'title': 'Pending Material',
            'description': 'A mock pending material',
            'category': 'Documents',
            'file_url': 'http://example.com/test.pdf',
            'status': 'pending_review'
        }
        study_materials.append(material)

        # Test approving the material
        response = self.app.patch('/api/materials/1/approve')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['material']['status'], 'approved')

    def test_categorization_and_navigation(self):
        # Add mock materials
        study_materials.extend([
            {
                'id': 2,
                'title': 'Category Test 1',
                'description': 'First category test',
                'category': 'Videos',
                'file_url': 'http://example.com/video1.mp4',
                'status': 'approved'
            },
            {
                'id': 3,
                'title': 'Category Test 2',
                'description': 'Second category test',
                'category': 'Documents',
                'file_url': 'http://example.com/doc1.pdf',
                'status': 'approved'
            }
        ])

        # Retrieve by category
        response = self.app.get('/api/materials/category/Documents')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['materials']), 1)
        self.assertEqual(response.json['materials'][0]['category'], 'Documents')

    def tearDown(self):
        # Clear the mock database
        study_materials.clear()

if __name__ == '__main__':
    unittest.main()
