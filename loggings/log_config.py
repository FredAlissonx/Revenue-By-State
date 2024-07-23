import logging
import logging.config
import os

class LoggerConfig:
    """
    A class used to configure and provide loggers for ETL and analysis processes.

    Methods
    -------
    config_logging() -> dict
        Configures the logging settings and returns the configuration dictionary.
    
    get_analysis_logger()
        Configures and returns a logger for analysis tasks.
    
    get_etl_logger()
        Configures and returns a logger for ETL tasks.
    """
    
    def config_logging(self) -> dict:
        """
        Configures the logging settings.

        This method sets up loggers, handlers, and formatters for logging. 
        It ensures that log files are stored in the specified directory.

        Returns
        -------
        dict
            The logging configuration dictionary.
        """
        
        log_dir = "C:\\RevenueByState\\loggings"
        os.makedirs(log_dir, exist_ok=True)
        
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(levelname)s - %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard'
                },
                'analysis_file_handler': {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'formatter': 'standard',
                    'filename': os.path.join(log_dir, 'analysis.log'),
                    'mode': 'a'
                },
                'etl_file_handler': {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'formatter': 'standard',
                    'filename': os.path.join(log_dir,'etl.log'),
                    'mode': 'a'
                }
            },
            'loggers': {
                'etl_logger': {
                    'handlers': ['etl_file_handler', 'console'],
                    'level': 'DEBUG',
                    'propagate': False
                },
                'analysis_logger': {
                    'handlers': ['analysis_file_handler', 'console'],
                    'level': 'DEBUG',
                    'propagate': False
                },
            }
        }

    def get_analysis_logger(self):
        """
        Configures and returns a logger for analysis tasks.

        This method sets up the logger for analysis tasks using the logging 
        configuration defined in `config_logging`.

        Returns
        -------
        logging.Logger
            The configured logger for analysis tasks.
        """
        
        logging.config.dictConfig(config=self.config_logging())
        return logging.getLogger("analysis_logger")
    
    def get_etl_logger(self):
        """
        Configures and returns a logger for ETL tasks.

        This method sets up the logger for ETL tasks using the logging 
        configuration defined in `config_logging`.

        Returns
        -------
        logging.Logger
            The configured logger for ETL tasks.
        """
        
        logging.config.dictConfig(config=self.config_logging())
        return logging.getLogger("etl_logger")
