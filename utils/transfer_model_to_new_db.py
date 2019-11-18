import ixmp
import message_ix

model = 'MESSAGE South Africa'
baseline = 'baseline'
database = 'message_sa'

mp = ixmp.Platform(dbprops=f'db/{database}', dbtype='HSQLDB')
mp_new = ixmp.Platform(dbprops=f'db_new/{database}', dbtype='HSQLDB')
base = message_ix.Scenario(mp, model=model, scenario=baseline)
fixed = base.clone(platform=mp_new, model=model, scenario='baseline', keep_solution=True)
mp.close_db()
mp_new.close_db()
