from utils.ads_utils import run_spark_sql_files_to_mysql
from utils.path_utils import ADS_SQL_PATH

ADS_SQL_FILES = sorted(ADS_SQL_PATH.glob("*.sql"))

run_spark_sql_files_to_mysql(ADS_SQL_FILES)