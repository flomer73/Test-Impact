#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import *
import json
import base64

def index(request):
	context = {}
	return render(request, 'index.html', context)

def getResponseTriangle(request, area, tipo, points):
    return HttpResponse(calculate_triangle(area, tipo, points))

def getResponseSquare(request, area, points):
    return HttpResponse(calculate_square(area, points))
    

def as_points(string):
    string = string + '=='
    arrayPoints = json.loads(base64.b64decode(string).decode('utf-8'))
    points = arrayPoints
    return points

def valid_points(points, shape):
    for i in range(0, len(points)):
        for j in range(i+1, len(points)):
            if points[i] == points[j]:
                return False
    if shape == 'square':
        d_ab = distance([points[0], points[1]])
        d_ac = distance([points[0], points[2]])
        d_ad = distance([points[0], points[3]])
        d_bc = distance([points[1], points[2]])
        d_bd = distance([points[1], points[3]])
        d_cd = distance([points[2], points[3]])
        distances = set([d_ab, d_ac, d_ad, d_bc, d_bd, d_cd])
        if len(distances) == 2:
            return True
    elif shape == 'triangle':
        d_ab = distance([points[0], points[1]])
        d_bc = distance([points[1], points[2]])
        d_ca = distance([points[2], points[0]])
        if d_ab + d_ca > d_bc and\
           d_ab + d_bc > d_ca and\
           d_ca + d_bc > d_ab:
            return True
    return False

def is_isosceles(points):
    # El triangulo es isosceles
    d_ab = distance([points[0], points[1]])
    d_bc = distance([points[0], points[2]])
    d_ca = distance([points[1], points[2]])
    if d_ab == d_ca or d_ab == d_bc or d_bc == d_ca:
        return True
    return False

def distance(points):
    if len(points) == 2:
        if len(points[0]) == 2 and len(points[1]) == 2:
            return ((points[1][0] - points[0][0])**2 + (points[1][1] - points[0][1]) ** 2.0) ** 0.5
    return -1

def as_num(value):
    try:
        value = float(value)
    except ValueError:
        value = None
    finally:
        return value

def areaShape(points, shape):
    _area = -1
    if shape == 'square':
        _area = abs(points[1][0] - points[0][0]) * 2
        
    if shape == 'triangle':
        _area = abs(((points[0][0] * (points[1][1] - points[2][1])) +\
                     (points[1][0] * (points[2][1] - points[0][1])) +\
                     (points[2][0] * (points[0][1] - points[1][1]))) / 2.0)

    return _area

def calculate_square(area, points):
    arg_area = as_num(area)
    points = as_points(points)
    if arg_area and points and len(points) == 4:
        if (valid_points(points, 'square') and areaShape(points, 'square') == arg_area):
            return 'response = true;'
    return 'response = false;'

def calculate_triangle(area, tipo, points):
    arg_area = as_num(area)
    shape = tipo
    points = as_points(points)
    if arg_area and points and len(points) == 3:
        if (valid_points(points, 'triangle') and areaShape(points, 'triangle') == arg_area):
            if ((shape == 'isosceles' and is_isosceles(points)) or shape == 'other'):
                return 'response = true;'
    return 'response = false;'