import csv, sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE Comments (id,review_id,text,author,pub_date);") # use your column names here

with open('/Users/macbookbro/Dev/api_yamdb/data/comments.csv','r', encoding='utf8') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['review_id'], i['text'], i['author'], i['pub_date']) for i in dr]

cur.executemany("INSERT INTO Comments (id,review_id,text,author,pub_date) VALUES (?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()