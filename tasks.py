import os

from RPA.Excel.Files import Files

from scrapper import logger
from scrapper.tasks.surf_web import Scrapper
from scrapper.utils.constants import EXCEL_FILE_PATH

if not os.path.exists('output'):
    os.mkdir('output')

if __name__ == "__main__":
    logger.info("Starting bot.")
    logger.info("Creating Excel notebook.")
    excel_client = Files()
    excel_client.create_workbook(EXCEL_FILE_PATH)
    excel_client.save_workbook()
    logger.info("Excel notebook created successfully.")
    scrapper = Scrapper()
    scrapper.load_news()
    scrapper.read_news()
    scrapper.generate_output()
    logger.info("Finished...")
