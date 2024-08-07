from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

MAGENTO_API_URL = "https://magento2-demo.scandiweb.com/rest/V1/products"  # Replace with actual URL
MAGENTO_AUTH_TOKEN = "6sy55rf16u5dktm63r436p0lqtpc2yq8"  # Replace with actual token

def create_magento_product(product):
    headers = {
        "Authorization": f"Bearer {MAGENTO_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(MAGENTO_API_URL, json=product, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

class Product(BaseModel):
    BrandName: str
    ProductID: str
    ProductName: str
    BrandDesc: str
    ProductSize: str
    Currency: str
    MRP: float
    SellPrice: float
    Discount: str
    Category: str

@app.post("/upload-products/")
async def upload_products(products: List[Product]):
    print("inside fast api")
    results = []
    for product in products:
        try:
            magento_product = {
                "product": {
                    "sku": product.ProductID,  # Assuming SKU is mapped from ProductID
                    "name": product.ProductName,
                    "price": product.SellPrice,  # Assuming price is mapped from SellPrice
                    "description": product.BrandDesc,
                    "category_ids": [product.Category],  # Ensure this is a valid ID
                    "attribute_set_id": 4,
                    "status": 1,
                    "visibility": 4,
                    "type_id": "simple",
                }
            }
            print("Sending to Magento:", magento_product)

            result = create_magento_product(magento_product)

            # Log the response from Magento
            print("Magento Response:", result)

            results.append(result)

        except HTTPException as e:
            print("Error sending to Magento:", e.detail)
            results.append({"error": str(e.detail)})
    return {"results": results}
