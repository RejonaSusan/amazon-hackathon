import re
import os
import pandas as pd
import multiprocessing
import time
import urllib
from PIL import Image
from pathlib import Path
from functools import partial
from tqdm import tqdm
import constants

def common_mistake(unit):
    if unit in constants.allowed_units:
        return unit
    if unit.replace('ter', 'tre') in constants.allowed_units:
        return unit.replace('ter', 'tre')
    if unit.replace('feet', 'foot') in constants.allowed_units:
        return unit.replace('feet', 'foot')
    return unit

def parse_string(s):
    s_stripped = "" if s is None or str(s) == 'nan' else s.strip()
    if s_stripped == "":
        return None, None
    pattern = re.compile(r'^-?\d+(\.\d+)?\s+[a-zA-Z\s]+$')
    if not pattern.match(s_stripped):
        raise ValueError("Invalid format in {}".format(s))
    parts = s_stripped.split(maxsplit=1)
    number = float(parts[0])
    unit = common_mistake(parts[1])
    if unit not in constants.allowed_units:
        raise ValueError("Invalid unit [{}] found in {}. Allowed units: {}".format(
            unit, s, constants.allowed_units))
    return number, unit

def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        return

def sanitize_filename(filename):
    # Replace any characters not allowed in filenames with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_image(image_info, save_folder, retries=3, delay=3):
    image_link, entity_name, grp_id = image_info
    if not isinstance(image_link, str) or not isinstance(entity_name, str) or not isinstance(grp_id, str):
        return

    # Sanitize the entity name and group ID to be used as a filename
    filename = f"{sanitize_filename(grp_id)}_{sanitize_filename(entity_name)}.jpg"
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for _ in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except:
            time.sleep(delay)
    
    create_placeholder_image(image_save_path) # Create a black placeholder image for invalid links/images

def download_images(image_infos, download_folder, allow_multiprocessing=True):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if allow_multiprocessing:
        download_image_partial = partial(
            download_image, save_folder=download_folder, retries=3, delay=3)

        with multiprocessing.Pool(64) as pool:
            list(tqdm(pool.imap(download_image_partial, image_infos), total=len(image_infos)))
            pool.close()
            pool.join()
    else:
        for image_info in tqdm(image_infos, total=len(image_infos)):
            download_image(image_info, save_folder=download_folder, retries=3, delay=3)

def get_image_links_entities_and_group_ids_from_csv(csv_file_path, url_column_name, entity_column_name, grp_id_column_name):
    df = pd.read_csv(csv_file_path)
    image_infos = df[[url_column_name, entity_column_name, grp_id_column_name]].dropna()
    return image_infos.values.tolist()

if __name__ == '__main__':
    csv_file_path = os.path.join("../dataset", "train.csv")
    url_column_name = 'image_link'  
    entity_column_name = 'entity_name'  # Column containing the entity names
    grp_id_column_name = 'group_id'  # Column containing the group IDs
    download_folder = os.path.join("../dataset", "imgs")

    # Fetch image links, entities, and group IDs, and download images
    image_infos = get_image_links_entities_and_group_ids_from_csv(csv_file_path, url_column_name, entity_column_name, grp_id_column_name)
    download_images(image_infos, download_folder, allow_multiprocessing=True)
