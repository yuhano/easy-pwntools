from flask import Blueprint, redirect, render_template
import easy_pwntools.services.menu_services as menu_services

bp = Blueprint(name = 'menu',
               import_name = __name__)

@bp.route('/', methods=['GET'])
def menu():
    return render_template('menu.html')

@bp.route('/code_editor', methods=['GET'])
def code_editor():
    return render_template('code_editor.html')

@bp.route('/cwe_list', methods=['GET'])
def cwe_list():
    return render_template('cwe_list.html')

@bp.route('/decompiler', methods=['GET'])
def decompiler():
    return render_template('decompiler.html')

@bp.route('/terminal', methods=['GET'])
def terminal():
    return render_template('terminal.html')