from datetime import date
from typing import Dict, List

from flask import Flask, jsonify, redirect, render_template, request, url_for

from backend.database import get_session, init_database
from backend.models import Sale


def create_app() -> Flask:
    init_database()
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

    @app.context_processor
    def inject_defaults():
        today = date.today().isoformat()
        categories = ["Tops", "Bottoms", "Outerwear", "Accessories"]
        sizes = ["XS", "S", "M", "L", "XL"]
        return {"today": today, "categories": categories, "sizes": sizes}

    @app.route("/")
    def index():
        with get_session() as session:
            sales: List[Sale] = session.query(Sale).order_by(Sale.sale_date.desc()).all()
        summary = _summarize_sales(sales)
        return render_template("index.html", sales=sales, summary=summary)

    @app.route("/sales", methods=["POST"])
    def add_sale():
        with get_session() as session:
            sale = Sale(
                item_name=request.form.get("item_name", "").strip(),
                size=request.form.get("size", "").strip(),
                category=request.form.get("category", "").strip(),
                sale_date=date.fromisoformat(request.form.get("sale_date", date.today().isoformat())),
                quantity=int(request.form.get("quantity", 0)),
                unit_price=float(request.form.get("unit_price", 0.0)),
            )
            session.add(sale)
            session.commit()
        return redirect(url_for("index"))

    @app.route("/api/sales")
    def sales_api():
        with get_session() as session:
            sales: List[Sale] = session.query(Sale).order_by(Sale.sale_date.desc()).all()
        payload = [
            {
                "id": sale.id,
                "item_name": sale.item_name,
                "size": sale.size,
                "category": sale.category,
                "sale_date": sale.sale_date.isoformat(),
                "quantity": sale.quantity,
                "unit_price": sale.unit_price,
                "total": sale.total,
            }
            for sale in sales
        ]
        return jsonify(payload)

    @app.route("/api/summary")
    def summary_api():
        with get_session() as session:
            sales: List[Sale] = session.query(Sale).all()
        summary = _summarize_sales(sales)
        return jsonify(summary)

    return app


def _summarize_sales(sales: List[Sale]) -> Dict[str, float]:
    total_revenue = sum(sale.total for sale in sales)
    total_items = sum(sale.quantity for sale in sales)
    average_price = (total_revenue / total_items) if total_items else 0.0
    return {
        "total_revenue": total_revenue,
        "total_items": total_items,
        "average_price": average_price,
    }


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
