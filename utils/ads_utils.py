from utils.spark_utils import create_spark,write_df_to_mysql
from utils.path_utils import CLEANED_DATA_PATH,ADS_SQL_PATH
from pathlib import Path
#run sparkSQL and write to mysql
def run_spark_sql_to_mysql(
        sql,
        table_name,
        app_name="RunSparkSqlToMysql",
        source_path = CLEANED_DATA_PATH,
        view_name="user_behavior",
        mode="overwrite"
):
    spark  = create_spark(app_name,with_mysql=True)
    try:
        df = spark.read.parquet(str(source_path))
        df.createOrReplaceTempView(view_name)
        result_df = spark.sql(sql)
        
        write_df_to_mysql(result_df,table_name,mode)
    finally:
        spark.stop()
#then a func to write from sqlfile
def run_spark_sql_file_to_mysql(
        sql_path,
        table_name,
        app_name="RunSparkSqlToMysql",
        source_path = CLEANED_DATA_PATH,
        view_name="user_behavior",
        mode="overwrite"
):
    sql = Path(sql_path).read_text(encoding="utf-8")
    run_spark_sql_to_mysql(
        sql=sql,
        table_name=table_name,
        app_name=app_name,
        source_path=source_path,
        view_name=view_name,
        mode=mode
    )
#files
def run_spark_sql_files_to_mysql(
        sql_paths,  
        source_path=CLEANED_DATA_PATH,
        view_name="user_behavior",
        ):
    spark = create_spark("BuildAdsTables", with_mysql=True)
    try:
        df = spark.read.parquet(str(source_path))
        df.createOrReplaceTempView(view_name)

        for sql_path in sql_paths:
            sql = sql_path.read_text(encoding="utf-8")

            result_df = spark.sql(sql)

            table_name = f"ads_{sql_path.stem}"
            write_df_to_mysql(result_df, table_name, mode="overwrite")

            print(f"building {table_name} from {sql_path.stem}")
    finally:
        spark.stop()