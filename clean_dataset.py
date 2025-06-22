import pandas as pd

def clean_amazon_data(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    # ✅ Step 1: Rename FIRST
    df = df.rename(columns={
        "title": "name",
        "productURL": "url",
        "price": "target_price"
    })

    # ✅ Step 2: Now drop rows with missing name, url, or target_price
    df = df.dropna(subset=["name", "url", "target_price"])

    # Step 3: Filter URLs containing '/dp/'
    df = df[df["url"].str.contains("/dp/")]

    # Step 4: Clean price values
    df["target_price"] = (
        df["target_price"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    # Step 5: Keep only numeric, valid prices
    df = df[pd.to_numeric(df["target_price"], errors="coerce").notnull()]
    df["target_price"] = df["target_price"].astype(float)
    df = df[df["target_price"] > 100]

    # Step 6: Drop duplicates and unnecessary columns
    df = df.drop_duplicates(subset="url")
    df = df[["name", "url", "target_price"]]
    df = df.head(1000)

    # Step 7: Save cleaned file
    df.to_csv(output_csv, index=False)
    print(f"✅ Cleaned dataset saved as {output_csv} with {len(df)} rows")

if __name__ == "__main__":
    clean_amazon_data("raw_products.csv", "products.csv")
