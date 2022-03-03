# WeiBoHierarchyData & RandomHierarchyData
## WeiBoHierarchyData
### Crawl Operation

crawl data from weibo.com  

links saved in './hotlinks'  

answers saved in './repost' 

```
$ python crawl_repost_hierarchy_data.py
```
### Results to HierarchyData

answers also saved in './repost' 

```
$ python data2tree.py
```

## RandomHierarchyData

random hierarchy data saved in './randjson' 

```
$ python randomJson.py
```