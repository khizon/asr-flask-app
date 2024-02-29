from transformers import MBartForConditionalGeneration, MBart50TokenizerFast, SeamlessM4TModel, AutoProcessor

class MBartTranslator:
    def __init__(self):
        self.model = MBartForConditionalGeneration.from_pretrained('facebook/mbart-large-50-many-to-many-mmt')
        self.tokenizer = MBart50TokenizerFast.from_pretrained('facebook/mbart-large-50-many-to-many-mmt')

        self.lang_map = {
            'English': 'en_XX',
            'Finnish': 'fi_FI',
        }

    def translate(self, text, src_lang='Finnish', tgt_lang='English'):
        try:
            self.tokenizer.src_lang = self.lang_map[src_lang]
            encoded = self.tokenizer(text, return_tensors='pt')
            forced_bos_token_id = self.tokenizer.lang_code_to_id[self.lang_map[tgt_lang]]
            generated_tokens = self.model.generate(**encoded, forced_bos_token_id=forced_bos_token_id)
            return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        except Exception as e:
            print(f'Error during MBart translation: {e}')
            return f'Translation error: {e}'

class SeamlessM4TTranslator:
    def __init__(self):
        self.model = SeamlessM4TModel.from_pretrained('facebook/hf-seamless-m4t-medium')
        self.processor = AutoProcessor.from_pretrained('facebook/hf-seamless-m4t-medium')
        self.lang_map = {
            'Finnish': 'fin',
            'English': 'eng'
        }

    def translate(self, text, src_lang='Finnish', tgt_lang='English'):
        try:
            text_inputs = self.processor(text=text, src_lang = self.lang_map[src_lang], tgt_lang = self.lang_map[tgt_lang], return_tensors='pt')
            output_tokens = self.model.generate(**text_inputs, tgt_lang=self.lang_map[tgt_lang], generate_speech=False)
            return self.processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
        except Exception as e:
            print(f'Error during SeamlessM4T Translations: {e}')
            return f'Translation Error: {e}'

class Translator:
    def __init__(self, model_name='MBart'):
        self.model_name = model_name

        if self.model_name == 'MBart':
            self.translator = MBartTranslator()
        elif self.model_name == 'SeamlessM4T':
            self.translator = SeamlessM4TTranslator()
        else:
            raise ValueError(f'Invalid model name: {self.model_name}')
        
    def translate(self, row):
        text = row['Text']
        src, tgt = row['Source'], row['Target']
        missing_langs = self.check_languages(src, tgt)

        if missing_langs is None:
            row['Translated'] = self.translator.translate(text, src, tgt)
            row['Error'] = ''
        else:
            row['Translated'] = ''
            row['Error'] = missing_langs

        return row
    
    def check_languages(self, src_lang, tgt_lang):
        missing_langs = [lang for lang in [src_lang, tgt_lang] if lang not in self.translator.lang_map]

        if missing_langs:
            return f"{self.model_name} does not support {', '.join(missing_langs)}"
        else:
            return None