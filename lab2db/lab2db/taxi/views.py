from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from Database import DB


def initialize_database(request):
    database = DB()
    database.initialization()

    # User.objects.initialize()
    # Product.objects.initialize()
    # Department.objects.initialize()

    return redirect('/')


def main(request):
    database = DB()
    msgs = []
    if 'fromLength' in request.GET and 'toLength' in request.GET \
            and request.GET['fromLength'] != '' and request.GET['toLength'] != '':
        list = database.getOrderListByLength(int(request.GET['fromLength']), int(request.GET['toLength']))
        msgs.append('by travel length')
    elif 'car_id' in request.GET and request.GET['car_id'] != '0':
        list = database.getOrderListByDriverID(int(request.GET['car_id']))
        msgs.append('by driver name')
    elif 'excludeWord' in request.GET and request.GET['excludeWord'] != '':
        list = database.getListExcluded(request.GET['excludeWord'])
        msgs.append('without : ' + request.GET['excludeWord'])
    elif 'includeWord' in request.GET and request.GET['includeWord'] != '':
        list = database.getListIncluded(request.GET['includeWord'])
        msgs.append('with : ' + request.GET['includeWord'])
    else:
        list = database.getOrderList()
    car = database.getCarList()
    return render(request, 'main_page.html', {'msgs': msgs, 'list': list, 'car': car})


def remove(request, id):
    database = DB()
    database.removeOrder(id)
    return redirect('/')


def edit(request, id):
    database = DB()
    if request.method == 'GET':
        address = database.getAddressList()
        car = database.getCarList()
        client = database.getClientList()
        order = database.getOrder(id)
        return render(request, 'edit_page.html', {'address': address, 'car': car, 'client': client, 'order': order})
    else:
        database.updateOrder(id, request.POST['start_id'], request.POST['finish_id'], request.POST['car_id'],
                             request.POST['client_id'], request.POST['entry-day-time'])
        return redirect('/')


def add(request):
    database = DB()
    if request.method == 'GET':
        address = database.getAddressList()
        car = database.getCarList()
        client = database.getClientList()
        return render(request, 'add_page.html', {'address': address, 'car': car, 'client': client})
    elif request.method == 'POST':
        database.saveOrder(request.POST['start_id'], request.POST['finish_id'], request.POST['car_id'],
                           request.POST['client_id'], request.POST['entry-day-time'])
        return redirect('/')
