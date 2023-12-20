from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.board = [['R', 'E', 'W', 'C', 'S'], ['A', 'C', 'T', 'F', 'I'], ['W', 'T', 'A', 'R', 'R'], ['I', 'S', 'A', 'P', 'D'], ['R', 'R', 'P', 'D', 'U']]

    def test_main_page_load(self):
         with app.test_client() as client:
            # perform a get request to the given path
            resp = client.get('/') 
            html = resp.get_data(as_text=True) 

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Boggle</h1>', html)
            self.assertIn('<table class="table table-borderless', html)

    def test_word_check_ok(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board

            resp = client.get('/check-word', query_string={"word-guess": "tarp"})
            payload = resp.get_data(as_text=True) 
                              
            self.assertEqual(resp.status_code, 200)
            self.assertIn('"result": "ok"', payload)   

    def test_word_check_not_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board

            resp = client.get('/check-word', query_string={"word-guess": "adobe"})
            payload = resp.get_data(as_text=True) 
                              
            self.assertEqual(resp.status_code, 200)
            self.assertIn('"result": "not-on-board"', payload)        

    def test_word_check_not_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board

            resp = client.get('/check-word', query_string={"word-guess": "qwerty"})
            payload = resp.get_data(as_text=True) 
                              
            self.assertEqual(resp.status_code, 200)
            self.assertIn('"result": "not-word"', payload)       

    def test_update_stats_no_history(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board

            resp = client.post('/update-stats', json={"score": 10}, content_type='application/json')
            payload = resp.json

            print(f"payload: {payload}")
            print(f"resp: {resp}")
                              
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(payload['high_score'], 10) 
            self.assertEqual(payload['times_played'], 1)   

    def test_update_stats_new_high_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board
                change_session['high_score'] = 10
                change_session['times_played'] = 2

            resp = client.post('/update-stats', json={"score": 15}, content_type='application/json')
            payload = resp.json

            print(f"payload: {payload}")
            print(f"resp: {resp}")
                              
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(payload['high_score'], 15) 
            self.assertEqual(payload['times_played'], 3)  

    def test_update_stats_old_high_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board
                change_session['high_score'] = 10
                change_session['times_played'] = 10

            resp = client.post('/update-stats', json={"score": 8}, content_type='application/json')
            payload = resp.json
                              
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(payload['high_score'], 10) 
            self.assertEqual(payload['times_played'], 11)                        
    
    def test_get_stats_no_history(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board

            resp = client.get('/stats')
            payload = resp.get_data(as_text=True) 

            print(f"payload: {payload}")
            print(f"resp: {resp}")
                              
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['high_score'], 0) 
            self.assertEqual(session['times_played'], 0)
            self.assertIn('"high_score": 0', payload)    
            self.assertIn('"times_played": 0', payload)      

    def test_get_stats_has_history(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board
                change_session['high_score'] = 10
                change_session['times_played'] = 2

            resp = client.get('/stats')
            payload = resp.get_data(as_text=True) 

            print(f"payload: {payload}")
            print(f"resp: {resp}")
                              
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['high_score'], 10) 
            self.assertEqual(session['times_played'], 2)
            self.assertIn('"high_score": 10', payload)    
            self.assertIn('"times_played": 2', payload)    
