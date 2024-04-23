import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

import json
import time
from google.api_core.exceptions import ResourceExhausted
import os

from typing import Optional, Dict


class GoogleLM:
    def __init__(self, 
                 model : genai.GenerativeModel, 
                 config : genai.GenerationConfig, 
                 api_key : Optional[str], 
                 safety_settings : Optional[Dict[HarmCategory, HarmBlockThreshold]] = None,
                 verbose = True) -> dict:
        
        """ GoogleLM class that can send prompts for Google's Generative AI models. It can be used to send prompts to the Gemini model to generate phishing detection reports given an URL.

        Args:
            model (genai.GenerativeModel): a generative model from Google's Generative AI models
            config (genai.GenerationConfig): a generation config for the model
            api_key (Optional[str]):  string with google api key, if not given it will read from the environment the GOOGLE_APL_KEY
            safety_settings (Optional[Dict[HarmCategory, HarmBlockThreshold]], optional): An object that blinds the final user from not compliant outputs. Defaults to None.
            verbose (bool): print the LM response. Defaults to True.

        Returns:
            dict: a json formatted output with the following fields: phishing_score, brands, phishing, suspicious_domain
        """
        
        load_dotenv()
        if api_key is None:
            #read the api key from the environment
            api_key = os.getenv("GOOGLE_API_KEY")

        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            print(f"Error configuring the Google API: {e}")
        
        if not isinstance(config, genai.GenerationConfig):
            raise ValueError("config must be an instance of genai.GenerationConfig")
        
        if not isinstance(model, genai.GenerativeModel):
            raise ValueError("config must be an instance of genai.GenerationConfig")
        
        self.model = model
        self.config = config 
        
        # https://ai.google.dev/gemini-api/docs/safety-settings
        if safety_settings is None:

            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        
        self.api_key = api_key
        self.verbose = verbose

    def _parse_lines(self, s):
        first_str = "```json"
        ind1 = s.find(first_str)
        ind2 = s.rfind("```")
        return s[ind1+len(first_str):ind2]

    def _create_prompt(self, url) -> str:
        
        return f"""
        You are a web programmer and security expert tasked with examining a URL to determine if it is a phishing site or a legitimate site.
        Submit your findings as JSON-formatted output with the following keys:
        - phishing_score: int (indicates phishing risk on a scale of 0 to 100)
        - brands: str (identified brand name or None if not applicable)
        - phishing: boolean (whether the site is a phishing site or a legitimate site)
        - suspicious_domain: boolean (whether the domain name is suspected to be not legitimate)
        - suspicious_elements : str (enumeration of suspicious elements found on the site or "No suspicious elements" if not applicable)
        URL:
        {url}"""

    def send_prompt(self, url):

        sec_prompt = self._create_prompt(url)
        try:
            resp = self.model.generate_content(
                sec_prompt , 
                generation_config = self.config ,
                safety_settings = self.safety_settings
            )
        
        #Doc w' timeouts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   https://ai.google.dev/gemini-api/docs/models/gemini
        except ResourceExhausted:
            
            start_time = time.time()
            end_time = start_time + 60  # 1 minute

            while time.time() < end_time:
                try:
                    resp = self.model.generate_content(
                    sec_prompt , 
                    generation_config = self.config ,
                    safety_settings = self.safety_settings
                )
                except Exception as e:
                    print(f"Request failed: {e}")
                    time.sleep(1)
    
        #text_resp = resp.parts[0].text
        text_resp = resp.text
        if self.verbose:
            print(text_resp)
        json_resp = json.loads(self._parse_lines(text_resp))
        return json_resp
    


if __name__ == "__main__":

    for MODEL_NAME in ['models/gemini-1.0-pro', 'models/gemini-1.5-pro-latest']:
        config = genai.GenerationConfig(temperature=0.0)
        model = genai.GenerativeModel(MODEL_NAME)

        lm = GoogleLM(model = model, config=config, api_key=None, verbose=True)

        print(f'{MODEL_NAME} - Prompting for URLs')

        lm.send_prompt("www.facebook.com")
        lm.send_prompt("http://shadetreetechnology.com/V4/validation/a111aedc8ae390eabcfa130e041a10a4")
        lm.send_prompt("https://support-appleld.com.secureupdate.duilawyeryork.com/ap/89e6a3b4b063b8d/?cmd=_update&dispatch=89e6a3b4b063b8d1b&locale=_")

        print('='*80)