from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dashboard.auth import login_required
from dashboard.db import get_db

bp = Blueprint('company', __name__)

@bp.route('/')
def index():
    db = get_db()
    companies = db.execute(
        'SELECT c.id, company_name, company_password'
        ' FROM company c'
    ).fetchall()
    return render_template('company/index.html', companies=companies)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_password = request.form['company_password']
        error = None

        if not company_name:
            error = 'Name is required.'
        if not company_password:
            error = 'Password is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO company (company_name, company_password, created_by)'
                ' VALUES (?, ?, ?)',
                (company_name, company_password, g.user['id'])
            )
            db.commit()
            return redirect(url_for('company.index'))

    return render_template('company/create.html')


def get_company(id):
    company = get_db().execute(
        'SELECT c.id, company_name, company_password'
        ' FROM company c'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if company is None:
        abort(404, f"Company id {id} doesn't exist.")

    return company

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    company = get_company(id)

    if request.method == 'POST':
        company_name = request.form['company_name']
        company_password = request.form['company_password']
        error = None

        if not company_name:
            error = 'Name is required.'
        if not company_password:
            error = 'Password is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE company SET company_name = ?, company_password = ?'
                ' WHERE id = ?',
                (company_name, company_password, id)
            )
            db.commit()
            return redirect(url_for('company.index'))

    return render_template('company/update.html', company=company)
