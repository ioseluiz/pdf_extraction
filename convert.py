import os
import pymupdf
import multiprocessing as mp
from pathlib import  Path
from pdf2image import convert_from_path

poppler_path = r"C:\Users\User\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin"
target_folder = r"C:\Users\User\Documents\data_projects\expats_project\imgs"
pdfs_folder = r"C:\Users\User\Documents\data_projects\expats_project\pdfs"

class TimeSheet():
    def __init__(self, file: str, page: int):
        self.file = file
        self.page = page
        
def divide_list(original_list, n):
    sublists = []
    # Create empty sublists
    for i in range(0, n):
        sublists.append({})
    # Add elements to each sublist
    max_index = int(len(original_list) / n)
    for i in range(0, n):
        if i == n-1:
            sublists[i] = {'index': i, 'data': original_list[(i*max_index):]}
        else:
            sublists[i] = {'index': i, 'data': original_list[(i*max_index):max_index*(i+1)]}
    total = 0
    for i in range(0,n):
        print(len(sublists[i]['data']))
        total += len(sublists[i]['data'])
    print(total)
    return sublists

def convert_images(list_files: list[str]):
    for file in list_files:
        pdf_fullname = Path(pdfs_folder) / file
        detect_time_sheet(pdf_fullname, file)
    

def detect_time_sheet(file_fullname: str, filename:str):
    doc = pymupdf.open(file_fullname) #open pdf file
    counter = 1
    for page in doc:
        text = page.get_text().encode("utf-")
        if "TIME SHEET" in text.decode("utf-8"):
            # convert to image and save
            print(f"file: {filename} and page {counter}")
            pdf_file = convert_from_path(file_fullname, poppler_path=poppler_path)
            for i in range(len(pdf_file)):
                if i == counter-1:
                    pdf_file[i].save(f"{target_folder}/{filename[:-4]}_page_{str(i)}.jpg", 'JPEG')
        counter += 1

def main():
    
    
    pdf_files = os.listdir(pdfs_folder)
    divided_list = divide_list(pdf_files, 16)
    nprocs = mp.cpu_count()
    print(f"Number of CPU cores: {nprocs}")
    procs = []
    for item in divided_list:
        proc = mp.Process(target=convert_images, args=(item['data'],))
        procs.append(proc)
        proc.start()
        
    for proc in procs:
        proc.join()
    
    

if __name__ == "__main__":
    main()