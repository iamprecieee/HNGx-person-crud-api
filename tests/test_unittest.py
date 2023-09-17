import unittest, json
from app import create_app
from resources.db import db


class TestApp(unittest.TestCase):
    def setUp(self):
        app = create_app("sqlite:///test_data.db")
        self.app = app.test_client() # Create a test client
        with app.app_context():
            db.create_all()
            
    def tearDown(self):
        app = create_app("sqlite:///test_data.db")
        with app.app_context():
            db.drop_all()
            
            
    def test_create_person_success(self):
        """ Successfully creating person """
        result = self.app.post("/api", json={"name": "John Doe"})
        assert result.status_code == 200
        assert json.loads(result.data.decode("utf-8")) == "Person created successfully."
        
        
    def test_create_person_failure(self):
        """ Trying to create person with an invalid 'name' """
        result = self.app.post("/api", json={"name": 2})
        assert result.status_code == 422
        assert json.loads(result.data.decode("utf-8"))["description"] == "Name must be a valid string!"
        
    def test_create_person_failure2(self):
        """ Trying to create duplicate persons """
        self.app.post("/api", json={"name": "Jane Smith"})
        result = self.app.post("/api", json={"name": "Jane Smith"})
        assert result.status_code == 400
        assert json.loads(result.data.decode("utf-8"))["description"] == "A person with that name already exists!"
        
    def test_retrieve_person_success(self):
        """ Successfully retrieving list of existing persons """
        result = self.app.get("/api")
        assert result.status_code == 200
        assert json.loads(result.data.decode("utf-8")) == []
        
    def test_retrieve_person_by_id_success(self):
        """ Successfully retrieving existing person by id """
        self.app.post("/api", json={"name": "John Doe"})
        result = self.app.get("/api/1")
        assert result.status_code == 200
        assert json.loads(result.data.decode("utf-8")) == {"id": 1, "name": "John Doe"}
        
    def test_retrieve_person_by_name_success(self):
        """ Successfully retrieving existing person by name """
        self.app.post("/api", json={"name": "John Doe"})
        result = self.app.get("/api/John%20Doe")
        assert result.status_code == 200
        assert json.loads(result.data.decode("utf-8")) == {"id": 1, "name": "John Doe"}
        
    def test_retrieve_person_by_id_failure(self):
        """ Failing to retrieve existing person by id """
        result = self.app.get("/api/1")
        assert result.status_code == 404
        assert json.loads(result.data.decode("utf-8"))["description"] == "Person with this id/name could not be located."
        
    def test_retrieve_person_by_name_failure(self):
        """ Failing to retrieve existing person by name """
        result = self.app.get("/api/John%20Doe")
        assert result.status_code == 404
        assert json.loads(result.data.decode("utf-8"))["description"] == "Person with this id/name could not be located."
        
    def test_update_person_by_id_success(self):
        """ Successfully updating exissting person by id """
        self.app.post("/api", json={"name": "John Doe"})
        result = self.app.put("/api/1", json={"name": "Jane Doe"})
        assert result.status_code == 200
        assert json.loads(result.data.decode("utf-8")) == {"id": 1, "name": "Jane Doe"}
        
    def test_update_person_by_name_success(self):
        """ Successfully updating existing person by name """
        self.app.post("/api", json={"name": "John Doe"})
        result = self.app.put("/api/John%20Doe", json={"name": "Jane Doe"})
        assert result.status_code == 200
        assert json.loads(result.data.decode("utf-8")) == {"id": 1, "name": "Jane Doe"}
        
    def test_update_person_by_id_failure(self):
        """ Failing to update existing person by id using duplicate name """
        self.app.post("/api", json={"name": "John Doe"})
        self.app.post("/api", json={"name": "Jane Smith"})
        result = self.app.put("/api/1", json={"name": "Jane Smith"})
        assert result.status_code == 400
        assert json.loads(result.data.decode("utf-8"))["description"] == "A person with that name already exists!"
        
    def test_update_person_by_name_failure(self):
        """ Failing to update existing person by name using duplicate name """
        self.app.post("/api", json={"name": "John Doe"})
        self.app.post("/api", json={"name": "Jane Smith"})
        result = self.app.put("/api/John%20Doe", json={"name": "Jane Smith"})
        assert result.status_code == 400
        assert json.loads(result.data.decode("utf-8"))["description"] == "A person with that name already exists!"
        
    def test_update_person_by_id_failure2(self):
        """ Failing to update non-existing person by id """
        result = self.app.put("/api/1", json={"name": "Jane Smith"})
        assert result.status_code == 404
        assert json.loads(result.data.decode("utf-8"))["description"] == "Person with this id/name could not be located."
        
    def test_update_person_by_name_failure2(self):
        """ Failing to update non-existing person by name """
        result = self.app.put("/api/Jane%20Doe", json={"name": "Jane Smith"})
        assert result.status_code == 404
        assert json.loads(result.data.decode("utf-8"))["description"] == "Person with this id/name could not be located."
        
    def test_delete_person_by_id_success(self):
        """ Successfully deleting existing person by id """
        self.app.post("/api", json={"name": "John Doe"})
        result = self.app.delete("/api/1", json={"name": "John Doe"})
        assert result.status_code == 204
        assert not result.data
        
    def test_delete_person_by_name_success(self):
        """ Successfully deleting existing person by name """
        self.app.post("/api", json={"name": "John Doe"})
        result = self.app.delete("/api/John%20Doe", json={"name": "John Doe"})
        assert result.status_code == 204
        assert not result.data
        
    def test_delete_person_by_id_failure(self):
        """ Failing to delete non-existing person by id """
        result = self.app.put("/api/1", json={"name": "Jane Smith"})
        assert result.status_code == 404
        assert json.loads(result.data.decode("utf-8"))["description"] == "Person with this id/name could not be located."
        
    def test_delete_person_by_name_failure(self):
        """ Failing to delete non-existing person by name """
        result = self.app.put("/api/Jane%20Smith", json={"name": "Jane Smith"})
        assert result.status_code == 404
        assert json.loads(result.data.decode("utf-8"))["description"] == "Person with this id/name could not be located."
            
            

if __name__ == "__main__":
    unittest.main()