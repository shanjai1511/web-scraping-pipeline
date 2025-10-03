from sdf_module import CommonModule
from lxml import html #type: ignore
import json
from datetime import datetime
import traceback
import pytz #type: ignore

class StyleunionComInternalFeasibility:

    @staticmethod
    def modify_page_doc(inhash, page_doc):
        """
        Site-specific logic for modifying the page_doc.
        For example, removing unwanted tags, cleaning content, etc.
        """
        final_data = []
        try:
            url,category = str(inhash).split("|")
            data = {}
            category = eval(category)
            page_json = page_doc.xpath("//script[contains(@class,'product-json')]")
            page_json = page_json[0].text
            page_json = json.loads(page_json)
            data["product_name"] = page_json.get("title")
            data["page_url"] = url
            data["inhash"] = str(inhash)
            data.update(category)
            description = page_json.get("description")
            if not description == '':
                description = html.fromstring(description)
                description = description.xpath("//text()")
                description = [item.strip() for item in description if item.strip()]
                description =  " ".join(description) 
                data["description"] = description
            star_ratings = page_doc.xpath("//span[contains(@class,'badge__stars')]/@aria-label")
            star_ratings = star_ratings[0]
            star_ratings = star_ratings.split(" ")[0]
            star_ratings = float(star_ratings)
            data["star_ratings"] = star_ratings
            reviews_count = page_doc.xpath("//span[contains(@class,'badge__text')]")
            reviews_count = reviews_count[0].text.strip().split(" ")[0]
            data["reviews_count"] = 0
            if reviews_count and not reviews_count == 'No':
                data["reviews_count"] = int(reviews_count)

            origin = page_doc.xpath("//span[contains(@class,'metafield-multi_line_text_field')]")
            origin = origin[0].text
            origin = origin.split("Made in ")[-1].split("\n")[0]
            data["origin"] = origin

            fit = page_doc.xpath("//p[contains(.,'Style')]/span[contains(@class,'swatches')]")
            if fit:
                fit = fit[0].text
                fit = fit.strip()
                data["fit"] = fit
            variant_id = []
            for node in page_json.get("variants"):
                variant_id.append(node.get("id"))
            data["variant_products_id_list"] = variant_id
            data["parent_id"] = variant_id[0]
            parent = True

            for node in page_json.get("variants"):
                variant_data = {}
                variant_data["variant_id"] = node.get("id")
                variant_data["sku"] = node.get("sku")
                variant_data["is_parent"] = False
                variant_data.update(data)
                variant_data["is_variant"] = True
                if parent and node.get("available"):
                    variant_data["is_parent"] = True
                    variant_data["is_variant"] = False
                    parent = False
                variant_data["size"] = node.get("option1") if node else next
                variant_data["color"] = node.get("option2")
                variant_data["stock_status"] = node.get("available")
                variant_data["sku"] = node.get("sku")
                variant_data["list_price"] = node.get("price")/100
                variant_data["selling_price"] = node.get("price")/100
                discount_percentage = ((variant_data["list_price"] - variant_data["selling_price"])/variant_data["list_price"]) * 100
                
                variant_data["discount_percentage"] = int(discount_percentage)
                
                final_data.append(variant_data)
        except Exception as e:
            print(f"Exception occurred: {e}")
            import pdb; pdb.set_trace()
        return final_data

    @staticmethod
    def get_crawl_timestamp(page_doc, inhash):
        current_datetime = datetime.now()
        # Format the date and time in the desired format
        formatted_datetime = current_datetime.strftime("%b %d, %Y @ %H:%M:%S.%f")[:-3]
        return formatted_datetime

    @staticmethod
    def get_uniq_id(page_doc, inhash):
        return CommonModule.encode(f"{page_doc.get("inhash")}|{page_doc.get("sku")}|{page_doc.get("size")}|{page_doc.get("color")}")

    @staticmethod
    def get_page_url(page_doc, inhash):
        value = page_doc.get("page_url")
        return value

    @staticmethod
    def get_product_name(page_doc, inhash):
        value = page_doc.get("product_name")
        return value

    @staticmethod
    def get_list_price(page_doc, inhash):
        value = page_doc.get("list_price")
        return value
    
    @staticmethod
    def get_selling_price(page_doc, inhash):
        value = page_doc.get("selling_price")
        return value
    
    @staticmethod
    def get_discount_percentage(page_doc, inhash):
        value = page_doc.get("discount_percentage")
        return value
    
    @staticmethod
    def get_size(page_doc, inhash):
        value = page_doc.get("size")
        return value
    
    @staticmethod
    def get_colour(page_doc, inhash):
        value = page_doc.get("color")
        return value
    
    @staticmethod
    def get_description(page_doc, inhash):
        value = page_doc.get("description")
        return value
    
    @staticmethod
    def get_sku(page_doc, inhash):
        value = page_doc.get("sku")
        return value
    
    @staticmethod
    def get_fit(page_doc, inhash):
        value = page_doc.get("fit")
        return value
    
    @staticmethod
    def get_origin(page_doc, inhash):
        value = page_doc.get("origin")
        return value
    
    @staticmethod
    def get_manufacturer(page_doc, inhash):
        value = page_doc.get("manufacturer")
        return value
    
    @staticmethod
    def get_is_parent(page_doc, inhash):
        value = page_doc.get("is_parent")
        return value
    
    @staticmethod
    def get_stock_status(page_doc, inhash):
        value = page_doc.get("stock_status")
        return value
    
    @staticmethod
    def get_variant_id(page_doc, inhash):
        value = page_doc.get("variant_id")
        return value
    
    @staticmethod
    def get_primary_category(page_doc, inhash):
        value = page_doc.get("primary_category")
        return value
    
    @staticmethod
    def get_primary_category_url(page_doc, inhash):
        value = page_doc.get("primary_category_url")
        return value
    
    @staticmethod
    def get_secondary_category(page_doc, inhash):
        value = page_doc.get("secondary_categroy")
        return value
    
    @staticmethod
    def get_secondary_category_url(page_doc, inhash):
        value = page_doc.get("secondary_category_url")
        return value
    
    @staticmethod
    def get_tertiary_category(page_doc, inhash):
        value = page_doc.get("tertiary_category")
        return value
    
    @staticmethod
    def get_tertiary_category_url(page_doc, inhash):
        value = page_doc.get("tertiary_category_url")
        return value
    
    @staticmethod
    def get_product_rank(page_doc, inhash):
        value = page_doc.get("rank")
        return value
    
    @staticmethod
    def get_star_rating(page_doc, inhash):
        value = page_doc.get("star_ratings")
        return value
    
    @staticmethod
    def get_reviews_count(page_doc, inhash):
        value = page_doc.get("reviews_count")
        return value