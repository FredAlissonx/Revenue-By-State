import logging
from pyspark.sql import SparkSession

class SparkSessionManager:
    _spark_session = None

    @classmethod
    def get_spark_session(cls, app_name: str, config: dict = None) -> SparkSession:
        """
        Creates or retrieves a Spark session.

        Parameters
        ----------
        app_name : str
            The name of the Spark application.
        config : dict, optional
            A dictionary of Spark configurations to be set in the session.

        Returns
        -------
        SparkSession
            A configured Spark session.
        """
        if cls._spark_session is None:
            try:
                builder = SparkSession.builder.appName(app_name)
                if config:
                    for key, value in config.items():
                        builder = builder.config(key, value)
                cls._spark_session = builder.getOrCreate()
            except Exception as e:
                logging.error(f"Error creating Spark session: {e}")
                raise
        return cls._spark_session
