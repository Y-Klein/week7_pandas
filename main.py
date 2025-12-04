import pandas as pd

df = pd.read_json(r"C:\git\week7_EXE\week7_pandas\orders_simple.json")


df["order_date"] = pd.to_datetime(df["order_date"])
df["total_amount"] = df["total_amount"].str.replace("$", "0")
df["total_amount"] = pd.to_numeric(df["total_amount"])
df["items_html"] = df["items_html"].str.replace("<br>", " ").str.replace("<b>","").str.replace("</b>","")
df["coupon_used"] = df["coupon_used"].replace("","no coupon")
df = df.assign(order_month = lambda x : x.order_date.dt.month)
total_amount_avg = df["total_amount"].mean()
df = df.assign(high_value_order = df["total_amount"] >  total_amount_avg)
df = df.sort_values("total_amount",ascending=[False])
rating_for_country = df.groupby("country")["rating"].mean
grouped = df.groupby('country')["rating"]
my_mean = grouped.transform(lambda x: x.mean())

df = df.assign(rating_for_country = my_mean)

df = df[(df["total_amount"] > 1000) & (df["rating"]> 4.5)]

df = df.assign(status_delivery = df["shipping_days"] >  7)
df["status_delivery"] = df["status_delivery"].replace(True , "delayed").replace(False,"on time")
df.to_csv("clean_orders_321424855.csv ")

