# PySpark + MySQL 电商用户行为分析项目

这是一个用于练习数据工程流程和 SQL 分析的实战项目。项目基于公开电商用户行为数据集，完成从原始 CSV 数据处理、PySpark 清洗、MySQL 入库，到 SQL 聚合分析和 Python 可视化的完整流程。

## 项目流程

```text
原始 CSV 数据
    -> PySpark 数据清洗
    -> 清洗后的 Parquet 数据
    -> MySQL user_behavior 表
    -> SQL 聚合分析
    -> Python 可视化输出
```

## 技术栈

- Python 3.11
- PySpark
- MySQL 8.0
- Docker Compose
- PyMySQL
- MySQL Connector/J
- pandas
- Plotly
- Parquet

## 项目结构

```text
.
├── data/                         # 本地数据目录，不提交到 Git
├── drivers/                      # 本地 JDBC jar，不提交到 Git
├── etl/
│   ├── check_raw_data.py          # 检查原始 CSV 数据
│   ├── clean_user_behavior.py     # 清洗用户行为数据并写出 Parquet
│   └── check_cleaned_data.py      # 检查清洗后的 Parquet 数据
├── load/
│   ├── load_to_mysql.py           # 将清洗后的样本数据写入 MySQL
│   ├── test_spark_mysql_connection.py
│   └── truncate_user_behavior.py
├── sql/
│   ├── analysis.sql               # SQL 分析语句
│   └── run_analysis.py            # 使用 Python 执行 analysis.sql
├── viz/
│   ├── visualize_analysis.py      # 生成 Plotly 可视化图表
│   └── output/                    # 图表输出目录，不建议提交到 Git
├── test/                          # 早期学习和测试脚本
├── utils/
│   ├── config_utils.py            # 读取 .env 并提供 MySQL 配置
│   ├── mysql_utils.py             # MySQL 工具函数
│   ├── path_utils.py              # 项目常用路径
│   └── spark_utils.py             # SparkSession 工具函数
├── requirements.txt
├── config.py                      # 早期配置文件，后续可逐步替换
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

当前 `requirements.txt` 包含：

```text
python-dotenv
pymysql
pyspark
pandas
plotly
```

### 3. 配置 Java 和 Hadoop Windows 工具

PySpark 本地运行需要 Java。本项目使用 Java 17。

```powershell
java -version
```

期望版本：

```text
17.x
```

Windows 本地写 Parquet 时，还需要 Hadoop Windows 辅助文件：

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

项目默认数据库配置：

```text
host: 127.0.0.1
port: 3307
database: taobao_analysis
user: sql_practice
```

## 配置 .env

在项目根目录创建 `.env`：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_USER=sql_practice
MYSQL_PASSWORD=SqlPractice@123456
MYSQL_DATABASE=taobao_analysis
```

`.env` 已加入 `.gitignore`，不要提交到 Git。

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

## 运行方式

所有命令建议在项目根目录执行。

### 创建 MySQL 表

```powershell
python -m create_user_behavior_table
```

### 检查原始数据

```powershell
python -m etl.check_raw_data
```

### 清洗数据

```powershell
python -m etl.clean_user_behavior
```

输出目录：

```text
data/cleaned/user_behavior_cleaned.parquet
```

### 检查清洗结果

```powershell
python -m etl.check_cleaned_data
```

### 导入样本数据到 MySQL

```powershell
python -m load.load_to_mysql
```

当前导入逻辑：

- 读取清洗后的 Parquet 数据
- 取 10000 行样本
- 先清空 `user_behavior` 表
- 再通过 JDBC 追加写入 MySQL

### 测试 Spark 连接 MySQL

```powershell
python -m load.test_spark_mysql_connection
```

### 执行 SQL 分析

```powershell
python -m sql.run_analysis
```

### 生成可视化图表

```powershell
python -m viz.visualize_analysis
```

图表默认输出到：

```text
viz/output/
```

当前可视化包括：

- 行为类型分布柱状图
- 每日 PV / UV 折线图
- 每小时行为量柱状图
- 热门商品 TOP10 横向条形图

## 当前 SQL 分析内容

`sql/analysis.sql` 当前包含：

- 总行数
- 去重用户数
- 去重商品数
- 行为类型分布
- 每日 PV / UV
- 每小时行为量
- 购买次数 TOP10 用户
- 行为次数 TOP10 商品

## 当前进度

- 已完成 Docker MySQL 环境配置
- 已完成 Python 读取 `.env` 并连接 MySQL
- 已完成 MySQL 建表
- 已完成 PySpark 读取原始 CSV
- 已完成 PySpark 清洗并写出 Parquet
- 已完成 Spark 通过本地 JDBC jar 连接 MySQL
- 已完成清洗样本数据写入 MySQL
- 已完成 Python 执行 SQL 分析
- 已完成 Plotly HTML 可视化输出
- 已将路径、配置、Spark、MySQL 公共逻辑抽取到 `utils/`

## 注意事项

- 不要提交 `.env`
- 不要提交 `data/`
- 不要提交 `drivers/` 下的 JDBC jar
- 不建议提交 `viz/output/` 下的图表产物
- 建议从项目根目录使用 `python -m ...` 方式运行脚本
- VS Code 的运行配置可放在本地 `.vscode/launch.json`
