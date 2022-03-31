import urllib.request
import urllib
import pandas as pd
import pathlib
import os

thisfile = pathlib.Path(__file__).parent.resolve()
print(thisfile)
# *******************************************************************************
# Get_qcew_data : This function takes a raw csv string and splits it into
# a two-dimensional array containing the data and the header row of the csv file
# a try/except block is used to handle for both binary and char encoding
def Get_qcew_data(csv):
    dataRows = []
    try: 
        dataLines = csv.decode().split('\r\n')
    except: 
        dataLines = csv.split('\r\n')
    
    for row in dataLines:
        dataRows.append(row.replace("\"", "").split(','))
    
    df = pd.DataFrame(data = dataRows[1:], columns = dataRows[0]).dropna()
    
    #using the QCEW Field Layouts we've determined which fields are numeric
    numeric_cols = ["qtrly_estabs", "month1_emplvl", "month2_emplvl", "month3_emplvl",
                    "total_qtrly_wages", "taxable_qtrly_wages", "qtrly_contributions",
                    "avg_wkly_wage", "lq_qtrly_estabs", "lq_month1_emplvl", 
                    "lq_month2_emplvl", "lq_month3_emplvl", "lq_total_qtrly_wages",
                    "lq_taxable_qtrly_wages", "lq_qtrly_contributions", "lq_avg_wkly_wage", 
                    "oty_qtrly_estabs_chg", "oty_qtrly_estabs_pct_chg", "oty_month1_emplvl_chg",
                    "oty_month1_emplvl_pct_chg", "oty_month2_emplvl_chg", "oty_month2_emplvl_pct_chg", 
                    "oty_month3_emplvl_chg", "oty_month3_emplvl_pct_chg", "oty_total_qtrly_wages_chg", 
                    "oty_total_qtrly_wages_pct_chg", "oty_taxable_qtrly_wages_chg", 
                    "oty_taxable_qtrly_wages_pct_chg", "oty_qtrly_contributions_chg", 
                    "oty_qtrly_contributions_pct_chg", "oty_avg_wkly_wage_chg", "oty_avg_wkly_wage_pct_chg"]
    df[numeric_cols] = df[numeric_cols].astype(float)
    return df
# *******************************************************************************

# *******************************************************************************
# qcewGetAreaData : This function takes a year, quarter, and area argument and
# returns an array containing the associated area data. Use 'a' for annual
# averages. 
# For all area codes and titles see:
# http://www.bls.gov/cew/doc/titles/area/area_titles.htm
#
def qcewGetAreaData(year, qtr, area):
    urlPath = f"http://data.bls.gov/cew/data/api/{year}/{qtr}/area/{area.upper()}.csv"
    httpStream = urllib.request.urlopen(urlPath)
    csv = httpStream.read()
    httpStream.close()
    return Get_qcew_data(csv)
# *******************************************************************************

# *******************************************************************************
# qcewGetIndustryData : This function takes a year, quarter, and industry code
# and returns an array containing the associated industry data. Use 'a' for 
# annual averages. Some industry codes contain hyphens. The CSV files use
# underscores instead of hyphens. So 31-33 becomes 31_33. 
# For all industry codes and titles see:
# http://www.bls.gov/cew/doc/titles/industry/industry_titles.htm
#
def qcewGetIndustryData(year, qtr, industry):
    urlPath = f"http://data.bls.gov/cew/data/api/{year}/{qtr}/industry/{industry}.csv"
    httpStream = urllib.request.urlopen(urlPath)
    csv = httpStream.read()
    httpStream.close()
    return Get_qcew_data(csv)
# *******************************************************************************

# *******************************************************************************
# qcewGetSizeData : This function takes a year and establishment size class code
# and returns an array containing the associated size data. Size data
# is only available for the first quarter of each year.
# For all establishment size classes and titles see:
# http://www.bls.gov/cew/doc/titles/size/size_titles.htm
#
def qcewGetSizeData(year,size):
    urlPath = f"http://data.bls.gov/cew/data/api/{year}/1/size/{size}.csv"
    httpStream = urllib.request.urlopen(urlPath)
    csv = httpStream.read()
    httpStream.close()
    return Get_qcew_data(csv)
# *******************************************************************************

def Download_InformativeFiles():
    layout_url = "https://www.bls.gov/cew/about-data/downloadable-file-layouts/quarterly/naics-based-quarterly-layout-csv.csv"
    size_url = "https://www.bls.gov/cew/classifications/size/size-titles-csv.csv"
    industries_url = "https://www.bls.gov/cew/classifications/industry/industry-titles-csv.csv"
    aggregations_url = "https://www.bls.gov/cew/classifications/aggregation/agg-level-titles-csv.csv"
    
    files = [(layout_url, 'layout.csv'), (size_url, 'size.csv'), (industries_url, 'industries.csv'), (aggregations_url, 'aggregations.csv')]
    for url, filename in files:
        response = urllib.request.urlopen(url)  
        file = open(os.path.join(thisfile, filename), 'wb')
        file.write(response.read())
        file.close()
        
if __name__ == '__main__':
    Download_InformativeFiles()
    Maryland_Data = qcewGetAreaData(2015,1, "24000")
    Auto_Manufacturing = qcewGetIndustryData(2015, 1, "3361")
    SizeData = qcewGetSizeData(2015, 6)

    '''
    Comments:
    - pull data for 10 states for 1 year
    - build db schema
    - move data and load into db 
    '''
