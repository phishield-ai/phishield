import json
from typing import Dict, Optional

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from loguru import logger

from phishield.conf import environment


class GoogleLM:
    def __init__(
        self,
        model: Optional[genai.GenerativeModel] = None,
        config: Optional[genai.GenerationConfig] = None,
        api_key: Optional[str] = None,
        safety_settings: Optional[Dict[HarmCategory, HarmBlockThreshold]] = None,
    ):
        if api_key is None:
            api_key = environment.GOOGLE_API_KEY
        if model is None:
            model = genai.GenerativeModel(model_name=environment.GOOGLE_AI_MODEL)
        if config is None:
            config = genai.GenerationConfig(temperature=0.0)

        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            logger.error(f"Error configuring the Google API: {e}")

        self.model = model
        self.config = config
        self.api_key = api_key

        if safety_settings is None:
            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

    def _parse_json(self, input: str):
        starting = "```json"
        content = input.find(starting)
        ending = input.rfind("```")
        return input[content + len(starting) : ending]

    async def ask(self, prompt: str, jsonable: bool = True) -> str:
        response = await self.model.generate_content_async(
            prompt, generation_config=self.config, safety_settings=self.safety_settings
        )

        if jsonable:
            return json.loads(self._parse_json(response.text))

        return response.text
