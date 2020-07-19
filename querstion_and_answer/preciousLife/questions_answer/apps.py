from django.apps import AppConfig


class QuestionsAnswerConfig(AppConfig):
    name = 'questions_answer'
    def ready(self):
        import accounts.signals
    
