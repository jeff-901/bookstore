import csv
import pandas as pd
import requests
import json
import numpy as np

with open("book.csv", newline="") as f:
    df = pd.read_csv(
        f,
        names=[
            "book_id",
            "ISBN",
            "name",
            "author",
            "author_original",
            "translator",
            "publishing_house",
            "publishing_date",
            "price",
        ],
    )


def add_book(data):
    # print(data)
    for key in data:
        if data[key] == "None" or data[key] == "":
            data[key] = None
    res = requests.post(
        "http://127.0.0.1:5000/api/book",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data),
    )
    # print(res.text)
    if res.status_code != 201 and res.text[-14:] != "already eists.":
        print(data)
        print(res.text)


rows = df.to_dict(orient="records")
with open("discount.csv", newline="") as f:
    df_discount = pd.read_csv(
        f,
        names=["book_id", "discount_price", "expire_date"],
    )


for row in rows:
    if df_discount.loc[df_discount["book_id"] == row["book_id"]] is not None:
        discounts = df_discount.loc[df_discount["book_id"] == row["book_id"]].to_dict(
            orient="records"
        )
        if len(discounts) > 0:
            discount = discounts[0]
            row["discount"] = {
                "discount_price": discount["discount_price"],
            }
            if "None" == discount.get("expire_date"):
                row["discount"]["expire_date"] = None
            elif "本" not in discount["expire_date"]:
                row["discount"]["expire_date"] = discount["expire_date"]
            else:
                row["discount"]["expire_date"] = None
    # print(row)
    if row["author"] != "None" and row["author"] != "":
        add_book(row)
    # break
