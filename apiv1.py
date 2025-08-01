from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Iamsorry1@localhost/news_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

article_categories = db.Table('article_categories',
    db.Column('article_id', db.String(36), db.ForeignKey('articles.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    publication_date = db.Column(db.DateTime)
    source_name = db.Column(db.String(100))
    relevance_score = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    categories = db.relationship('Category', secondary=article_categories, backref='articles')

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), unique=True)


def serialize_article(article):
    return {
        'id': article.id,
        'title': article.title,
        'description': article.description,
        'url': article.url,
        'publication_date': article.publication_date.isoformat() if article.publication_date else None,
        'source_name': article.source_name,
        'categories': [c.category_name for c in article.categories],
        'relevance_score': article.relevance_score
    }

@app.route('/api/v1/news/category')
def get_by_category():
    cat = request.args.get('category')
    if not cat:
        return jsonify({'error': 'category parameter required'}), 400
    articles = (
        Article.query
        .join(article_categories)
        .join(Category)
        .filter(Category.category_name == cat)
        .order_by(Article.publication_date.desc())
        .limit(5)
        .all()
    )
    return jsonify([serialize_article(a) for a in articles])

@app.route('/api/v1/news/score')
def get_by_score():
    try:
        min_score = float(request.args.get('min_score', 0))
    except ValueError:
        return jsonify({'error': 'min_score must be a float'}), 400
    articles = (
        Article.query
        .filter(Article.relevance_score >= min_score)
        .order_by(Article.relevance_score.desc())
        .limit(5)
        .all()
    )
    return jsonify([serialize_article(a) for a in articles])

@app.route('/api/v1/news/search')
def full_text_search():
    query_param = request.args.get('query')
    if not query_param:
        return jsonify({'error': 'query parameter required'}), 400

    # like_pattern = f"%{query_param}%"
    # articles = (
    #     Article.query
    #     .filter(
    #         Article.title.ilike(like_pattern) |
    #         Article.description.ilike(like_pattern)
    #     )
    #     .order_by(Article.relevance_score.desc())
    #     .limit(5)
    #     .all()
    # )
    match_expr = "MATCH(title, description) AGAINST(:query_param IN NATURAL LANGUAGE MODE)"
    articles = (
        Article.query
        .filter(text(match_expr))
        .order_by(text(f"{match_expr} + relevance_score DESC"))
        .params(query_param=query_param)
        .limit(5)
        .all()
    )
    return jsonify([serialize_article(a) for a in articles])

@app.route('/api/v1/news/source')
def get_by_source():
    source = request.args.get('source')
    if not source:
        return jsonify({'error': 'source parameter required'}), 400
    articles = (
        Article.query
        .filter(Article.source_name == source)
        .order_by(Article.publication_date.desc())
        .limit(5)
        .all()
    )
    return jsonify([serialize_article(a) for a in articles])

@app.route('/api/v1/news/nearby')
def get_nearby():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        radius = float(request.args.get('radius', 10))
    except (TypeError, ValueError):
        return jsonify({'error': 'lat, lon, radius must be numeric'}), 400
    haversine = 6371 * func.acos(
        func.cos(func.radians(lat)) * func.cos(func.radians(Article.latitude)) *
        func.cos(func.radians(Article.longitude) - func.radians(lon)) +
        func.sin(func.radians(lat)) * func.sin(func.radians(Article.latitude))
    )
    results = (
        Article.query
        .add_columns(haversine.label('distance'))
        .filter(haversine <= radius)
        .order_by(text('distance ASC'))
        .limit(5)
        .all()
    )
    articles = [article for article, dist in results]
    return jsonify([serialize_article(a) for a in articles])

if __name__ == '__main__':
    app.run(debug=True)
