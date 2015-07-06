# mysql-database-describe
Text report generator for MySQL databases

Usage
-----
python ./mysql-database-describe.py host username password database > output.txt

Example
-------
```
DATABASE: phpmyadmin

TABLE_NAME          | ENGINE | TABLE_COLLATION | TABLE_COMMENT                              
------------------- | ------ | --------------- | -------------------------------------------
pma_bookmark        | MyISAM | utf8_bin        | Bookmarks                                  
pma_column_info     | MyISAM | utf8_bin        | Column information for phpMyAdmin          
pma_designer_coords | MyISAM | utf8_bin        | Table coordinates for Designer             
pma_history         | MyISAM | utf8_bin        | SQL history for phpMyAdmin                 
pma_pdf_pages       | MyISAM | utf8_bin        | PDF relation pages for phpMyAdmin          
pma_recent          | MyISAM | utf8_bin        | Recently accessed tables                   
pma_relation        | MyISAM | utf8_bin        | Relation table                             
pma_table_coords    | MyISAM | utf8_bin        | Table coordinates for phpMyAdmin PDF output
pma_table_info      | MyISAM | utf8_bin        | Table information for phpMyAdmin           
pma_table_uiprefs   | MyISAM | utf8_bin        | Tables' UI preferences                     
pma_tracking        | MyISAM | utf8_bin        | Database changes tracking for phpMyAdmin   
pma_userconfig      | MyISAM | utf8_bin        | User preferences storage for phpMyAdmin    

---

TABLE: pma_bookmark

COLUMN_NAME | COLUMN_TYPE  | COLLATION_NAME  | COLUMN_KEY | EXTRA          | COLUMN_DEFAULT | IS_NULLABLE | COLUMN_COMMENT
----------- | ------------ | --------------- | ---------- | -------------- | -------------- | ----------- | --------------
id          | int(11)      |                 | PRI        | auto_increment |                | NO          |               
dbase       | varchar(255) | utf8_bin        |            |                |                | NO          |               
user        | varchar(255) | utf8_bin        |            |                |                | NO          |               
label       | varchar(255) | utf8_general_ci |            |                |                | NO          |               
query       | text         | utf8_bin        |            |                |                | NO          |               

INDEX_NAME | SEQ_IN_INDEX | COLUMN_NAME | NON_UNIQUE | NULLABLE | INDEX_TYPE
---------- | ------------ | ----------- | ---------- | -------- | ----------
PRIMARY    | 1            | id          | 0          |          | BTREE     

---

TABLE: pma_column_info

COLUMN_NAME            | COLUMN_TYPE     | COLLATION_NAME  | COLUMN_KEY | EXTRA          | COLUMN_DEFAULT | IS_NULLABLE | COLUMN_COMMENT
---------------------- | --------------- | --------------- | ---------- | -------------- | -------------- | ----------- | --------------
id                     | int(5) unsigned |                 | PRI        | auto_increment |                | NO          |               
db_name                | varchar(64)     | utf8_bin        | MUL        |                |                | NO          |               
table_name             | varchar(64)     | utf8_bin        |            |                |                | NO          |               
column_name            | varchar(64)     | utf8_bin        |            |                |                | NO          |               
comment                | varchar(255)    | utf8_general_ci |            |                |                | NO          |               
mimetype               | varchar(255)    | utf8_general_ci |            |                |                | NO          |               
transformation         | varchar(255)    | utf8_bin        |            |                |                | NO          |               
transformation_options | varchar(255)    | utf8_bin        |            |                |                | NO          |               

INDEX_NAME | SEQ_IN_INDEX | COLUMN_NAME | NON_UNIQUE | NULLABLE | INDEX_TYPE
---------- | ------------ | ----------- | ---------- | -------- | ----------
db_name    | 1            | db_name     | 0          |          | BTREE     
db_name    | 2            | table_name  | 0          |          | BTREE     
db_name    | 3            | column_name | 0          |          | BTREE     
PRIMARY    | 1            | id          | 0          |          | BTREE     

[...]
```

References
----------
* [Changing default encoding of Python?](http://stackoverflow.com/questions/2276200/changing-default-encoding-of-python)
* [Fetching rows as dictionaries with MySQL Connector/Python](http://geert.vanderkelen.org/fetching-rows-as-dictionaries-with-mysql-connectorpython/)

Notes
-----
Meh.
