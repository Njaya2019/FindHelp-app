import psycopg2
import os
import psycopg2.extras as psyExtras

class db():
    # set DB_URL=dbname=userdb user=postgres host=localhost password=a1990n
    # userdb_param = os.environ['DB_URL']
    # testdb_param = os.environ['TDB_URL']
    
    @staticmethod
    def connectToDatabase(db_parameters):
        try:
            # db_env_var
            # db_parameters = os.environ[db_env_var]
            con = psycopg2.connect(db_parameters)
        except KeyError:
            message = "Expected database environment variable '{}' not set.".format(db_parameters)
            print(message)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            cur = con.cursor(cursor_factory=psyExtras.DictCursor)
            return (con, cur)
    
    @staticmethod
    def createTables(con_cur):
        # current_timestamp is timezone aware
        # field questionimage is set notnull because it's value can be null.
        tables=(
            """CREATE TABLE IF NOT EXISTS users(userid SERIAL PRIMARY KEY,fullname VARCHAR(50) NOT NULL,
               email VARCHAR(50) NOT NULL,roles BOOLEAN NOT NULL,passwords TEXT NOT NULL, emailverified BOOLEAN NOT NULL DEFAULT false)
            """,
            """CREATE TABLE IF NOT EXISTS questions(questionid SERIAL PRIMARY KEY,questiontitle VARCHAR(300) NOT NULL,
               questiondescription TEXT NOT NULL,questionimage TEXT,timeposted TIMESTAMPTZ,
               userid INT REFERENCES users(userid) ON DELETE CASCADE, tags TEXT [])
            """,
            """CREATE TABLE IF NOT EXISTS answers(answerid SERIAL PRIMARY KEY,userid INT REFERENCES users(userid) ON DELETE CASCADE,
               questionid INT REFERENCES questions(questionid) ON DELETE CASCADE,
               answer TEXT NOT NULL,answerimage TEXT,timeanswered TIMESTAMPTZ, markedcorrect BOOLEAN NOT NULL DEFAULT false)
            """,
            """CREATE TABLE IF NOT EXISTS votes(userid INT REFERENCES users(userid) ON DELETE CASCADE,answerid INT REFERENCES answers(answerid) ON DELETE CASCADE,
               upvote INT DEFAULT 0  NOT NULL, downvote INT DEFAULT 0 NOT NULL, PRIMARY KEY(userid, answerid))
            """,
            """CREATE TABLE IF NOT EXISTS comments(commentid SERIAL PRIMARY KEY, comment VARCHAR(300) NOT NULL, answerid INT REFERENCES answers(answerid) ON DELETE CASCADE,
               userid INT REFERENCES users(userid) ON DELETE CASCADE,timecommented TIMESTAMPTZ)
            """,
            """ALTER TABLE users ADD COLUMN emailverified BOOLEAN  NOT NULL DEFAULT false
            """

           )
        try:
            con=con_cur[0]
            cur=con_cur[1]
            # create table one by one
            for table in tables:
                cur.execute(table)
                print('TABLE CREATED')
            # close communication with the PostgreSQL database server
            # cur.close()
            # commit the changes. Saves data to the database permanently.
            con.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            pass
        finally:
            # close communication with the PostgreSQL database server
            # con.close()
            # cur.close()
            pass
    
    @staticmethod
    def dropTables(con_cur):
        try:
            # con_cur = db.connectToDatabase(db_url)
            con = con_cur[0]
            cur = con_cur[1]
            table_names = ('users', 'questions', 'answers', 'votes', 'comments')
            for table_name in table_names:
                del_query = 'DROP TABLE IF EXISTS {} CASCADE'.format(table_name)
                cur.execute(del_query)
            con.commit()
        except TypeError as err:
            print(err)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            print('Tables deleted')
        finally:
            # close communication with the PostgreSQL database server
            # con.close()
            # cur.close()
            pass



# r=db.connectToDatabase('DB_URL')
# db.createTables()
# db.dropTables()


# print(r)

