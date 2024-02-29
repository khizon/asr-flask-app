import pytest
# from app import flask_app

class Test_App():

    def test_Home(self, app):
        with app.test_client() as test_client:
            response = test_client.get('/')

            assert response.status_code == 200
    
    def test_translate_invalid_model(self, app):
        with app.test_client() as test_client:
            response = test_client.post('/translate/InvalidModel/')

            assert response.status_code == 500
            assert "InvalidModel not supported" in response.data.decode()

    def test_translate_empty_data(self, app):
        with app.test_client() as test_client:
            response = test_client.post('translate/MBart/', json=[])

            # assert response.status_code == 500
            assert "Input data needed" in response.data.decode()

    def test_translate_both_languages_supported(self, app, translation_data):
        with app.test_client() as test_client:
            response = test_client.post('/translate/MBart/', json=translation_data)

            assert response.status_code != 500
            
            json_response = response.get_json()
            assert len(json_response) == len(translation_data)
            assert '' == json_response[0]['Error']

    def test_translate_source_language_unsupported(self, app, translation_data):
        with app.test_client() as test_client:
            translation_data[0]['Source'] = 'Unsupported'
            response = test_client.post('/translate/MBart/', json=translation_data)

            assert response.status_code != 500
            
            json_response = response.get_json()
            assert len(json_response) == len(translation_data)
            assert 'Unsupported' in json_response[0]['Error']
            assert '' in json_response[0]['Translated']

    def test_translate_target_language_unsupported(self, app, translation_data):
        with app.test_client() as test_client:
            translation_data[0]['Target'] = 'Unsupported'
            response = test_client.post('/translate/MBart/', json=translation_data)

            assert response.status_code != 500
            
            json_response = response.get_json()
            assert len(json_response) == len(translation_data)
            assert 'Unsupported' in json_response[0]['Error']
            assert '' in json_response[0]['Translated']

    def test_translate_both_languages_unsupported(self, app, translation_data):
        with app.test_client() as test_client:
            translation_data[0]['Source'] = 'Unsupported'
            translation_data[0]['Target'] = 'Unsupported'
            response = test_client.post('/translate/MBart/', json=translation_data)

            assert response.status_code != 500
            
            json_response = response.get_json()
            assert len(json_response) == len(translation_data)
            assert 'Unsupported' in json_response[0]['Error']
            assert '' in json_response[0]['Translated']