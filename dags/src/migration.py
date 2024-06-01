import snowflake.connector
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Snowflake connection parameters
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

def create_snowflake_session():
    try:
        logger.info("Creating Snowflake session...")
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            role=SNOWFLAKE_ROLE
        )
        logger.info("Snowflake session created successfully.")
        return conn
    except Exception as e:
        logger.error(f"Error creating Snowflake session: {e}")
        raise

def check_data_exists(conn):
    try:
        logger.info("Checking if data exists in the 'forecast' table...")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM forecast")
        count = cur.fetchone()[0]
        cur.close()
        return count > 0
    except Exception as e:
        logger.error(f"Error checking data in 'forecast' table: {e}")
        raise

def move_data(conn):
    try:
        logger.info("Moving data from 'forecast' to 'historical_forecast' and clearing 'forecast' table...")
        cur = conn.cursor()

        # Step 1: Insert data from 'forecast' to 'historical_forecast'
        insert_query = """
        INSERT INTO historical_forecast
        SELECT * FROM forecast;
        """
        cur.execute(insert_query)
        
        # Step 2: Truncate the 'forecast' table
        truncate_query = """
        TRUNCATE TABLE forecast;
        """
        cur.execute(truncate_query)
        
        logger.info("Data moved successfully and 'forecast' table has been cleared.")

    except Exception as e:
        logger.error(f"Error moving data in Snowflake: {e}")
        raise
    finally:
        cur.close()

if __name__ == "__main__":
    try:
        # Step 1: Create a Snowflake session
        conn = create_snowflake_session()
        
        # Step 2: Check if data exists in the 'forecast' table
        if check_data_exists(conn):
            # Step 3: Move data from 'forecast' to 'historical_forecast' and clear 'forecast' table
            move_data(conn)
        else:
            logger.info("No data found in 'forecast' table. No operations performed.")
        
    except Exception as e:
        logger.error(f"Failed to run script: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            logger.info("Snowflake session closed.")
