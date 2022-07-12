import logging

logger = logging.Logger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(levelname)s] %(name)s : %(asctime)s - %(message)s')
file_handler = logging.FileHandler('Log.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
