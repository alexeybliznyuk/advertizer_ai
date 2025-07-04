from service.deepseek_repository import DeepSeekRepository

class DeepSeekService:
    def __init__(self):
        self.repository = DeepSeekRepository()

    def create_post(self, user_input):
        system_prompt = "Предложи пост для пользователя, который проходит курс."
        conversation = [{"role": "system", "content": f"{system_prompt}"}]
        conversation += user_input

        generation_information = [{"informaion_about_course":
         {"course_title": "Python для продвинутых",
    "short_description": "Углубленный курс для тех, кто уже освоил основы Python и хочет выйти на профессиональный уровень. Вы изучите продвинутые концепции языка, такие как метаклассы, декораторы, асинхронное программирование, оптимизацию кода и работу с большими данными. Практические задания и реальные кейсы помогут закрепить навыки и подготовиться к сложным проектам.",
    "tags": "Python, ПродвинутыйУровень, ООП",
    "gender": "Любой",
    "skill_level": "Продолжающие"}
        }
        ]
        conversation += generation_information

        data = {
            "model": "deepseek-chat",
            "messages": conversation
        }

        response = self.repository.call_deepseek_api(data)
        return response 

    def create_message(self, user_input):
        system_prompt = "Предложи сообщение для пользователя, который проходит курс."
        conversation = [{"role": "system", "content": f"{system_prompt}"}]
        conversation += user_input

        generation_information = [{"informaion_about_course":
         {"course_title": "Python для продвинутых",
    "short_description": "Углубленный курс для тех, кто уже освоил основы Python и хочет выйти на профессиональный уровень. Вы изучите продвинутые концепции языка, такие как метаклассы, декораторы, асинхронное программирование, оптимизацию кода и работу с большими данными. Практические задания и реальные кейсы помогут закрепить навыки и подготовиться к сложным проектам.",
    "tags": "Python, ПродвинутыйУровень, ООП",
    "gender": "Любой",
    "skill_level": "Продолжающие"}
        }
        ]
        conversation += generation_information

        data = {
            "model": "deepseek-chat",
            "messages": conversation
        }

        response = self.repository.call_deepseek_api(data)
        return response 