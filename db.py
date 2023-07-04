import mysql.connector as mariadb
import configparser
import logging

from mysql.connector import Error

class Database:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.connection = None
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('Database')
        logger.setLevel(logging.DEBUG)

        # Создание обработчика для вывода логов в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Создание форматировщика для логов
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Добавление обработчика к логгеру
        logger.addHandler(console_handler)

        return logger

    def connect(self):
        try:
            host = self.config.get('database', 'host')
            port = self.config.get('database', 'port')
            user = self.config.get('database', 'user')
            password = self.config.get('database', 'password')
            database = self.config.get('database', 'database')

            self.connection = mariadb.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            self.logger.info("Установлено соединение с базой данных MySQL")
        except Error as e:
            self.logger.error(f"Ошибка при подключении к базе данных MySQL: {e}")

    def execute_query(self, query, values=None):
        try:
            self.connect()
            cursor = self.connection.cursor()

            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            self.connection.commit()

            result = cursor.fetchall()

            cursor.close()
            self.connection.close()

            return result

        except mariadb.Error as e:
            if isinstance(e, mariadb.errors.InterfaceError) and "Connection reset by peer" in str(e):
                self.logger.info("Соединение сброшено. Переподключение...")
                self.connect()
                return self.execute_query(query, values)
            else:
                self.logger.error(f"Ошибка при выполнении запроса: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
        self.logger.info("Отключено от базы данных MySQL")