from sqlalchemy import create_engine
import os
from common.tools import get_credentials

dbName = 'chat'
dbUrlBase = 'mysql+pymysql://{}@localhost'.format(get_credentials(os.path.dirname(os.environ['GRESSPRO']) + '/.db_secrets'))
dbUrl = dbUrlBase + '/' + dbName
defaultConnectArgs = {'charset': 'utf8mb4'}

engine = create_engine(dbUrl, connect_args = defaultConnectArgs, encoding = 'utf-8', echo = False)
