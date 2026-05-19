from utils.ads_utils import run_spark_sql_file_to_mysql
from utils.path_utils import ADS_SQL_PATH

ADS_SQL_FILES = [
        "rf_segment_summary.sql",
        "category_top_analysis.sql",
]
for sql_file in ADS_SQL_FILES:
    sql_path = ADS_SQL_PATH / sql_file
    run_spark_sql_file_to_mysql(
        sql_path=sql_path,
        table_name=f"ads_{sql_path.stem}",
        app_name=f"BuildAds"+"".join(word.capitalize() for word in sql_path.stem.split('_'))
    )