
import mysql.connector as mysql
from radio_scrape.radio_scrape import DBConfig as dbConf
import time

class MySQL():    #------------------------------------------------------
    def connect(self):
        
        conn = mysql.connect(**dbConf.dbConfig)
        # create cursor 
        cursor = conn.cursor(dictionary=True)
        # cursor = conn.cursor(MySQLdb.cursors.DictCursor)   
        return conn, cursor

    #------------------------------------------------------    
    def close(self, cursor, conn):        
        # close cursor
        cursor.close()
                
        # close connection to MySQL
        conn.close()  

    #------------------------------------------------------        
    def use_community_radio_DB(self, cursor):
        '''Expects open connection.'''
        # select DB
        cursor.execute("USE community_radio")

    

    # ---------------------------------------------------------
    def insert_multiple(self, mySql_insert_query, data_for_db):
        
        # connect to MySQL
        conn, cursor = self.connect()
        
        self.use_community_radio_DB(cursor)

        cursor.executemany(mySql_insert_query, data_for_db)
        conn.commit()
        print(cursor.rowcount, "Record inserted successfully")
   
  
    def insert_episode(self, episode):
        # connect to MySQL
        conn, cursor = self.connect()
        
        self.use_community_radio_DB(cursor)
        
        query = """INSERT INTO episodes (show_id, ep_date, mp3, file_size) VALUES (%s, %s, %s, %s)"""
        cursor.execute(query,(episode['show_id'], episode['ep_date'], episode['mp3'], episode['file_size']))
        
        try:
            conn.commit()
        except:
            print(cursor.statement,)

        time.sleep(.2)
        self.close(cursor, conn)

    #------------------------------------------------------  
          
    def insert_show(self, show):
        # connect to MySQL
        conn, cursor = self.connect()
        self.use_community_radio_DB(cursor)
        
        query = """INSERT INTO shows (`showName`, `source`, `img`, `desc`, `host`, `internal_link`, `ext_link`, `email`, `duration`, `slug`)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) as new
                 ON DUPLICATE KEY UPDATE
                `showName` = new.`showName`, `source` = new.`source`, `img` = new.`img`, `desc` = new.`desc`, `host` = new.`host`, `internal_link` = new.`internal_link`, `ext_link` = new.`ext_link`, `email` = new.`email`, `duration` = new.`duration`, `slug` = new.`slug`;
                """
        # print("""INSERT INTO shows (showName, source, img, desc, host, internal_link, ext_link, email) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (show['showName'], show['source'], show['img'], show['desc'], show['host'], show['internal_link'], show['ext_link'], show['email']))
        
        cursor.execute(query,(show['showName'], show['source'], show['img'], show['desc'], show['host'], show['internal_link'], show['ext_link'], show['email'], show['duration'], show['slug']))
        
        try:
            conn.commit()
        except:
            print(cursor.statement,)

        time.sleep(.2)
        self.close(cursor, conn)

    # ---------------------------------------------------------
    def insert_all_tags(self, data_for_db):
        

        query = """INSERT INTO all_tags (`tag`, `frequency`)
                VALUES (%s, %s) as new
                ON DUPLICATE KEY UPDATE
                `tag` = new.`tag`, `frequency` = new.`frequency`;
                """

        # connect to MySQL
        conn, cursor = self.connect()
        
        self.use_community_radio_DB(cursor)

        cursor.executemany(query, data_for_db)
        conn.commit()
        print(cursor.rowcount, "Records inserted successfully")

    # ---------------------------------------------------------

    def insert_show_tags(self, data_for_db):
        

        query = """INSERT INTO show_tags (`show_id`, `tag_id`, `frequency`)
                VALUES (%s, %s, %s) as new
                ON DUPLICATE KEY UPDATE
                `frequency` = new.`frequency`;
                """

        # connect to MySQL
        conn, cursor = self.connect()
        
        self.use_community_radio_DB(cursor)

        cursor.executemany(query, data_for_db)
        conn.commit()
        print(cursor.rowcount, "Records inserted successfully")

    #------------------------------------------------------   
         
    def get_all_tags(self):
        # connect to MySQL
        conn, cursor = self.connect()
        self.use_community_radio_DB(cursor)
        # select data
        cursor.execute(f"""select * from all_tags""")

        return cursor.fetchall()
    #------------------------------------------------------   
         
    def get_shows_by_source(self, source):
        # connect to MySQL
        conn, cursor = self.connect()
        self.use_community_radio_DB(cursor)
        # select data
        cursor.execute(f"""select * from shows where source='{source}'""")

        return cursor.fetchall()
 
    #------------------------------------------------------   
         
    def get_show_descriptions(self):
        # connect to MySQL
        conn, cursor = self.connect()
        self.use_community_radio_DB(cursor)
        # select data
        cursor.execute("""select `id`, `showName`, `desc` from shows""")

        return cursor.fetchall()

    def get_newest_ep_by_source(self, source):
        # connect to MySQL
        conn, cursor = self.connect()
        self.use_community_radio_DB(cursor)
        # select data
        cursor.execute(f"""with date_ranked_eps AS (
                                select episodes.id, show_id, ep_date,
                                    rank() OVER (PARTITION BY show_id
                                                    ORDER BY ep_date DESC
                                                ) AS `Rank`
                                FROM episodes
                                left join shows
                                on shows.id = episodes.show_id
                                where shows.source = '{source}'
                            )
                            SELECT id, show_id, ep_date
                            FROM date_ranked_eps
                            WHERE `Rank` = 1""")

        return cursor.fetchall()

    def remove_old_eps_by_show(self, show_id):
        # connect to MySQL
        conn, cursor = self.connect()
        self.use_community_radio_DB(cursor)
        
        query = f"""delete from episodes where show_id = {show_id}"""
        print('query', query)
        
        cursor.execute(query,)
        
        try:
            conn.commit()
        except:
            print(cursor.statement,)

        time.sleep(.2)
        self.close(cursor, conn)

    def remove_outdated_show_tags(self, show_id, tag_ids):
        # connect to MySQL
        conn, cursor = self.connect()
        self.use_community_radio_DB(cursor)

        
        query = f"""delete from show_tags where show_id = {show_id} and `tag_id` not in ({','.join(str(id) for id in tag_ids)})"""
        print('query', query)
        
        cursor.execute(query,)
        
        try:
            conn.commit()
        except:
            print(cursor.statement,)

        time.sleep(.2)
        self.close(cursor, conn)