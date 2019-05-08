To crawl from **www.Amazon.com**, we can simply run

``` {bash}
python3 ./amazon_crawler.py #entries sku1 sku2 sku3 ...
```

Here *#entries* is the number of entries you want, which is usually set from 50 to 200 in order to avoid black listing of Amazon.com.

11/29: now *#entries* represents num of additional entries you want. Script will tell you current num of entries in json.

*sku1 sku2 sku3 ...* are beginning node of crawler to begin with. The crawler will go from these skus to go to linked skus from their sites. skus are informat of 10 characters and can be obtained directly from Amazon product link.

A product link from Amazon is like *https://www.amazon.com/dp/B077KSCW6G* and **B077KSCW6G** is the sku embedded.

For example, we can run command like

``` {bash}
python3 ./amazon_crawler.py 100 B077KSCW6G B01MDNLX2Q
```

After the data is crawled, to dump data into the sqlite database, please run the following code

``` {bash}
python3 ./dump.py
```

The code will automatically regenerate the data and dump all changes in data.json into ../db.sqlite.