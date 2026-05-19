from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Common paths
RAW_DATA_PATH = BASE_DIR / "data" / "UserBehavior.csv"
CLEANED_DATA_PATH = BASE_DIR / "data" / "cleaned" / "user_behavior_cleaned.parquet"
MYSQL_JAR_PATH = BASE_DIR / "drivers" / "mysql-connector-j-8.4.0.jar"
ANALYSIS_SQL_PATH = BASE_DIR / "sql" / "analysis.sql"
VIZ_OUTPUT_DIR = BASE_DIR / "viz" / "output"
ADS_SQL_PATH = BASE_DIR / "ads" / "sql"