def create_bare_tables(DBAPI2Connector, SQLFile=None):
    cur = DBAPI2Connector.cursor()
    if SQLFile == None:
        sqlqueries = os.path.dirname(os.path.realpath(__file__))
        sqlqueries = os.path.join(sqlqueries, "bootstrap.sql")
        sqlqueries = open(sqlqueries, mode="r")
    else:
        sqlqueries = open(SQLFile, mode="r")
    cur.execute(sqlqueries)
    DBAPI2Connector.commit()
    cur.close()
