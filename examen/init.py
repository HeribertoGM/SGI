from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd

engine = create_engine('postgresql+psycopg2://usr:pword@localhost:5432/MemSch')

def populate(obj):
	df = pd.read_csv(obj['file_name'])
	df.columns = [x.lower() for x in df.columns]

	if 'fechaultimamod' not in df.columns and obj['index']:
		df['fechaultimamod'] = datetime.today().strftime('%Y-%m-%d')
	if 'nombrepcmod' not in df.columns and obj['index']:
		df['nombrepcmod'] = 'hgm'
	if 'clausuariomod' not in df.columns and obj['index']:
		df['clausuariomod'] = 86

	df.to_sql(obj['table_name'].lower(), engine, if_exists='append', index=obj['index'], index_label=obj['index_label'].lower())

files = [
	{
		"file_name": "./data/MDA_exa.csv",
		"table_name": "MemTraMDADet",
		"index": True,
		"index_label": "idMDA"
	},
	{
		"file_name": "./data/MTR_exa.csv",
		"table_name": "MemTraMTRDet",
		"index": True,
		"index_label": "idMTR"
	},
	{
		"file_name": "./data/TC_exa.csv",
		"table_name": "MemTraTcDet",
		"index": True,
		"index_label": "idTc"
	},
	{
		"file_name": "./data/tbfin_exa.csv",
		"table_name": "MemTraTBFin",
		"index": False,
		"index_label": ""
	}
]

if __name__ == "__main__":
	for file in files:
		populate(file)
	
		print(f'finished: {file["table_name"]}')
	
	print('finished')