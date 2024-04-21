import os

BASE_PATH =  os.path.abspath(__file__)
BASE_PATH =  os.path.dirname(BASE_PATH)
DATASET = os.path.join(BASE_PATH,'dataset')
MODERATE_DATASET = os.path.join(BASE_PATH,'dataset','test_moderate')
THICK_DATASET = os.path.join(BASE_PATH,'dataset','test_thick')
THIN_DATASET = os.path.join(BASE_PATH,'dataset','test_thin')
DEMO_DATASET = os.path.join(BASE_PATH,'dataset','input','001.png')


CSV_LOGGER_PATH  = os.path.join(BASE_PATH,'CSVs','training_res.csv')