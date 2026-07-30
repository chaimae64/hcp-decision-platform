import psycopg2


class UserService:

    @staticmethod
    def get_all():

        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="hcp_bi",
            user="postgres"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                username,
                email,
                role,
                created_at
            FROM users
            ORDER BY id
        """)

        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return users

    @staticmethod
    def create(username, email, password, role):

        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="hcp_bi",
            user="postgres"
        )

        cursor = conn.cursor()

        # Vérifier le nom d'utilisateur
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username=%s
            """,
            (username,)
        )

        if cursor.fetchone():

            cursor.close()
            conn.close()

            return "username_exists"

        # Vérifier l'email
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        if cursor.fetchone():

            cursor.close()
            conn.close()

            return "email_exists"

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password,
                role
            )
            VALUES
            (%s,%s,%s,%s)
            """,
            (
                username,
                email,
                password,
                role
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return "success"


    @staticmethod
    def delete(user_id):

        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="hcp_bi",
            user="postgres"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_by_id(user_id):

        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="hcp_bi",
            user="postgres"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                role
            FROM users
            WHERE id=%s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user


    @staticmethod
    def update(user_id, username, email, role):

        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="hcp_bi",
            user="postgres"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET
                username=%s,
                email=%s,
                role=%s
            WHERE id=%s
            """,
            (
                username,
                email,
                role,
                user_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def change_password(user_id, password):

        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="hcp_bi",
            user="postgres"
        )

        cursor = conn.cursor()

        # Vérifier que l'utilisateur existe
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        if not cursor.fetchone():

            cursor.close()
            conn.close()

            return False

        # Modifier le mot de passe
        cursor.execute(
            """
            UPDATE users
            SET password = %s
            WHERE id = %s
            """,
            (
                password,
                user_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return True