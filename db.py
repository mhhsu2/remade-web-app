import pymysql
import yaml
import os

class Database:
    def __init__(self):
        CREDENTIAL_DIR = '.credentials'
        db_crediential = yaml.load(open(os.path.join(CREDENTIAL_DIR, 'db.yaml')), Loader=yaml.FullLoader)
        host = db_crediential['mysql_host']
        user = db_crediential['mysql_user']
        password = db_crediential['mysql_password']
        db = db_crediential['mysql_db']
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_exp_info(self):
        self.cur.execute("SELECT * from experiments_info")
        result = self.cur.fetchall()
        return result

    def list_ir(self, loading_amp, exp_id, min_percent_fatigue_life, max_percent_fatigue_life):

        amp = ', '.join(amp for amp in loading_amp)

        query = """
                    SELECT exp_id, 
                        loading_amp, 
                        CAST(norm_cycles*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        cycles,
                        FORMAT(temperature, 2) AS temperature 
                        FROM ir
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND norm_cycles BETWEEN {}/100 AND {}/100
                        AND cycles % 1000 = 0;
                """.format(amp, exp_id, min_percent_fatigue_life, max_percent_fatigue_life)  
        self.cur.execute(query)
        result= self.cur.fetchall()
        return result
    
    def list_ae(self, loading_amp, exp_id, min_percent_fatigue_life, max_percent_fatigue_life):
        amp = ', '.join(amp for amp in loading_amp)

        query = """
                    SELECT exp_id, 
                        loading_amp, 
                        CAST(norm_cycles*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        cycles,
                        FORMAT(avg_ae_hits, 2) AS avg_ae_hits 
                        FROM ae
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND norm_cycles BETWEEN {}/100 AND {}/100;
                """.format(amp, exp_id, min_percent_fatigue_life, max_percent_fatigue_life)       
        self.cur.execute(query)
        result= self.cur.fetchall()
        return result
    
    def list_lu(self, loading_amp, position, exp_id, min_percent_fatigue_life, max_percent_fatigue_life):
        amp = ', '.join(amp for amp in loading_amp)
        pos = ', '.join(p for p in position)

        query = """
                    SELECT exp_id, 
                        loading_amp, 
                        position,
                        replicate,
                        CAST(norm_cycles*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        CAST(avg_wave_speed AS DECIMAL(6,2)) AS avg_wave_speed 
                        FROM lu
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND position IN ({})
                        AND norm_cycles BETWEEN {}/100 AND {}/100;
                """.format(amp, exp_id, pos, min_percent_fatigue_life, max_percent_fatigue_life)       
        self.cur.execute(query)
        result= self.cur.fetchall()
        return result
    
    def list_nlu(self, loading_amp, position, nlu_amp, exp_id, min_percent_fatigue_life, max_percent_fatigue_life):
        l_amp = ', '.join(amp for amp in loading_amp)
        pos = ', '.join(p for p in position)
        nlu_amp =', '.join(amp for amp in nlu_amp)


        query = """
                    SELECT exp_id, 
                        loading_amp, 
                        position,
                        nlu_amp,
                        replicate,
                        CAST(norm_cycles*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        FORMAT(beta, 4) AS beta 
                        FROM nlu
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND position IN ({})
                        AND nlu_amp IN ({})
                        AND norm_cycles BETWEEN {}/100 AND {}/100;
                """.format(l_amp, exp_id, pos, nlu_amp, min_percent_fatigue_life, max_percent_fatigue_life)       
        self.cur.execute(query)
        result= self.cur.fetchall()
        return result

if __name__ == "__main__":
    # Test the db connection
    db = Database()
    print(f"Connected: {db.con.open}")
