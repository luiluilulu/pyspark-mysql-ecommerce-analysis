# PySpark MySQL 电商用户行为分析项目

这是一个用于练习 SQL 和数据工程流程的实战项目。项目基于淘宝用户行为数据集，完成从原始 CSV 数据读取、PySpark 清洗、MySQL 存储连接测试，到后续 SQL 聚合分析和 Python 可视化的完整链路。

## 项目流程

```text
原始 CSV 数据
    -> PySpark 数据清洗
    -> Parquet 清洗结果
    -> MySQL 数据表
    -> SQL 聚合分析
    -> Python 可视化
```

## 技术栈

- Python 3.11
- PySpark
- MySQL 8.0
- Docker Compose
- PyMySQL
- MySQL JDBC Driver
- Parquet

## 项目结构

```text
.
├── data/                         # 本地数据目录，不提交到 Git
├── etl/
│   ├── check_raw_data.py          # 检查原始 CSV 数据
│   ├── clean_user_behavior.py     # 清洗用户行为数据并输出 Parquet
│   └── check_cleaned_data.py      # 检查清洗后的 Parquet 数据
├── load/
│   └── test_spark_mysql_connection.py  # 测试 Spark JDBC 连接 MySQL
├── test/                         # 早期连接、建表、插入查询测试脚本
├── config.py                     # 读取 .env 中的 MySQL 配置
├── create_user_behavior_table.py # 创建正式业务表
├── check_user_behavior_table.py  # 检查业务表结构
├── docker-compose.yml            # MySQL 容器配置
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
python -m pip install python-dotenv pymysql pyspark
```

### 3. 配置 Java 和 Hadoop 工具

PySpark 本地运行需要 Java 17。

```powershell
java -version
```

Windows 本地写 Parquet 还需要 Hadoop Windows 工具，目录示例：

```text
C:\hadoop\bin\winutils.exe
C:\hadoop\bin\hadoop.dll
```

对应环境变量：

```text
JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.19.10-hotspot
HADOOP_HOME=C:\hadoop
```

## MySQL 启动

使用 Docker Compose 启动 MySQL：

```powershell
docker compose up -d
```

检查容器：

```powershell
docker ps
```

项目默认使用：

```text
host: 127.0.0.1
port: 3307
database: taobao_analysis
user: sql_practice
```

## 配置 .env

项目根目录创建 `.env`：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_USER=sql_practice
MYSQL_PASSWORD=SqlPractice@123456
MYSQL_DATABASE=taobao_analysis
```

`.env` 已加入 `.gitignore`，不要提交到 Git。

## 数据说明

原始数据文件不提交到仓库，需要手动放到：

```text
data/UserBehavior.csv
```

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

## 运行步骤

### 1. 测试 Python 连接 MySQL

```powershell
python test/test_mysql_connection.py
```

### 2. 创建 user_behavior 表

```powershell
python create_user_behavior_table.py
```

### 3. 检查原始数据

```powershell
python etl/check_raw_data.py
```

### 4. 清洗数据

```powershell
python etl/clean_user_behavior.py
```

清洗后输出：

```text
data/cleaned/user_behavior_cleaned.parquet
```

### 5. 检查清洗结果

```powershell
python etl/check_cleaned_data.py
```

### 6. 测试 Spark 连接 MySQL

```powershell
python load/test_spark_mysql_connection.py
```

## 当前进度

- 已完成 Docker MySQL 环境配置
- 已完成 Python 读取 `.env` 并连接 MySQL
- 已完成 MySQL 建表测试
- 已完成 PySpark 读取原始 CSV
- 已完成 PySpark 清洗并输出 Parquet
- 已完成 Spark JDBC 连接 MySQL 测试

## 后续计划

- 将清洗后的 Parquet 数据写入 MySQL
- 编写 SQL 聚合分析脚本
- 完成用户行为指标分析
- 使用 Python 绘制可视化图表

## 注意事项

- `data/` 目录不提交到 Git
- `.env` 不提交到 Git
- JDBC 驱动当前通过 Spark 自动下载
- Windows 本地运行 Spark 需要正确配置 Java 17、`winutils.exe` 和 `hadoop.dll`
