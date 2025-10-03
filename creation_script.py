import os
import pandas as pd #type: ignore
import sys
import json
def print_status(status, file_name, project, site_name, info):
    status_message = {
        "status": status,
        "file_name": file_name,
        "project": project,
        "site_name": site_name,
        "info": info
    }
    json_message = json.dumps(status_message, indent=4)
    
    print(json_message)

def create_project_structure(base_path, project_name, site_name, py_content, yml_content):
    project_path = os.path.join(base_path, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print_status("created", project_path, project_name, site_name, "Directory created")

    py_file_path = os.path.join(project_path, f"{site_name}_{project_name}.py")
    yml_file_path = os.path.join(project_path, f"{site_name}_{project_name}.yml")

    with open(py_file_path, 'w') as py_file:
        py_file.write(py_content)
        print_status("created", py_file_path, project_name, site_name, "Python file created")

    with open(yml_file_path, 'w') as yml_file:
        yml_file.write(yml_content)
        print_status("created", yml_file_path, project_name, site_name, "YAML file created")

def create_text_file(base_path, project_name, site_name):
    project_path = os.path.join(base_path, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print_status("created", project_path, project_name, site_name, "Directory created")
        
    txt_file_path = os.path.join(project_path, f"{site_name}_{project_name}.txt")
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write("")
        print_status("created", txt_file_path, project_name, site_name, "Text file created")

def create_folder(base_path, project_name, site_name):
    project_path = os.path.join(base_path, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print_status("created", project_path, project_name, site_name, "Directory created")

    site_folder_path = os.path.join(project_path, f"{site_name}_{project_name}")
    if not os.path.exists(site_folder_path):
        os.makedirs(site_folder_path)
        print_status("created", site_folder_path, project_name, site_name, "Site folder created")

def create_excel_file(base_path, project_name, site_name):
    project_path = os.path.join(base_path, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print_status("created", project_path, project_name, site_name, "Directory created")

    excel_file_path = os.path.join(project_path, f"{site_name}_{project_name}.xlsx")
    df = pd.DataFrame()  # Empty DataFrame to create an empty Excel file
    df.to_excel(excel_file_path, index=False)
    print_status("created", excel_file_path, project_name, site_name, "Excel file created")

def main():
    if len(sys.argv) != 3:
        print("Usage: python automated_script.py <project_name> <site_name>")
        sys.exit(1)

    project_name = sys.argv[1]
    site_name = sys.argv[2]

    base_dir = os.getcwd()

    url_collector_path = os.path.join(base_dir, 'url_collector')
    url_fetcher_path = os.path.join(base_dir, 'url_fetcher')
    url_extractor_path = os.path.join(base_dir, 'url_data_extractor')
    scrape_output_path = os.path.join(base_dir, 'scrape_output')
    class_name_in_site_script = f"{site_name}_{project_name}"
    class_name_in_site_script = ''.join([word.capitalize() for word in class_name_in_site_script.split('_')])
    # Content for each file type
    collector_py_content = f"""from sdf_module import CommonModule

class {class_name_in_site_script}(CommonModule):
    def get_final_url(self, url, depth, current_depth_level):
        page_url = []
        try:
            dom = self.get_page_content_hash(url)
            if dom["status_code"] != 200:
                raise Exception("No proper DOM found")
            parsed_tree = self.get_parsed_tree(dom)
            if parsed_tree is None:
                raise Exception("Parsing failed")
            page_url = self.get_value_from_xpath(parsed_tree, "xpath", "all/first")
        except Exception as e:
            print(f"Exception occurred: "+ e)
        return page_url
    """
    collector_yml_content = """depth0:
  seed_url: ["",""]
  method_name: get_final_url
depth1:
  method_name: get_final_url"""
    
    fetcher_py_content = f"""from sdf_module import *
class {class_name_in_site_script}:
    def get_page_content(self, url, args_hash):
        page_content = CommonModule.get_page_content_hash(url, args_hash)
        return page_content
"""
    fetcher_yml_content = """request_type:
verification_xpath:
ingnore_cache_for_retries:
retry_attempt_per_url:"""
    
    extractor_py_content = f"""from sdf_module import CommonModule
from lxml import html #type: ignore
import json
class {class_name_in_site_script}:
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
"""
    extractor_yml_content = """---
domain: jbhifi.nz.com
fields:
  crawl_timestamp:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  uniq_id:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  page_url:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  product_name:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  price:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  size:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  colour:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  description:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  sku:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  fit:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  origin:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  manufacturer:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  is_parent:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  stock_status:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  variant_id:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  primary_category:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  primary_category_url:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  secondary_category:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  secondary_category_url:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  tertiary_category:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  tertiary_category_url:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
  product_rank:
    desc_of_xpath:
    standard_nodeset_range: first
    standard_nodeset_join_char: "|"
    standard_post_processing_functions: "remove_line_and_spaces"
"""
    
    create_project_structure(url_collector_path, project_name, site_name, collector_py_content, collector_yml_content)
    create_project_structure(url_fetcher_path, project_name, site_name, fetcher_py_content, fetcher_yml_content)
    create_project_structure(url_extractor_path, project_name, site_name, extractor_py_content, extractor_yml_content)

    scrape_collector_output = os.path.join(scrape_output_path, 'collector_output')
    scrape_fetcher_output = os.path.join(scrape_output_path, 'fetcher_output')
    scrape_extractor_output = os.path.join(scrape_output_path, 'extractor_output')

    create_text_file(scrape_collector_output, project_name, site_name)
    create_folder(scrape_fetcher_output, project_name, site_name)
    create_excel_file(scrape_extractor_output, project_name, site_name)

if __name__ == "__main__":
    main()