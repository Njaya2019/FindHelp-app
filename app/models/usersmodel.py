from .dataBase import db
from werkzeug.security import check_password_hash, generate_password_hash

class users():

    @staticmethod
    def addUser(con_cur, fullname, email, roles, passwords):
        try:
            con = con_cur[0]
            cur = con_cur[1]
            email_sql = "SELECT email FROM users WHERE email=%s"
            cur.execute(email_sql, (email,))
            # if there are no rows fetchall returns an empty list.
            emailAvailable = cur.fetchone()
            if emailAvailable:
                return "The email already exists"
            else:
                hashed_password=generate_password_hash(passwords, method='sha256')
                adduser_sql = "INSERT INTO users(fullname,email,roles,passwords) VALUES(%s,%s,%s,%s) RETURNING userid, fullname, email, roles, passwords"
                userData = (fullname, email, roles, hashed_password,)
                cur.execute(adduser_sql, userData)
                con.commit()
                addedUser = cur.fetchone()
                return addedUser
        except Exception as err:
            print(err)
        finally:
            pass
            # if con is not None:
            #     con.close()
    @staticmethod
    def userLogin(con_cur, email, password):
        '''A method to check the authenicity of the user'''
        try:
            con = con_cur[0]
            cur = con_cur[1]
            email_sql = "SELECT * FROM users WHERE email=%s"
            cur.execute(email_sql, (email,))
            authent_user = cur.fetchone()
            if authent_user:
                
                check_password = check_password_hash(authent_user['passwords'], password)
                if check_password:
                    return authent_user
                else:
                    return 'Wrong password'
            else:
                return 'The user with email {} dosen\'t exists. Check the email and try again'.format(email)
        except Exception as err:
            print(err)
        finally:
            if con is not None:
                con.close()



# d=users.addUser("Andrew Njaya Odhiambo", "njayaandrew@ande.com", "Admin", "1234")
# print(d)