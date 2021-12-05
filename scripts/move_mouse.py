#! /usr/bin/env /usr/bin/python3

from config import Config
import pyautogui
from logging_setup import get_logger, add_handler
from random import randint

logger = get_logger(__name__)

module = __file__.split('/')[-1].split('.')[0]

logging_path = Config.LOGS_DIR + "/" + module + "/"
add_handler(logger, logging_path)

if __name__ == "__main__":
	rand = randint(1, 10)

	logger.info(f"Moving mouse down {rand} pixel")
	pyautogui.moveRel(0, -rand)
	logger.info(f"Moved mouse down {rand} pixel")

	logger.info(f"Moving mouse up {rand} pixel")
	pyautogui.moveRel(0, rand)
	logger.info(f"Moved mouse up {rand} pixel")
