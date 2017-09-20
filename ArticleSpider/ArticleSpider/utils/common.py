import hashlib
import itertools


def get_md5(url):
    if isinstance(url,str):
        url=url.encode('utf-8')
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()


def convert(listnumber):
    value="".join(itertools.chain(*listnumber))
    return value
