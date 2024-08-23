import mysql.connector
from mysql.connector import Error
from loggings.logging_setup import LoggerSetup

class DatabaseConnector:
    def __init__(self, host, user, password):
        self._conn = None
        self._host = host
        self._user = user
        self._password = password
        self._database_name = None
        self._logger = self.setup_logging()
        
    
    def setup_logging(self):
        return LoggerSetup.get_database_logger()
    
    def get_connection(self):
        try:
            self._conn = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password
            )
            if self._conn.is_connected():
                self._logger.info("Connected to MySQL server")
        except Error as e:
            self._logger.error(f"Error in connection: {e}")
            self._conn = None
    
    def create_database(self, database_name):
        if self._conn is None or not self._conn.is_connected():
            self._logger.warning("Connection not established or already closed. Call get_connection() first.")
            return
        
        try:
            with self._conn.cursor() as cursor:
                self._database_name = database_name
                query_create_database = f"CREATE DATABASE IF NOT EXISTS `{database_name}`"
                cursor.execute(query_create_database)
                self._logger.info(f"Database '{database_name}' created or already exists")
        except Error as e:
            self._logger.error(f"Error creating the database: {e}")
    
    
    def close_connection(self):
        if self._conn and self._conn.is_connected():
            self._conn.close()
            self._logger.info("MySQL connection is closed")
    
    def get_jdbc_url_and_properties(self):
        if self._database_name is None:
            self._logger.warning("Database name is not set. Please create a database first.")
            return None, None
        
        jdbc_url = f"jdbc:mysql://{self._host}/{self._database_name}"
        jdbc_properties = {
            "user": self._user,
            "password": self._password,
            "driver": "com.mysql.cj.jdbc.Driver"
        }
        
        return jdbc_url, jdbc_properties