import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

from flask import Flask, render_template
from routes.clientes import clientes_bp
from routes.estoque import estoque_bp
from routes.financeiro import financeiro_bp
from routes.vendas import vendas_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.register_blueprint(clientes_bp)
app.register_blueprint(estoque_bp)
app.register_blueprint(financeiro_bp)
app.register_blueprint(vendas_bp)
app.register_blueprint(dashboard_bp)


@app.route("/")
def index():
    return render_template("index.html")

def formatar_moeda(valor):
    try:
        numero = float(valor) if valor is not None else 0.0
    except (ValueError, TypeError):
        numero = 0.0
    return f"R$ {numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

app.jinja_env.filters['formatar_moeda'] = formatar_moeda

if __name__ == "__main__":
    app.run(debug=True)