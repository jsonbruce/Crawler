from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response, json, jsonify, Response
from . import main
from ..models import Project, getProvinces, getCities, getCityProjects


@main.route('/data', methods=['GET'])
def data():
    projects = Project.query.limit(50).all()
    data = [p.to_json() for p in projects]
    response = Response(json.dumps(data), mimetype="application/json")
    return response


@main.route('/provinces', methods=['GET'])
def get_provinces():
    provinces = getProvinces()
    response = Response(json.dumps(provinces), mimetype="application/json")
    return response


@main.route('/cities', methods=['GET'])
def get_cities():
    cities = getCities()
    response = Response(json.dumps(cities), mimetype="application/json")
    return response


@main.route('/cityprojects', methods=['GET'])
def get_city_projects():
    data = getCityProjects()
    data = sorted(data.items(), key=lambda v : v[1], reverse=True)
    result = []
    for k, v in data:
        result.append({'name': k, 'value': v})
    response = Response(json.dumps(result), mimetype="application/json")
    return response


@main.route('/index', methods=['GET'])
@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')
