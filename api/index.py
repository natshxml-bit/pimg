from flask import Flask, jsonify

# Import rute dari folder routes
from api.routes.home import home_bp
# Nanti import juga yang lain: from api.routes.chapter import chapter_bp, dll

app = Flask(__name__)

# Register rute (Mirip app.use('/home', homeRouter) di Express)
app.register_blueprint(home_bp, url_prefix='/home')

@app.route('/')
def index():
    return jsonify({
        "status": True,
        "message": "API MGKOMIK versi Python Berjalan Mantap 🚀"
    })

# Ini wajib ada biar Vercel bisa ngeksekusi Flask-nya
if __name__ == '__main__':
    app.run()
