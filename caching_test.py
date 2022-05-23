from flask import Flask
from flask_caching import Cache
from random import randint

app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE":"RedisCache", "CACHE_REDIS_HOST":"127.0.0.1", "CACHE_REDIS_PORT":"6379"})

cache.init_app(app)

@app.route('/')
@cache.cached(timeout=10)
def index():
    return f"hello {randint(10, 1000)}"


if __name__ == "__main__":
    app.run(debug=True )