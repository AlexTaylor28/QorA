import logging
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

class Neo4jManager:

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri, user, password):
        if self._initialized:
            logger.info(f"[Neo4j Driver] already initialized for {uri}")
            return
        
        self.uri = uri
        
        try:
            self.driver = GraphDatabase.driver(uri, auth = (user, password))
            self.driver.verify_connectivity()
            logger.info(f"[Neo4j Driver] successfully initialized for {uri}")
        except Exception as e:
            logger.error(f"[Neo4j Driver] Failed to connect to {uri}", exc_info = True)
            raise

        self._initialized = True

    def execute_read_one(self, query, parameters = None):
        if not self.driver:
            logger.error("[Neo4j Driver] is not initialized. Cannot execute_read_one().")
            raise ConnectionError("Neo4j Driver is not initialized.")

        def _txn_func(transaction):
            result = transaction.run(query, parameters)
            record = result.single()
            return record.data() if record else None

        try:
            with self.driver.session(default_access_mode = "READ") as session:
                return session.execute_read(_txn_func)
        except Exception as e:
            logger.error(f"[Neo4j Driver] execute_read_one failed. Query: {query} | Params: {parameters}", exc_info = True)
            raise

    def execute_read_many(self, query, parameters = None):
        if not self.driver:
            logger.error("[Neo4j Driver] is not initialized. Cannot execute_read_many().")
            raise ConnectionError("Neo4j Driver is not initialized.")
            
        def _txn_func(transaction):
            result = transaction.run(query, parameters)
            return result.data()
        
        try:
            with self.driver.session(default_access_mode = "READ") as session:
                return session.execute_read(_txn_func)
        except Exception as e:
            logger.error(f"[Neo4j Driver] execute_read_many failed. Query: {query} | Params: {parameters}", exc_info = True)
            raise

    def execute_write(self, query, parameters = None):
        if not self.driver:
            logger.error("[Neo4j Driver] is not initialized. Cannot execute_write().")
            raise ConnectionError("Neo4j Driver is not initialized.")
        
        def _txn_func(transaction):
            result = transaction.run(query, parameters)
            return result.data()
        
        try:
            with self.driver.session(default_access_mode = "WRITE") as session:
                return session.execute_write(_txn_func)
        except Exception as e:
            logger.error(f"[Neo4j Driver] execute_write failed. Query: {query} | Params: {parameters}", exc_info = True)
            raise

    def close(self):
        if self.driver:
            self.driver.close()
            logger.info(f"[Neo4j Driver] closed for {self.uri}")