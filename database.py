import os
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("database.py")
logger.setLevel(logging.INFO)


metadata = MetaData()
Base = declarative_base(metadata=metadata)


def get_db_session():
    return DatabaseManager().get_db_session()


def dsn_from_env():
    """returns dsn suitable to pass to sqlalchemy's create_engine
    if env var SQLALCHEMY_DSN is found, it will be used, else composite vars
    are examined (note at least SQLALCHEMY_DBNAME is required):
      * SQLALCHEMY_SCHEME (default=postgres)
      * SQLALCHEMY_HOST (default=localhost)
      * SQLALCHEMY_PORT (default=5432)
      * SQLALCHEMY_DBNAME (no default; required)
      * SQLALCHEMY_USER (no default; required for authed access to db)
      * SQLALCHEMY_PASS (no default; required for authed access to db)
    """
    dsn = os.environ.get("SQLALCHEMY_DSN", "")
    # For local use only
    # Deployed code gets it from environment
    dsn = "postgresql://currentapi:Current123!@aa8og5oo6hypyq.cm3yh0naog66.us-east-1.rds.amazonaws.com:5432/current_api_v1"
    if not dsn:
        scheme = os.environ.get("SQLALCHEMY_SCHEME", "postgres")
        host = os.environ.get("SQLALCHEMY_HOST", "localhost")
        port = os.environ.get("SQLALCHEMY_PORT", "5432")
        dbname = os.environ.get("SQLALCHEMY_DBNAME", "")
        user = os.environ.get("SQLALCHEMY_USER", "")
        pwd = os.environ.get("SQLALCHEMY_PASS", "")
        if not dbname:
            raise ValueError("SQLALCHEMY_DSN or SQLALCHEMY_DBNAME is required")
        auth = "{}:{}@".format(user, pwd) if user and pwd else ""
        if not auth:
            logger.warning("DB auth not configured")
        dsn = "{}://{}{}:{}/{}".format(scheme, auth, host, port, dbname)
    logger.info("dsn_from_env: {}".format(dsn))
    return dsn


class DatabaseManager(object):
    def __new__(self):
        """
        Creates a Singleton Class for Database
        """
        if not hasattr(self, "instance"):
            self.instance = super().__new__(self)
        return self.instance

    def __init__(self):
        if not hasattr(self, "engine"):
            logger.info("creating a new DB Engine")
            self.engine = self.create_db_engine()

    @staticmethod
    def create_db_engine():
        return create_engine(dsn_from_env(), echo=True, pool_size=10, max_overflow=10)

    def get_db_session(self):
        session = sessionmaker()
        session.configure(bind=self.engine)
        db_session = session()
        return db_session
