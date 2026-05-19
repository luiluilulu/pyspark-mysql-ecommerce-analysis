# PySpark + MySQL 电商用户行为分析项目

这是一个面向数据开发与数据分析练习的电商用户行为分析项目。项目基于公开用户行为数据集，完成从原始 CSV、PySpark 清洗、Parquet 明细落地、Spark SQL 全量聚合、MySQL ADS 结果表，到 Plotly 可视化输出的完整链路。

项目同时保留一张 MySQL 样本明细表 `user_behavior`，用于 SQL 练习和小样本验证；正式报表与可视化优先读取 Spark 全量聚合后的 `ads_*` 结果表。

## 项目流程

```text
原始 CSV
    -> PySpark 全量清洗
    -> Parquet 明细层
    -> Spark SQL 全量聚合
    -> MySQL ads_* 结果表
    -> Plotly 可视化
```

同时保留样本链路：

```text
Parquet 明细层
    -> MySQL user_behavior 10000 行样本
    -> SQL 练习与小样本验证
```

## 技术栈

- Python 3.11
- PySpark / Spark SQL
- Parquet
- MySQL 8.0
- Docker Compose
- PyMySQL
- MySQL Connector/J
- pandas
- Plotly
- Git

## 项目结构

```text
.
├── ads/
│   ├── build_ads.py              # 扫描 ads/sql/*.sql，批量构建 MySQL ads_* 表
│   └── sql/                      # Spark SQL 全量聚合脚本
├── data/                         # 本地数据目录，不提交到 Git
├── drivers/                      # 本地 JDBC jar，不提交到 Git
├── etl/
│   ├── check_raw_data.py          # 检查原始 CSV 数据
│   ├── clean_user_behavior.py     # 清洗用户行为数据并写出 Parquet
│   └── check_cleaned_data.py      # 检查清洗后的 Parquet 数据
├── load/
│   ├── load_to_mysql.py           # 将 10000 行样本明细写入 MySQL
│   ├── test_spark_mysql_connection.py
│   └── truncate_user_behavior.py
├── sql/
│   ├── analysis.sql               # MySQL 样本表 SQL 练习
│   └── run_analysis.py            # 使用 Python 执行 analysis.sql
├── utils/
│   ├── ads_utils.py               # Spark SQL -> MySQL ADS 表工具函数
│   ├── config_utils.py            # 读取 .env 并提供 MySQL/JDBC 配置
│   ├── mysql_utils.py             # MySQL 工具函数
│   ├── path_utils.py              # 项目常用路径
│   └── spark_utils.py             # SparkSession 与 JDBC 写入工具函数
├── viz/
│   ├── visualize_analysis.py      # 从 ads_* 表读取数据并生成 Plotly 图表
│   └── output/                    # 图表输出目录，不提交到 Git
├── report.md                      # 项目分析报告
├── requirements.txt
├── create_user_behavior_table.py
├── check_user_behavior_table.py
├── docker-compose.yml
└── .gitignore
```

## 环境准备

### 1. 创建 Conda 环境

```powershell
conda create -n sql-practice python=3.11
conda activate sql-practice
```

### 2. 安装 Python 依赖

```powershell
python -m pip install -r requirements.txt
```

### 3. 配置 Java 与 Hadoop Windows 工具

PySpark 本地运行需要 Java。本项目使用 Java 17。

```powershell
java -version
```

Windows 本地运行 Spark/Parquet 时，需要准备 Hadoop Windows 辅助文件：

```text
C:\hadoop\bin\winutils.exe
C:\hadoop\bin\hadoop.dll
```

建议配置环境变量：

```text
JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.19.10-hotspot
HADOOP_HOME=C:\hadoop
```

### 4. 准备 MySQL JDBC 驱动

下载 MySQL Connector/J，并将 jar 文件放到：

```text
drivers/mysql-connector-j-8.4.0.jar
```

`drivers/*.jar` 已加入 `.gitignore`，不会提交到 Git。

## 启动 MySQL

使用 Docker Compose 启动 MySQL：

```powershell
docker compose up -d
```

检查容器状态：

```powershell
docker ps
```

本地连接配置由 `.env` 管理。`.env` 不提交 Git，示例：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=taobao_analysis
```

## 数据集说明

将原始 CSV 文件放到：

```text
data/UserBehavior.csv
```

原始数据文件不提交到 Git。

字段顺序：

```text
user_id,item_id,category_id,behavior_type,timestamp
```

行为类型：

```text
pv    浏览
fav   收藏
cart  加购
buy   购买
```

清洗后保留字段：

```text
user_id
item_id
category_id
behavior_type
behavior_time
behavior_date
behavior_hour
```

## 运行顺序

所有命令建议在项目根目录执行。

### 1. 创建 MySQL 样本明细表

```powershell
python -m create_user_behavior_table
```

### 2. 检查原始数据

```powershell
python -m etl.check_raw_data
```

### 3. 全量清洗数据

```powershell
python -m etl.clean_user_behavior
```

输出目录：

```text
data/cleaned/user_behavior_cleaned.parquet
```

### 4. 检查清洗结果

```powershell
python -m etl.check_cleaned_data
```

### 5. 导入 10000 行样本明细到 MySQL

```powershell
python -m load.load_to_mysql
```

该步骤只写入样本明细，用于 SQL 练习，不承担全量报表分析。

### 6. 构建全量 ADS 结果表

```powershell
python -m ads.build_ads
```

`ads/build_ads.py` 会自动扫描：

```text
ads/sql/*.sql
```

每个 SQL 文件会生成一张 MySQL 结果表：

```text
ads_ + SQL 文件名去掉 .sql
```

例如：

```text
ads/sql/daily_pv_uv.sql -> ads_daily_pv_uv
ads/sql/rf_segment_summary.sql -> ads_rf_segment_summary
```

当前 ADS 指标包括：

- `ads_behavior_type_count`
- `ads_category_top_analysis`
- `ads_conversion_rate`
- `ads_daily_pv_uv`
- `ads_hourly_behavior_count`
- `ads_repurchase_summary`
- `ads_rf_segment_summary`
- `ads_top10_item_id`

### 7. 生成可视化图表

```powershell
python -m viz.visualize_analysis
```

图表默认输出到：

```text
viz/output/
```

`viz/output/` 不提交 Git。

## 指标说明

项目当前覆盖以下指标：

- 行为类型分布：统计 `pv`、`cart`、`fav`、`buy` 的行为量。
- 每日 PV/UV：统计每日浏览量和浏览用户数。
- 每小时行为量：分析用户行为在一天内的活跃时段。
- 转化漏斗：浏览 -> 收藏/加购 -> 购买。
- 复购率：购买次数大于等于 2 的购买用户占比。
- 类目热度 TOP10：按类目总行为量排序，统计浏览、收藏/加购、购买和购买用户数。
- 商品 TOP10：按商品总行为量排序。
- RF 用户分层：由于数据集没有金额字段，使用最近购买间隔和购买次数做 RF 分层，替代完整 RFM。

## 设计说明

本项目不将 1 亿级明细全量写入 MySQL。原因是 MySQL 更适合作为结果查询和可视化支撑，不适合在本地环境承载大规模行为明细分析。

当前分工：

```text
Parquet: 保存清洗后的全量明细
Spark SQL: 执行全量聚合计算
MySQL user_behavior: 保存 10000 行样本用于 SQL 练习
MySQL ads_*: 保存小规模分析结果表
Plotly: 读取 ads_* 表生成可视化
```

## Windows 本地 Spark 注意事项

- Java 建议使用 17。
- Windows 下需要配置 `winutils.exe` 和 `hadoop.dll`。
- Spark 连接 MySQL 需要本地 MySQL Connector/J jar。
- 本地 Spark 结束时可能出现临时目录 jar 删除 warning，例如无法删除 `mysql-connector-j-8.4.0.jar`。如果结果表已正常写入 MySQL，该 warning 通常不影响计算结果。
- 建议使用 `python -m 包名.模块名` 从项目根目录运行脚本。

## Git 注意事项

不要提交以下内容：

```text
.env
data/
drivers/*.jar
viz/output/
sql/sql_practice_mysql.session.sql
```

## 项目报告

项目分析报告见：

```text
report.md
```
