#example of using cenusdata

'''
As a first example, let’s suppose we’re interested in unemployment
and high school dropout rates for block groups in Cook County, Illinois, which contains Chicago, IL.
'''

# setting pandas n censusdta and setting display options 
import pandas as pd
import censusdata

def main():
    

    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.precision', 2)



    #to download we must identify the tables containing the variables interest to us.
    #use ACS documentation, in particular Table Shells (https://www.census.gov/programs-surveys/acs/technical-documentation/summary-file-documentation.html)
    #can use cenusdata.search to find given text patterns. We can limit the output to the relevenant variables

    censusdata.search('acs5', 2015, 'label', 'unemploy')[160:170]
    censusdata.search('acs5', 2015, 'concept', 'education')[730:790]



    #using censusdata.printtable to show vars in table

    censusdata.printtable(censusdata.censustable('acs5', 2015, 'B23025'))
    censusdata.printtable(censusdata.censustable('acs5', 2015, 'B15003'))



    #after getting relevant variables, we need to identify the geographies.
    #we are going to get block groups in Cook County IL
    #1. look for FIPS code
    #2. find identifiers for all counties within IL to find Cook

    #1
    #print(censusdata.geographies(censusdata.censusgeo([('state','*')]), 'acs5', 2015)) #IL is 17

    #2
    #print(censusdata.geographies(censusdata.censusgeo([('state','17'), ('county', '*')]), 'acs5', 2015)) #cook is 031




    #once we have identified variables and geos of interest,
    #we can download the data using censusdata.download. compute variables for the percent unemployed and the percent w no hs degree

    cook_cnty = censusdata.download('acs5', 2015, censusdata.censusgeo([('state','17'), ('county','031'), ('block group','*')]), ['B23025_003E', 'B23025_005E', 'B15003_001E', 'B15003_002E', 'B15003_003E','B15003_004E', 'B15003_005E', 'B15003_006E', 'B15003_007E', 'B15003_008E','B15003_009E', 'B15003_010E', 'B15003_011E', 'B15003_012E', 'B15003_013E','B15003_014E', 'B15003_015E', 'B15003_016E'])
    cook_cnty['percent_unemployed'] = cook_cnty.B23025_005E / cook_cnty.B23025_003E * 100

    cook_cnty['percent_nohs'] = (cook_cnty.B15003_002E + cook_cnty.B15003_003E + cook_cnty.B15003_004E + cook_cnty.B15003_005E + cook_cnty.B15003_006E + cook_cnty.B15003_007E + cook_cnty.B15003_008E + cook_cnty.B15003_009E + cook_cnty.B15003_010E + cook_cnty.B15003_011E + cook_cnty.B15003_012E + cook_cnty.B15003_013E + cook_cnty.B15003_014E + cook_cnty.B15003_015E + cook_cnty.B15003_016E) / cook_cnty.B15003_001E * 100



    cook_cnty = cook_cnty[['percent_unemployed', 'percent_nohs']]
    print(cook_cnty.describe())


    #to show the 30 block groups in cook w highest rate of unemployment and the percent w no hs degree
    print(cook_cnty.sort_values('percent_unemployed', ascending=False).head(30))

    #show correlation
    print(cook_cnty.corr())

    censusdata.exportcsv('cook_data.csv', cook_cnty)
main()



