import pymysql
import json

host = 'localhost'
user = 'root'
password = 'Iamsorry1'
database = 'news_data'

connection = pymysql.connect(
    host=host,
    user=user,
    password=password
)

cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS news_data CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
cursor.execute("USE news_data;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    url TEXT,
    publication_date DATETIME,
    source_name VARCHAR(100),
    relevance_score FLOAT,
    latitude FLOAT,
    longitude FLOAT
);
""")

cursor.execute("""
ALTER TABLE articles 
ADD FULLTEXT INDEX ft_title_description (title, description);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS article_categories (
    article_id VARCHAR(36),
    category_id INT,
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles(id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
""")

with open('news_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_categories = set()
for article in data:
    for category in article['category']:
        all_categories.add(category)

for category in all_categories:
    cursor.execute("INSERT IGNORE INTO categories (category_name) VALUES (%s)", (category,))

cursor.execute("SELECT category_name, category_id FROM categories")
category_dict = {row[0]: row[1] for row in cursor.fetchall()}

article_data = []
article_categories_data = []
for article in data:
    article_id = article['id']
    publication_date = article['publication_date'].replace('T', ' ')
    article_tuple = (
        article_id,
        article['title'],
        article['description'],
        article['url'],
        publication_date,
        article['source_name'],
        article['relevance_score'],
        article['latitude'],
        article['longitude']
    )
    article_data.append(article_tuple)
    for category in article['category']:
        category_id = category_dict[category]
        article_categories_data.append((article_id, category_id))

cursor.executemany("""
INSERT INTO articles (id, title, description, url, publication_date, source_name, relevance_score, latitude, longitude)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""", article_data)

cursor.executemany("""
INSERT INTO article_categories (article_id, category_id)
VALUES (%s, %s)
""", article_categories_data)

connection.commit()

cursor.close()
connection.close()

print("Data successfully stored in the 'news_data' database.")