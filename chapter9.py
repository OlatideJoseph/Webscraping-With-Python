import pprint
import psycopg


def main(conninfo="dbname=pages user=webcrawler"):
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DROP TABLE IF EXISTS pages;"
                "CREATE TABLE IF NOT EXISTS pages ("
                "id BIGSERIAL PRIMARY KEY,"
                "title VARCHAR(200),"
                "content VARCHAR(10000),"
                "created TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
            )
            cur.execute(
                "INSERT INTO pages (title, content) VALUES (%s, %s);",
                (
                    "Test page title",
                    "This is some test page content. It can be up to 10,000 characters long.",
                ),
            )
            cur.execute(
                """INSERT INTO pages (id, title, content, created) VALUES (%s, %s, %s, %s)""",
                (
                    3,
                    "Test page title",
                    "This is some test page content. It can be up to 10,000 characters long.",
                    "2014-09-21 10:25:32",
                ),
            )
            cur.execute("SELECT * FROM pages")
            # will return (1, 100, "abc'def")

            # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
            # of several records, or even iterate on the cursor
            for record in cur.fetchall():
                print(pprint.pformat(record))
            cur.execute("SELECT COUNT(*) FROM pages")
            print(cur.fetchone())

            conn.commit()
    return conn


if __name__ == "__main__":
    conn = main()
    print(conn.closed)
