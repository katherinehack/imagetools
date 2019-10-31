
import psycopg2
import psycopg2.extras
import sys, os, os.path
import csv, codecs
import datetime
from datetime import date
import sys, re, time
import subprocess
from subprocess import Popen, PIPE
import psycopg2
import osgeo, ogr
import fnmatch
import gdal


hd_name = 'ImgStore1'
#rootDir = 'K:\\NFI_images_ZN1\\RAW\\812131'
rootDir = r'D:\ORTHO\MB_2013_14_Submissions\ORTHO'
host = 'pgpfc1.nfis_org'
db_name = 'nfi'
user = 'khackett'
srid = '102001'
schema = 'khackett'
table_name = 'shape_102001'
db_table_name = schema + '.' + table_name
global image_type 
global image_year
global image_sensor 
global image_ref
global line_mdata


#Define our connection string
conn_string = "host='pgpfc1.nfis.org' dbname='nfi' user='khackett' password='n0vacancY'"
 
# print the connection string we will use to connect
print ('Connecting to database\n' + conn_string)
 
# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)
 
# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()
print ("Connected!\n")

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.smtxml'):
        print(file)



#define nfi_plot_sample_id
sample_id = ("SELECT distinct nfi_plot_sample_id FROM nfi_plot_ts.nfi_plot_sample a "
             "WHERE a.layer = 'LC' and a.meas_id = 1 and a.nfi_plot = {0}")

#insert base query fro the table nfi_plot_image
def insert_info(nfi_plot_sample_id,image_type,image_date,image_sensor,image_ref,geometry,thumbnail):
    ins_img_inf = ("INSERT INTO " + user + ".nfi_plot_image(nfi_plot_sample_id,image_type_code,image_date,image_sensor_code,image_ref,geom,thumbnail) "
                                 "VALUES({0},'{1}',{2},'{3}','{4}',{5},'{6}') ")

    #ins_img_inf = ("INSERT INTO vsotskov.nfi_plot_image(nfi_plot_sample_id,image_type_code,image_year,image_sensor_code,image_ref,geom) "
    #                             "SELECT({0},'{1}',{2},'{3}','{4}',ST_Transform(b.geom,102001) as geom from vsotskov.shape_4326 b ")

    existing_row = ("SELECT * FROM khackett.nfi_plot_image a WHERE a.nfi_plot_sample_id = {0} and a.image_type_code = {1}  and a.image_date = {2} and a.image_sensor_code = {3}  ")
    existing_row_new = existing_row.format(nfi_plot_sample_id,'\'' + image_type + '\'','\'' + image_date + '\'','\'' + image_sensor + '\'')
    cursor.execute(existing_row_new)
    rowcount = cursor.rowcount
    
    print('rowcount = ' + str(rowcount))
    if rowcount == 0:
        geometry = geometry.split(')')[0]
        ins_img_inf_new = ins_img_inf.format(nfi_plot_sample_id,image_type,'\'' + image_date + '\'',image_sensor,image_ref,geometry,thumbnail)
        print('insert statement: ' + ins_img_inf_new)
        print('################################################################')
        cursor.execute(ins_img_inf_new)
        conn.commit()


count_imd = 0
for path, dirs, files in os.walk(rootDir):
    
    #print (dirs)
    for nfi_plot in dirs:
        print('######################################')
        #if nfi_plot == '661591':
        #   next(nfi_plot)


        print('NFI plot = ' + str(nfi_plot))
        for dirName, subdirList, fileList in os.walk(rootDir + '\\' + nfi_plot):
            for fname in fileList:
                f_array = fname.split(".")
                if len(f_array) == 2:
                    f_array = fname.split(".")
                    f_array_shp = f_array[0].split("_")
                    d_array = dirName.split("\\")

                    #thumb_name = 'thumb'
                    #thumb_ref = dirName + '\\' + thumb_name
                    #print(thumb_ref)

                    #print('Thumbnail ref: ' + thumb_ref)
                    thumb_store_dir = 'D:\ORTHO\MB_2013_14_Submissions\ORTHO' + '\\' + str(nfi_plot) + '\\'
                        
                    thum_store_ref = thumb_store_dir + 'Auxiliary'
                    print(thum_store_ref)
                    #thum_store_db = 'D:\ORTHO\MB_2013_14_Submissions\ORTHO' + '/' + str(nfi_plot)
                    #print('thum_store_db:' + thum_store_db)
                    #thum_store_db_file = thum_store_db + '/' + thumb_name
                    thum_folder_cmd = 'if not exist ' + thum_store_ref + ' mkdir ' + thum_store_ref
                    #print(thum_folder_cmd)

                    #do thumb folder!
                    process = subprocess.Popen(thum_folder_cmd, shell=True)
                    process.wait()
                        
                    
                    
