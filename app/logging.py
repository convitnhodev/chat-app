import logging 
import logging.handlers
import time 


class LoggerSetup: 
    def __init__(self) -> None:
        self.logger = logging.getLogger('')
        self.setup_logging()

    def setup_logging(self):
        pass 
        
            