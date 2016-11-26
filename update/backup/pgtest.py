import os
import psycopg2
import urlparse
os.environ["DATABASE_URL"]="postgres://bzcqxiwycrcsmu:hbMRZUikdHaEguseLgkzc0Dyka@ec2-54-235-250-156.compute-1.amazonaws.com:5432/d6p1tgnp1b7nsp"
def main():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(dbname=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)



    cur = conn.cursor()
    cur.execute("select max(number) from pages;")
    db_name = cur.fetchall()
    print db_name
    


if __name__ == "__main__":
    main()
