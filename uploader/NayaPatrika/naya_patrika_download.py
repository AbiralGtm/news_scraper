import shutil

import urllib3
url = 'http://www.enayapatrika.com/enayapatrika.com/ep/2017/12/6/files/pdfsam_merge.pdf'
c = urllib3.PoolManager()

file_name = "date.pdf"
with c.request('GET', url, preload_content=False) as resp, open(file_name, 'wb') as out_file:
    shutil.copyfileobj(resp, out_file)