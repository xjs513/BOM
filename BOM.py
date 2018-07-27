# -*- coding:utf-8 -*-
# !/usr/bin/env python

from flask import Flask, render_template
import config
from controller.menu_controller import menu
from controller.bom_input_ctr import bom_input_do
from controller.bom_product_ctr import bom_product_do
from controller.bom_composite_ctr import bom_composite_do
from controller.bom_rel_ctr import bom_rel_do

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(menu, url_prefix='/menu')
app.register_blueprint(bom_input_do, url_prefix='/bom_input_do')
app.register_blueprint(bom_product_do, url_prefix='/bom_product_do')
app.register_blueprint(bom_composite_do, url_prefix='/bom_composite_do')
app.register_blueprint(bom_rel_do, url_prefix='/bom_rel_do')


@app.route('/')
def index():
    return render_template("home.html")


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=config.PORT)
