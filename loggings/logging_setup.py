import logging
import logging.config
import json
import os


class LoggerSetup:
    """
    A class used to configure and provide loggers for ETL and analysis processes.

    Methods
    -------
    config_logging(config_path: str = "logging_config.json") -> None
        Configures the logging settings from a JSON file.

    get_logger(logger_name: str) -> logging.Logger
        Returns a configured logger by name.
    """

    _is_configured = False  # Class-level variable to track configuration
    CONFIG_PATH = "C:\\RevenueByState\\loggings\\logging_config.json"

    @classmethod
    def config_logging(self, config_path: str = CONFIG_PATH) -> None:
        """
        Configures the logging settings.

        This method loads the logging configuration from a JSON file 
        and sets up the loggers.

        Parameters
        ----------
        config_path : str
            Path to the logging configuration JSON file.
        """
        if not LoggerSetup._is_configured:
            log_dir = "C:\\RevenueByState\\loggings"
            os.makedirs(log_dir, exist_ok=True)

            try:
                with open(config_path, 'r') as file:
                    config = json.load(file)
                logging.config.dictConfig(config)
                LoggerSetup._is_configured = True  # Mark as configured
            except FileNotFoundError:
                logging.basicConfig(level=logging.WARNING)
                logging.warning(f"Logging configuration file not found: {config_path}")
            except json.JSONDecodeError as e:
                logging.basicConfig(level=logging.WARNING)
                logging.warning(f"Error decoding JSON logging configuration: {e}")
    @classmethod
    def get_logger(self, logger_name: str) -> logging.Logger:
        """
        Returns a configured logger by name.

        This method sets up the logger using the logging configuration 
        defined in `config_logging`.

        Parameters
        ----------
        logger_name : str
            The name of the logger to return.

        Returns
        -------
        logging.Logger
            The configured logger.
        """
        if not LoggerSetup._is_configured:
            self.config_logging()
        return logging.getLogger(logger_name)

    @classmethod
    def get_analysis_logger(self) -> logging.Logger:
        """
        Returns a logger for EDA tasks.

        Returns
        -------
        logging.Logger
            The configured logger for analysis tasks.
        """
        return self.get_logger(logger_name="analysis_logger")

    @classmethod
    def get_etl_logger(self) -> logging.Logger:
        """
        Returns a logger for ETL tasks.

        Returns
        -------
        logging.Logger
            The configured logger for ETL tasks.
        """
        return self.get_logger(logger_name="etl_logger")

    @classmethod
    def get_database_logger(self) -> logging.Logger:
        """
        Returns a logger for database tasks.

        Returns
        -------
        logging.Logger
            The configured logger for database tasks.
        """
        return self.get_logger(logger_name="database_logger")