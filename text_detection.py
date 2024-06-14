import os
import re
import csv
from pathlib import Path
from paddleocr import PaddleOCR

def save_csv(filename: str, headers: list[str], data: list[dict]) -> None:
    with open(filename, 'w', encoding="utf-8",newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        print(f"CSV file {filename} was generated successfully...")

def print_data(data: list[dict]) -> None:
    for item in data:
        print(item)
        
def get_page(text):
    pattern = re.compile(r"page_[0-9]+")
    result = pattern.findall(text)
    return int(result[0][5:])

def get_month(text):
    pass

def get_year(text):
    pattern = re.compile(r"[0-9]{4}")
    result = pattern.findall(text)
    return int(result[0])

def get_name(text):
    pass

def get_badge(text):
    pass

def get_department(text):
    pass
    

def main():
    ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
    data = []
    files_errors = []
    headers = ["file", "page","name","badge", "month","year","department"]
    root_folder = os.getcwd()
    imgs_folder = Path(root_folder) / "imgs"
    # Get contents of imgs folder
    imgs_files = os.listdir(imgs_folder)
    counter = 1 # for testing
    for img in imgs_files:
        words = []
        name = ""
        department = ""
        if counter < 1001:
            full_img_path = Path(imgs_folder) / img
            print(f"No. {counter} --- File: {full_img_path}")
            try:
                result = ocr.ocr(str(full_img_path))
                inner_result = result[0]
                # print(len(inner_result))
                for i in range(0,20):
                    if "MES" in inner_result[i][1][0]:
                        month = inner_result[i+1][1][0]
                        year = inner_result[i+2][1][0]
                    if  inner_result[i][1][0] == "LAST AND FIRST NAME":
                        name = inner_result[i+1][1][0]
                    if "BADGE" in inner_result[i][1][0]:
                        badge = inner_result[i+1][1][0]
                    if "DEPARTMENT" in inner_result[i][1][0]:
                        department = inner_result[i+1][1][0]
                    # print(inner_result[i][1][0])
            
                info = {
                    "file": img,
                    "page": get_page(img),
                    "name": name,
                    "badge": badge,
                    "month": month,
                    "year": year,
                    "department": department,
                    
                }
                data.append(info)
            except:
                files_errors.append(img)
                
            counter += 1
        
    # print_data(data)
    print_data(files_errors)
    save_csv("extracted_data.csv", headers, data)
    
    
    

if __name__ == "__main__":
    main()