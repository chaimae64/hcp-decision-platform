import psycopg2


class AuthService:

    @staticmethod
    def login(username, password):

        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="hcp_bi",
            user="postgres"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username, role
            FROM users
            WHERE username=%s
            AND password=%s
            """,
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user