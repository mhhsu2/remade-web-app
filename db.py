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
        query = """
                    SELECT exp_id,
                           loading_amp,
                           FORMAT(max_percent_fatigue_life, 2) AS max_percent_fatigue_life,
                           ir,
                           ae,
                           lu,
                           nlu,
                           xrd
                    FROM exp_info
                """
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def list_ir(self, loading_amp, exp_id, min_percent_fatigue_life, max_percent_fatigue_life):

        amp = ', '.join(amp for amp in loading_amp)

        query = """
                    SELECT exp_id, 
                        loading_amp, 
                        CAST(percent_fatigue_life*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        cycles,
                        FORMAT(temperature, 2) AS temperature 
                        FROM ir
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND percent_fatigue_life BETWEEN {}/100 AND {}/100
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
                        CAST(percent_fatigue_life*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        cycles,
                        FORMAT(ae_hits, 2) AS ae_hits 
                        FROM ae
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND percent_fatigue_life BETWEEN {}/100 AND {}/100;
                """.format(amp, exp_id, min_percent_fatigue_life, max_percent_fatigue_life)       
        self.cur.execute(query)
        result= self.cur.fetchall()
        return result
    
    def list_lu(self, loading_amp, dist_from_center, exp_id, min_percent_fatigue_life, max_percent_fatigue_life):
        amp = ', '.join(amp for amp in loading_amp)
        pos = ', '.join(p for p in dist_from_center)

        query = """
                    SELECT exp_id, 
                        loading_amp, 
                        dist_from_center,
                        replicate,
                        CAST(percent_fatigue_life*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        CAST(wave_speed AS DECIMAL(6,2)) AS wave_speed 
                        FROM lu
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND dist_from_center IN ({})
                        AND percent_fatigue_life BETWEEN {}/100 AND {}/100;
                """.format(amp, exp_id, pos, min_percent_fatigue_life, max_percent_fatigue_life)      
        self.cur.execute(query)
        result= self.cur.fetchall()
        return result
    
    def list_nlu(self, loading_amp, dist_from_center, nlu_amp, exp_id, min_percent_fatigue_life, max_percent_fatigue_life):
        l_amp = ', '.join(amp for amp in loading_amp)
        pos = ', '.join(p for p in dist_from_center)
        nlu_amp =', '.join(amp for amp in nlu_amp)


        query = """
                    SELECT exp_id, 
                        loading_amp, 
                        dist_from_center,
                        nlu_amp,
                        replicate,
                        CAST(percent_fatigue_life*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        FORMAT(acoustic_parameter, 4) AS acoustic_parameter 
                        FROM nlu
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND dist_from_center IN ({})
                        AND nlu_amp IN ({})
                        AND percent_fatigue_life BETWEEN {}/100 AND {}/100;
                """.format(l_amp, exp_id, pos, nlu_amp, min_percent_fatigue_life, max_percent_fatigue_life)       
        self.cur.execute(query)
        result= self.cur.fetchall()
        return result

    def list_xrd(self, loading_amp, dist_from_center, exp_id, min_percent_fatigue_life, max_percent_fatigue_life):
        l_amp = ', '.join(amp for amp in loading_amp)
        pos = ', '.join(p for p in dist_from_center)


        query = """
                    SELECT exp_id, 
                        loading_amp, 
                        dist_from_center,
                        CAST(percent_fatigue_life*100 AS DECIMAL(5,2)) AS percent_fatigue_life, 
                        residual_stress,
                        fwhm
                        FROM xrd
                    WHERE loading_amp IN ({})
                        AND exp_id IN ({})
                        AND dist_from_center IN ({})
                        AND percent_fatigue_life BETWEEN {}/100 AND {}/100;
                """.format(l_amp, exp_id, pos, min_percent_fatigue_life, max_percent_fatigue_life)       
        self.cur.execute(query)
        result= self.cur.fetchall()
        return result
        

    def get_user_id(self, user_id):
        query = f"""
                    SELECT user_id
                    FROM User
                    WHERE user_id = '{user_id}'
        """
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result[0]['user_id']

    def get_user_password(self, user_id):
        query = f"""
                    SELECT password
                    FROM User
                    WHERE user_id = '{user_id}'
        """
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result[0]['password']

if __name__ == "__main__":
    # Test the db connection
    db = Database()
    print(f"Connected: {db.con.open}")

    # Test exp_info table
    print(f"Exp Info Table\n {db.list_exp_info()[0]}")

    # Test ir table
    print(f"IR Table\n {db.list_ir(['11.7'], 5, 5, 30)[0]}")

    # Test ae table
    print(f"AE Table\n {db.list_ae(['11.7'], 5, 5, 30)[0]}")

    # Test lu table
    print(f"LU Table\n {db.list_lu(['11.7'], ['0', '-90'], 19, 0, 100)[0]}")

    # Test nlu table
    print(f"NLU Table\n {db.list_nlu(['11.7'], ['0', '-90'], ['10'], 19, 0, 100)[0]}")

    # Test xrd table
    print(f"XRD Info Table\n {db.list_xrd(['11.7'], ['0', '-90'], 19, 0, 100)[0]}")
