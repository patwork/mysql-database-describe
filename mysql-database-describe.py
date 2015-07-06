#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Text report generator for MySQL databases
# https://github.com/patwork/mysql-database-describe
#

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

import MySQLdb

# ----------------------------------------------------------------------------
config = {
	'schema': 'information_schema',
	'charset': 'utf8',
	'init_command': 'SET NAMES UTF8',
	'delimiter': ' | '
}

# ----------------------------------------------------------------------------
def fatalError(e):

	if isinstance(e, str):
		sys.stderr.write(e)
		sys.exit(2)

	elif isinstance(e, MySQLdb.Error):
		sys.stderr.write('MySQL error (%d): %s\n' % (e.args[0], e.args[1]))
		sys.exit(3)

	else:
		sys.stderr.write('Error: %s\n' % sys.exc_info()[0])
		sys.exit(4)

# ----------------------------------------------------------------------------
def myPrint(txt):

	print txt

# ----------------------------------------------------------------------------
def myPrintTable(data, cols):

	if len(data) < 2:
		return

	num = len(cols)
	pads = [ 0 ] * num
	bar = []

	for row in data:
		for col in range(num):
			pads[col] = max(pads[col], len(row[col]))

	for col in range(num):
		bar.append('-' * pads[col])
	data.insert(1, bar)

	for row in data:
		txt = []
		for col in range(num):
			txt.append(row[col].ljust(pads[col]))
		myPrint(config['delimiter'].join(txt))

	myPrint('')

# ----------------------------------------------------------------------------
def dbQuery(mysql, sql):

	data = []
	cur = mysql.cursor()

	try:
		cur.execute(sql)
		columns = tuple( [col[0].decode(config['charset']) for col in cur.description] )
		for row in cur:
			data.append(dict(zip(columns, row)))

	except MySQLdb.Error, e:
		fatalError(e)

	finally:
		cur.close()

	return data

# ----------------------------------------------------------------------------
def getTables(mysql, database):

	sql = 'SELECT * FROM `TABLES` WHERE `TABLE_SCHEMA` = "%s" ORDER BY `TABLE_NAME`' % mysql.escape_string(database)
	return dbQuery(mysql, sql)

# ----------------------------------------------------------------------------
def getColumns(mysql, database):

	sql = 'SELECT * FROM `COLUMNS` WHERE `TABLE_SCHEMA` = "%s" ORDER BY `ORDINAL_POSITION`' % mysql.escape_string(database)
	return dbQuery(mysql, sql)

# ----------------------------------------------------------------------------
def getKeys(mysql, database):

	sql = 'SELECT * FROM `STATISTICS` WHERE `TABLE_SCHEMA` = "%s" ORDER BY `INDEX_NAME`, `SEQ_IN_INDEX`' % mysql.escape_string(database)
	return dbQuery(mysql, sql)

# ----------------------------------------------------------------------------
def getExt(mysql, database):

	sql = 'SELECT * FROM `KEY_COLUMN_USAGE` WHERE `TABLE_SCHEMA` = "%s" AND `REFERENCED_TABLE_SCHEMA` IS NOT NULL ORDER BY `CONSTRAINT_NAME`' % mysql.escape_string(database)
	return dbQuery(mysql, sql)

# ----------------------------------------------------------------------------
def showDatabase(database):

	myPrint('DATABASE: %s\n' % database)

# ----------------------------------------------------------------------------
def showTables(tables):

	cols = [ 'TABLE_NAME', 'ENGINE', 'TABLE_COLLATION', 'TABLE_COMMENT' ]
	output = [ cols ]

	for table in tables:
		row = []
		for col in cols:
			row.append(table[col])
		output.append(row)

	myPrintTable(output, cols)

# ----------------------------------------------------------------------------
def showDetails(tables, columns, keys, ext):

	details = [
		{ 'data': columns, 'names': [ 'COLUMN_NAME', 'COLUMN_TYPE', 'COLLATION_NAME', 'COLUMN_KEY', 'EXTRA', 'COLUMN_DEFAULT', 'IS_NULLABLE', 'COLUMN_COMMENT' ] },
		{ 'data': keys, 'names': [ 'INDEX_NAME', 'SEQ_IN_INDEX', 'COLUMN_NAME', 'NON_UNIQUE', 'NULLABLE', 'INDEX_TYPE' ] },
		{ 'data': ext, 'names': [ 'CONSTRAINT_NAME', 'COLUMN_NAME', 'REFERENCED_TABLE_NAME', 'REFERENCED_COLUMN_NAME' ] }
	]

	for table in tables:
		table_name = table['TABLE_NAME']

		myPrint('---\n\nTABLE: %s\n' % table_name)

		for detail in details:

			data = detail['data']
			names = detail['names']
			output = [ names ]

			for arr in data:
				if arr['TABLE_NAME'] == table_name:
					row = []
					for name in names:
						row.append('' if arr[name] == None else str(arr[name]))
					output.append(row)

			myPrintTable(output, names)

# ----------------------------------------------------------------------------
def createReport(args):

	try:
		mysql = MySQLdb.connect(
			host = args[1],
			user = args[2],
			passwd = args[3],
			db = config['schema'],
			charset = config['charset'],
			init_command = config['init_command']
		)

	except MySQLdb.Error, e:
		fatalError(e)

	database = args[4]

	tables = getTables(mysql, database)
	columns = getColumns(mysql, database)
	keys = getKeys(mysql, database)
	ext = getExt(mysql, database)

	showDatabase(database)
	showTables(tables)
	showDetails(tables, columns, keys, ext)

	try:
		mysql.close()

	except MySQLdb.Error, e:
		fatalError(e)

# ----------------------------------------------------------------------------
if __name__ == '__main__':

	if len(sys.argv) < 5:
		print 'usage: %s host username password database' % (sys.argv[0])
		sys.exit(1)

	createReport(sys.argv)
	sys.exit(0)

# EoF
# vim: noexpandtab tabstop=4 softtabstop=4 shiftwidth=4
