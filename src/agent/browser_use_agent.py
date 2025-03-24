from browser_use import Agent

class BrowserAgent:

    def __init__(self,task,controller,llm):
        self.task=task
        self.controller=controller
        self.llm=llm

    def get_agent(self):
        agent = Agent(
        task= self.task,
        llm=self.llm,
        controller=self.controller
        #,use_vision = true
        )
        return agent