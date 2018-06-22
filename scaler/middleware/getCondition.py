import pandas as pd
import datetime
from datetime import date
from datetime import timedelta
import re
import time

#url = "https://www.wunderground.com/history/airport/KSNA/"
#req_city = "req_city=irvine"
#req_state = "req_state=CA"
#req_statename = "req_statename=California"
#reqdb_zip = "reqdb.zip=92612"
#req = '&'.join([req_city, req_state, req_statename, reqdb_zip])
#time = date.today().strftime("%Y/%m/%d")
#tmp = '/'.join([url, str(time), 'DailyHistory.html?' + req])
#tables = pd.read_html(tmp)
#res = tables[-1].values
#res = res[-1]
#res = res[4]
#pressure = float(re.findall(r"\d+\.?\d*", res)[0])
#print(pressure)

hour = int(time.strftime('%H',time.localtime(time.time())));
print(hour+1)