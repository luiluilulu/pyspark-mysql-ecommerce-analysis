from utils.mysql_utils import get_mysql_connection
from utils.path_utils import VIZ_OUTPUT_DIR

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots #做双y轴图
import plotly.graph_objects as go


 
def query_to_df(sql):
    #Execute SQL and return a DataFrame
    conn = get_mysql_connection()
    df = pd.read_sql(sql,conn)
    conn.close()
    return df

def save_fig(fig,filename):
    #Save fig
    VIZ_OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    
    output_path = VIZ_OUTPUT_DIR / filename
    fig.write_html(str(output_path))

    print("saved:",output_path)

def polt_conversion_funnel():
    sql="""
        SELECT 
            step_order,
            start_users,
            converted_users
        FROM ads_conversion_rate
    """
    df = query_to_df(sql)
    
    pv_users = df[df["step_order"]==1]["start_users"].values[0]
    interest_users = df[df["step_order"]==1]["converted_users"].values[0]
    buy_users = df[df["step_order"]==2]["converted_users"].values[0]

    funnel_date ={
        "stage":["浏览","收藏/加购",'购买'],
        "users":[int(pv_users),int(interest_users),int(buy_users)]
    }

    fig = px.funnel(
        data_frame=funnel_date,
        x = "users",
        y = "stage",
        title="用户行为转化漏斗",
        labels={
            "users": "用户数",
            "stage": "阶段"
        }
    )
    fig.update_traces(textinfo="value+percent initial")

    save_fig(fig,"connversion_funnel.html")

def plot_behavior_type_count():
    sql = """
        SELECT *
        FROM ads_behavior_type_count
        ORDER BY cnt DESC;"""

    df = query_to_df(sql)

    fig = px.bar(
        data_frame= df,
        x="behavior_type",
        y="cnt",
        title="行为类型分布",
        color="behavior_type",
        text = "cnt",
        labels={
            "behavior_type":"行为类型",
            "cnt" : "数量"
        },
        template= "plotly_white"
        )

    save_fig(fig,"behavior_type.html")
    
def plot_daily_pv_uv():
    sql = """
        SELECT behavior_date,pv_cnt,user_cnt
        FROM ads_daily_pv_uv
        ORDER BY behavior_date;"""
    df = query_to_df(sql)

    fig = make_subplots(specs=[
        [{"secondary_y":True}]
        ])
    
    fig.add_trace(
        go.Scatter(
            x=df["behavior_date"],
            y=df["pv_cnt"],
            name = "浏览量",
            mode = 'lines+markers'
        ),
        secondary_y=False
    )


    fig.add_trace(
        go.Scatter(
            x=df["behavior_date"],
            y =df["user_cnt"],
            name="浏览用户数",
            mode="lines+markers"
        ),
        secondary_y=True
    )   

    fig.update_layout(
        title = "每日浏览量 / 浏览用户数",
        template = "plotly_white",
        hovermode ="x unified"
    )

    fig.update_xaxes(title_text = "日期")

    fig.update_yaxes(
        title_text = "浏览量",
        secondary_y=False
    )

    fig.update_yaxes(
        title_text = "浏览用户数",
        secondary_y=True
    )
    '''fig = px.line(
        data_frame=df,
        x="behavior_date",
        y=["pv_cnt","user_cnt"],
        title= "每日浏览量/浏览用户数",
        labels={
            "behavior_date": "日期",
            "pv_cnt" :"浏览量",
            "user_cnt":"用户量"
        },
        markers= True
        )'''
    save_fig(fig,"daily_pv_uv.html")

def plot_hourly_behavior_count():
    sql = """
        SELECT behavior_hour,behavior_cnt
        FROM ads_hourly_behavior_count
        ORDER BY behavior_hour;"""
    df = query_to_df(sql)
    fig = px.bar(
        data_frame=df,
        x="behavior_hour",
        y="behavior_cnt",
        labels={
            "behavior_hour":"小时",
            "behavior_cnt":"总行为量"
        },
        title="历史每小时行为量",
        template="plotly_white"
    )
    fig.update_xaxes(
        tickmode = "linear",
        dtick = 2,
        range=[-0.5,23.5]
    )
    fig.update_yaxes(tickformat=".2s")
    save_fig(fig,"hourly_behavior_count.html")
    
def plot_top10_items():
    sql = """
        SELECT item_id ,all_behavior_cnt
        FROM ads_top10_item_id
        ORDER BY all_behavior_cnt DESC
        LIMIT 10; """
    df = query_to_df(sql)
    df["item_id"] = df["item_id"].astype(str)
    fig = px.bar(
            data_frame= df,
            x= "all_behavior_cnt",
            y="item_id",
            title="热门商品TOP10",
            labels={
                "all_behavior_cnt":"总行为量",
                "item_id":"商品id"
            },
            orientation="h",
            height=500
            )
    fig.update_yaxes(autorange = "reversed")
    save_fig(fig,"top10_items.html")



def main():
    plot_behavior_type_count()
    plot_daily_pv_uv()
    plot_hourly_behavior_count()
    plot_top10_items()
    polt_conversion_funnel()

if __name__ == "__main__":
    main()