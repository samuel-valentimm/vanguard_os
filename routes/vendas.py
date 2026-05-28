from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.venda_service import VendaService

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route("/venda_direta", methods=['GET', 'POST'])
def nova_venda():

    if request.method == 'POST':

        try:
            VendaService.registrar_venda_direta(request.form)
            flash("Venda realizada!", "success")
        except Exception as e:
            flash(f"Erro: {str(e)}", "error")

        return redirect(url_for('vendas.nova_venda'))
    
    return render_template("venda_direta.html")