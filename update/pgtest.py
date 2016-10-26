import os
import psycopg2
import urlparse
#os.environ["DATABASE_URL"]="postgres://vkmornqrrtwcac:o9EHjYYljxJqzIiiyzY2gJ77TZ@ec2-54-235-250-156.compute-1.amazonaws.com:5432/d4nn8u1tlq76j6"
def main():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)

    cur = conn.cursor()
    print cur
    db_data = cur.execute("select * from pages")
    print db_data


if __name__ == "__main__":
    main()
