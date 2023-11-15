from .entities.users import User


class ModelUsers:
    @classmethod
    def get_by_id(cls, db, user_id):
        try:
            with db.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, usertype, fullname FROM users WHERE id = %s", (
                        user_id,)
                )
                row = cursor.fetchone()
                if row:
                    return User(row[0], row[1], None, row[2], row[3])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(cls, db, user):
        try:
            with db.connection.cursor() as cursor:
                cursor.execute("call sp_verifyIdentity(%s, %s)",
                               (user.username, user.password))
                row = cursor.fetchone()
                if row and row[0] is not None:
                    return User(row[0], row[1], row[2], row[4], row[3])
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)
