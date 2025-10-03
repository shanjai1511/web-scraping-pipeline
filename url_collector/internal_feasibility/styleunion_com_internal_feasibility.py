from sdf_module import CommonModule
from lxml import html #type: ignore
import math
class StyleunionComInternalFeasibility(CommonModule):
    def get_category_url(self, url, depth, current_depth_level):
        page_url = []
        try:
            dom = self.get_page_content_hash(url)
            if dom["status_code"] != 200:
                raise Exception("No proper DOM found")
            parsed_tree = html.fromstring(dom["page_doc"])
            if parsed_tree is None:
                raise Exception("Parsing failed")
            cat_dom = parsed_tree.xpath("//li[contains(@class,'navigation__menuitem')]")
            for cat in cat_dom:
                data = {}
                primary_category = cat.xpath(".//a[contains(@class, 'navigation')]")[0].text
                primary_category = primary_category.strip()
                data["primary_category"] = primary_category

                url_key = cat.xpath(".//@href")[0]
                primary_category_url = f"https://styleunion.in{url_key}"
                data["primary_category_url"] = primary_category_url
                
                sub_cat_node = cat.xpath(".//*[contains(@class,'navigation__menulink--icon')]")
                if sub_cat_node:
                    sub_cat_dom = cat.xpath(f".//ul[contains(@aria-label,'{primary_category}')]/li[contains(@class,'dropdown__menuitem')]")
                    for sub_cat in sub_cat_dom:
                        sub_data = {}
                        secondary_category = sub_cat.xpath(".//text()")
                        secondary_category =  [item.strip() for item in secondary_category if item.strip()]
                        sub_data["secondary_categroy"] = secondary_category[0]

                        secondary_category_url = sub_cat.xpath(".//@href")
                        secondary_category_url = f"https://styleunion.in{secondary_category_url[0]}"
                        sub_data["secondary_category_url"] = secondary_category_url
                        sub_data.update(data)
                        inner_cat_node = sub_cat.xpath(".//ul[contains(@class,'dropdown dropdown--nested js-dropdown-nested')]")
                        if inner_cat_node:
                            inner_cat = sub_cat.xpath(".//li[contains(@class,'dropdown__menuitem')]")
                            for inner in inner_cat:
                                inner_data = {}
                                inner_category = inner.xpath(".//text()")
                                inner_category = [item.strip() for item in inner_category if item.strip()]
                                inner_data["inner_category"] = inner_category[0]

                                inner_category_url = inner.xpath(".//@href")
                                inner_category_url = f"https://styleunion.in{inner_category_url[0]}"
                                inner_data["inner_category_url"] = inner_category_url
                                inner_data.update(sub_data)
                                page_url.append(f"{inner_category_url}|{inner_data}")
                        else:
                            page_url.append(f"{secondary_category_url}|{sub_data}")
                else:
                    page_url.append(f"{primary_category_url}|{data}")
        except Exception as e:
            print(f"Exception occurred: {e}")
        return page_url
    
    def  get_pagination_url(self, keyurl, depth, current_depth_level):
        pagination_url = []
        try:
            url, category = keyurl.split("|")
            dom = self.get_page_content_hash(url)
            if dom["status_code"] != 200:
                raise Exception("No proper DOM found")
            parsed_tree = html.fromstring(dom["page_doc"])
            if parsed_tree is None:
                raise Exception("Parsing failed")
            product_count = parsed_tree.xpath("//script[contains(.,'productCount')]")
            product_count = product_count[0].text
            product_count = product_count.split("productCount: '")[-1].split("'")[0]
            product_count = math.ceil(int(product_count)/12)
            if product_count > 1:
                for page in range(1,product_count):
                    pagination_url.append(f"{url}?page={page}|{category}")
            else:
                return [keyurl]
        except Exception as e:
            print(f"Exception occurred: {e}")
        return pagination_url

    def get_product_url(self, url, depth, current_depth_level):
        product_url = []
        try:
            url, category = url.split("|")
            url = url.replace("-page","")
            dom = self.get_page_content_hash(url)
            if dom["status_code"] != 200:
                raise Exception("No proper DOM found")
            parsed_tree = html.fromstring(dom["page_doc"])
            if parsed_tree is None:
                raise Exception("Parsing failed")
            url_dom = parsed_tree.xpath("//div[contains(@id, 'product-listing')]")
            rank = 1
            category = eval(category)
            for prod in url_dom:
                category["rank"] = rank
                rank = rank + 1
                tag = prod.xpath(".//div[@class='new icn']")
                if tag:
                    category["product_tags"] = tag[0].text
                url_key = prod.xpath(".//a/@href")
                product_url.append(f"https://styleunion.in/{url_key[0]}|{category}")
        except Exception as e:
            print(f"Exception occurred: {e}")
        return product_url