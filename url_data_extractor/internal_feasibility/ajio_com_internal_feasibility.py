from sdf_module import CommonModule
from lxml import html #type: ignore
import json
class AjioComInternalFeasibility:
     @staticmethod
    def modify_page_doc(inhash, page_doc):
        final_data = []
        try:
            url,category = str(inhash).split("|")
        except Exception as e:
            print(f"Exception occurred: " + e)
        return final_data

    @staticmethod
    def get_crawl_timestamp(page_doc, inhash):
        return CommonModule.get_current_timestamp()

    @staticmethod
    def get_uniq_id(page_doc, inhash):
        return CommonModule.encode(inhash['url'])

    @staticmethod
    def get_page_url(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None

    @staticmethod
    def get_product_name(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None

    @staticmethod
    def get_price(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_size(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_colour(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_description(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_sku(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_fit(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_origin(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_manufacturer(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_is_parent(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_stock_status(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_variant_id(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_primary_category(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_primary_category_url(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_secondary_category(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_secondary_category_url(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_tertiary_category(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_tertiary_category_url(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
    
    @staticmethod
    def get_product_rank(page_doc, inhash):
        value = page_doc.xpath("xpath")
        return value if value else None
