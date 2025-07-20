from flask import Flask, Blueprint, render_template, redirect, url_for
from models import House

detail_page = Blueprint("detail_page", __name__)


@detail_page.route("/house/<id>")
def index(id=None):
    if not id:
        return redirect(url_for("index_page.index"))

    house = House.query.filter_by(id=id).first()
    if not house:
        return redirect(url_for("index_page.index"))

    return render_template("detail.html", house=house)
