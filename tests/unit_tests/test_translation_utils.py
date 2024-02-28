import pytest
class TestMBartTranslator:
    def test_MBart_translate_supported_languages(self, translator_MBart):
        text = 'Hello World'
        
        result = translator_MBart.translate(text, 'English', 'Finnish')
        assert isinstance(result, str), "Expected to return string w/ no exceptions"

    def test_MBart_translate_unsupported_language(self, translator_MBart):
        text = 'Hello World'
        with pytest.raises(Exception):
            result = translator_MBart.translate(text, 'English', 'Chinese')
            assert result.contains('Translation error'), "Expected to trigger an Exception and return a translation error"

class TestTranslator:
    def test_check_languages_both_supported(self, translator, translation_row_valid):
        result = translator.check_languages(translation_row_valid['Source'], translation_row_valid['Target'])
        assert result is None

    def test_check_languages_unsupported(self, translator, translation_row_invalid):
        result = translator.check_languages(translation_row_invalid['Source'], translation_row_invalid['Target'])
        assert translation_row_invalid['Source'] in result

    def test_translate_supported(self, translator, translation_row_valid):
        result = translator.translate(translation_row_valid)
        assert isinstance(result['Translated'], str)
    
    def test_translate_unsupported(self, translator, translation_row_invalid):
        result = translator.translate(translation_row_invalid)
        assert translation_row_invalid['Source'] in result['Translated']

