import os
import re
import csv
from pathlib import Path
from paddleocr import PaddleOCR
import multiprocessing as mp

root_folder = os.getcwd()
# imgs_folder = Path(root_folder) / "imgs"
imgs_folder = r"C:\Users\jlmunoz\OneDrive - Autoridad del Canal de Panama\Documents\tasks\2024\expats\imgs"
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory


def divide_list(original_list, n):
    sublists = []
    # Create empty sublists
    for i in range(0,n):
        sublists.append({})
    # Add elements to each sublist
    max_index = int(len(original_list) / n)
    for i in range(0, n):
        if i == n-1:
            sublists[i] = {"index": i, "data": original_list[(i*max_index):]}
        else:
            sublists[i] = {"index": i, "data": original_list[(i*max_index):max_index*(i+1)]}

    total = 0
    for i in range(0,n):
        print(len(sublists[i]['data']))
        total += len(sublists[i]['data'])
    print(total)
    return sublists

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

def validate_month(text):
    pass

def validate_year(text: str) -> str:
    pattern = re.compile(r"[0-9]{4}")
    if re.fullmatch(pattern, text):
        return text
    else:
        return ""

def get_name(text):
    pass

def validate_badge(text: str) -> str:
    pattern = re.compile(r"[0-9]{6}")
    if re.fullmatch(pattern, text):
        return text
    else:
        return ""

def get_department(text):
    pass

def header_extraction(imgs_files: list[str], ind: int):
    data = []
    files_errors = []
    error_headers = ["filename"]
    headers = ["id","file", "page","name","badge", "month","year","department"]
    counter = 1
    for img in imgs_files:
        words = []
        name = ""
        department = ""
        # if (counter >= 1) and (counter < 2000):
        full_img_path = Path(imgs_folder) / img
        print(f"Process: {ind} --- No. {counter} --- File: {full_img_path}")
        try:
            result = ocr.ocr(str(full_img_path))
            inner_result = result[0]
            # print(len(inner_result))
            for i in range(0,20):
                if "MES" in inner_result[i][1][0]:
                    month = inner_result[i+1][1][0]
                    year = inner_result[i+2][1][0]
                    year = validate_year(year)
                if  inner_result[i][1][0] == "LAST AND FIRST NAME":
                    name = inner_result[i+1][1][0]
                if "BADGE" in inner_result[i][1][0]:
                    badge = inner_result[i+1][1][0]
                    badge = validate_badge(badge)
                if "DEPARTMENT" in inner_result[i][1][0]:
                    department = inner_result[i+1][1][0]
                # print(inner_result[i][1][0])
        
            info = {
                "id": counter,
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
            files_errors.append({"filename": img})
                
        counter += 1
        
    # print_data(data)
    print_data(files_errors)
    root_folder = os.getcwd()
    errors_folder = Path(root_folder) / "errors"
    test_data_folder = Path(root_folder) / "test_data"
    save_csv(f"{test_data_folder}/{ind}_extracted_data_test.csv", headers, data)
    save_csv(f"{errors_folder}/{ind}_errors_files.txt", error_headers, files_errors)
    

def main():
    
    
    
    # Get contents of imgs folder
    imgs_files = os.listdir(imgs_folder)
    # Limit the quantity of files
    imgs_files = imgs_files[8001:10001]
    # for img in imgs_files:
    #     print(img)
     # for testing

    list_imgs_divided = divide_list(imgs_files, 14)
    folders = list_imgs_divided


    procs = []
    for item in folders:
        proc = mp.Process(target=header_extraction, args=(item['data'],item['index']))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    
    
    
    

if __name__ == "__main__":
    main()