from sdf_module import *

class AjioComInternalFeasibility(CommonModule):
    def get_category_url(self, url, depth, current_depth_level):
        page_url = []
        cat_url = []
        try:
            dom = self.get_page_content_hash(url)
            if dom["status_code"] != 200:
                raise Exception("No proper DOM found")
            parsed_tree = CommonModule.get_parsed_tree(dom, "lxml")
            if parsed_tree is None:
                raise Exception("Parsing failed")
            page_url = parsed_tree.xpath("//script[contains(.,'childDetails')]")
            page_url = page_url[0].text
            page_url =  page_url.split(";\r\n")[0]
            page_url = page_url.split("_PRELOADED_STATE__ = ")[1]
            page_url = json.loads(page_url)
            for node in page_url["navigation"]["data"]["childDetails"]:
                data = {}
                data["primary_category"] = node["name"]
                data["primary_category_url"] = "https://www.ajio.com" + node["url"]
                sub_node =  next((item for item in node["childDetails"] if item["name"] == "CATEGORIES"), None)
                sub_node = sub_node["childDetails"]
                for sub in sub_node:
                    sub_data = {} | data
                    sub_data["secondary_name"] = sub["name"]
                    sub_data["secondary_name_url"] = "https://www.ajio.com" + sub["url"]
                    cat_url.append(sub_data["secondary_name_url"] + "|" + json.dumps(sub_data))
        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # Fixed string concatenation issue
        return cat_url
    
    def get_pagination_url(self, url, depth, current_depth_level):
        pagination_url = []
        try:
            url,cat_data = url.split("|")
            dom = self.get_page_content_hash(url)
            if dom["status_code"] != 200:
                raise Exception("No proper DOM found")
            parsed_tree = CommonModule.get_parsed_tree(dom, "lxml")
            if parsed_tree is None:
                raise Exception("Parsing failed")
            parsed_tree = parsed_tree.xpath("//script[contains(.,'numberOfItems')]")[0].text
            total_product = parsed_tree.split("numberOfItems")[1]
            total_product = total_product.split(': "')[1].split('"')[0]
            total_product = int(total_product)
            pages = total_product / 45
            pages = math.ceil(pages)
            for i in range(pages):
                pagination_url.append(f"https://www.ajio.com/api/category/10?currentPage={i}&pageSize=45&format=json&query=%3Arelevance&curated=true&curatedid={url.split("/")[-1]}" + "|" + cat_data)
        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # Fixed string concatenation issue
        return pagination_url

    def get_product_url(self, url, depth, current_depth_level):
        product_url = []
        try:
            url,cat_data = url.split("|")
            dom = self.get_page_content_hash(url)
            if dom["status_code"] != 200:
                raise Exception("No proper DOM found")
            cat_data = json.loads(cat_data)
            page_doc = json.loads(dom["page_doc"])
            page_doc = page_doc["products"]
            i = 1
            for node in page_doc:
                data = {}
                data["rank"] = i
                i = i + 1
                data.update(cat_data)
                product_url.append("https://www.ajio.com" + node["url"] + "|" + json.dumps(data))
        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # Fixed string concatenation issue
        return product_url