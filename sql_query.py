1.
import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("justjoin.sqlite")

cur = con.cursor()

# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute("""
SELECT SUM(Count) AS TotalCount
FROM (
  SELECT COUNT(*) AS Count
  FROM tech
  GROUP BY Technologies
) subquery;
"""):
    print(row)

# Be sure to close the connection
con.close()


2.
import sqlite3

conn = sqlite3.connect('justjoin.sqlite')
c = conn.cursor()

c.execute('DROP TABLE tech;')

conn.commit()
conn.close()




# Open Table
 SELECT *
  FROM tech;

# Count Technologies
SELECT SUM(Count) AS TotalCount
FROM (
  SELECT COUNT(*) AS Count
  FROM tech
  GROUP BY Technologies
) subquery;
