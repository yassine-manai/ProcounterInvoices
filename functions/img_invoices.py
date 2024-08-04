import os
import requests
from config.config import PROCOUNTOR_URL
from functions.request_api import get_headers  
from config.log_config import logger

def fetch_invoices_and_images():
    base_url = f"{PROCOUNTOR_URL}/invoices"
    headers = get_headers()
    
    try:
        response = requests.get(base_url,headers=headers)
        response.raise_for_status()  
        data = response.json()
        
        if response.status_code == 200 and "results" in data:
            invoices = data["results"]
            
            if not os.path.exists("images_invoices"):
                os.makedirs("images_invoices")
            
            for invoice in invoices:
                invoice_id = invoice["id"]
                image_url = f"{base_url}/{invoice_id}/image"
                
                try:
                    image_response = requests.get(image_url,headers=headers)
                    image_response.raise_for_status()
                    
                    image_path = os.path.join("invoices/images_invoices", f"image_{invoice_id}.png")
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_response.content)
                    
                        #logger.success(f"Image for invoice {invoice_id} saved successfully.")
                
                except requests.RequestException as e:
                    logger.error(f"Failed to fetch image for invoice {invoice_id}: {e}")
        
        else:
            logger.info("No invoice data found in the response.")
    
    except requests.RequestException as e:
        logger.error(f"Failed to fetch invoices: {e}")


