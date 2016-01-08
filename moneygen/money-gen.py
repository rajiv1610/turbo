'''
USE AT YOUR OWN PERIL
'''

from BeautifulSoup import BeautifulSoup
import urllib
import sys
import argparse
import pprint
import xlsxwriter
from datetime import datetime

'''
parser = argparse.ArgumentParser()
parser.add_argument("sticker", action="store", nargs='?')
options = parser.parse_args()

sticker = options.sticker
'''

stock_meta = []

def populateStickers(page, worksheet, startRow):
    sock = urllib.urlopen(page)
    htmlSource = sock.read()
    sock.close()

    soup = BeautifulSoup(htmlSource)
    #print soup('table')[0].prettify()

    sTable = soup.find("div",{"id":"ctl00_cph1_pnl1"}).find("div",{"id":"ctl00_cph1_divSymbols"}).find("table",{"class":"quotes"})
    #print sTable
    headerDone = 0
    r = startRow  # index to worksheet row
    for row in sTable.findAll('tr'):
        if headerDone is 0:
            ths = row('th')
            c = 0
            for th in ths:
                worksheet.write(0, c, th.string)
                c += 1
            headerDone = 1
        else:
            tds = row('td')
            c = 0
            sticker = "TBD"
            foundAnalystReview = False
            for td in tds:
                if c is 0:
                    sticker = td.a.string
                    # Get analyst review info for this sticker
                    if populateAnalystReview(sticker, worksheet, r):
                        worksheet.write(r, c, td.a.string)
                        foundAnalystReview = True
                    else:
                        # No analyst reviews found, skip this sticker
                        break
                else:
                    worksheet.write(r, c, td.string)
                c += 1
            if foundAnalystReview:
                r += 1
    return r
 
# returns true if analyst review was found, false otherwise
def populateAnalystReview(sticker, worksheet, wRow):
    sock = urllib.urlopen("http://www.marketwatch.com/investing/stock/" + sticker + "/analystestimates")
    htmlSource = sock.read()
    sock.close() 

    soup = BeautifulSoup(htmlSource)
    #print soup('table')[0].prettify()

    keyVal = {}
    c = 9
    snapshotTable = soup.find("table",{"class":"snapshot"})
    if snapshotTable is None:
        #print "No snapshot found for ", sticker
        return False
    for row in snapshotTable.findAll('tr'):
        tds = row('td')
        key = "key"
        isKey = 1
        for td in tds:
            if td.string is not None:
                if isKey:
                    # Remember the key
                    key = td.string.strip()
                    isKey = 0
                else:
                    # Assign value
                    keyVal[key] = td.string.strip()
                    worksheet.write(wRow, c, td.string.strip())
                    if len(stock_meta) == (c - 9):
                        stock_meta.append(key)
                    c += 1
                    isKey = 1

    print (keyVal["Average Recommendation:"] + " " + sticker)
    '''
    print "==========================="
    print keyVal["Average Recommendation:"]
    print "==========================="
    pprint.pprint(keyVal)
    print "==========================="
    '''
    return True


workbook = xlsxwriter.Workbook('all_stocks_analyst-' + datetime.now().strftime("%Y%m%d-%H%M%S") + ".xlsx")
worksheet = workbook.add_worksheet()
startRow = 1

from string import ascii_uppercase
for Ch in ascii_uppercase:
    startRow = populateStickers("http://eoddata.com/stocklist/NASDAQ/" + Ch + ".htm", worksheet, startRow)

meta_c = 9
for meta in stock_meta:
    worksheet.write(0, meta_c, meta)
    meta_c += 1

workbook.close()
