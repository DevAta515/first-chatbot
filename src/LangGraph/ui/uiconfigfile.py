from configparser import ConfigParser

class Config:
    def __init__(self,config_file='./src/LangGraph/ui/uiconfigfile.ini'):
        self.config=ConfigParser()
        self.config.read(config_file)

    def get_llms(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    def get_usecase(self):
        return self.config["DEFAULT"].get("USECASE_OPTIONS").split(", ")
    def get_models(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")
    def get_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")