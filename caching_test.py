from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE":"RedisCache", "CACHE_REDIS_HOST":"127.0.0.1", "CACHE_REDIS_PORT":"6379"})

cache.init_app(app)

@app.route('/')
@cache.cached(timeout=3600)
def index():
    return f"hello {[_ for _ in range(1000)]}"

@app.route('/a')
@cache.cached(timeout=3600)
def a():
    return "well hello there"


if __name__ == "__main__":
    app.run(debug=True )