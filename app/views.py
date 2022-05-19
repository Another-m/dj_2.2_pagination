from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):

    data = read_data()
    quan_lines = int(request.GET.get("qlines", 10))
    if len(data) % quan_lines > 0:
        quan_lines_all = len(data) // quan_lines + 1
    else:
        quan_lines_all = len(data) // quan_lines

    current_page = int(request.GET.get("page", 1))
    paginator = Paginator(data, quan_lines)
    page = paginator.get_page(current_page)

    count_page = f' | страница {current_page} из {quan_lines_all}  | '
    next_page_url, prev_page_url = None, None
    if current_page < quan_lines_all: next_page_url = f'?qlines={quan_lines}&page={current_page + 1}'
    if current_page > 1: prev_page_url = f'?qlines={quan_lines}&page={current_page - 1}'

    return render(request, 'index.html', context={
        'bus_stations': page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
        'count_page': count_page,
        '5_lines': '?qlines=5',
        '10_lines': '?qlines=10',
        '20_lines': '?qlines=20',
    })


def read_data():
    with open("data-398-2018-08-30.csv", "r") as file:
        data = csv.reader(file)
        data_list = []
        for count, val in enumerate(data):
            data_dict = {'Name': val[1], 'Street': val[4], 'District': val[6]}
            if count != 0: data_list.append(data_dict)

        return data_list
