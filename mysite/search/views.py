from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Book
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import xlwt
import csv

# Create your views here.

def landing(request):
    return HttpResponse("Cartoon Landing Page!")

def gotomain(request):
    return render(request, 'search/search.html')

def search(request):
    book_list = Book.objects.all().order_by('title')
    q = request.GET.get('q', "") 
    if q:
        book_list = book_list.filter(Q(title__icontains=q) | Q(author__icontains=q)).distinct()
        context = {'book_list' : book_list,}
        return render(request, 'search/result.html', context)
    else:
        book_list = Book.objects.all().order_by('title')
        context = {'book_list' : book_list,}
        return render(request, 'search/result.html', context)

@login_required
def orderby(request):
        book_list = Book.objects.order_by('location')
        context = {'book_list' : book_list,}
        return render(request, 'search/result.html', context)

@login_required
def new(request):
    return render(request, 'search/insert.html')

@login_required
def insert(request):
    title = request.POST.get('title')
    author = request.POST.get('author')
    publisher = request.POST.get('publisher')
    location = request.POST.get('location')
    
    book = Book(title=title, author=author, publisher=publisher, location=location,)
    book.save()
    return render(request, 'search/insert.html')

@login_required
def edit(request, book_id):
    book = Book.objects.get(id=book_id)
    context = {'book' : book}
    return render(request, 'search/update.html', context)

@login_required
def update(request, book_id):
    book = Book.objects.get(id=book_id)
    book.title = request.POST.get('title')
    book.number = request.POST.get('number')
    book.author = request.POST.get('author')
    book.publisher = request.POST.get('publisher')
    book.location = request.POST.get('location')
    book.save()
    return redirect('search:gotomain')

@login_required
def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('search:gotomain')

@login_required
def export_list(request):
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'book_list.xls' 
    wb = xlwt.Workbook(encoding='ansi')
    ws = wb.add_sheet('도서목록')
    row_num = 0
    col_names = ['title', 'number', 'author', 'publisher', 'location']
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name)
    rows = Book.objects.all().values_list('title', 'number', 'author', 'publisher', 'location') 
    for row in rows:
        row_num +=1
        for col_num, attr in enumerate(row):
            ws.write(row_num, col_num, attr)
    wb.save(response)
    return response

@login_required
def export_content(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_book.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['title', 'number', 'author', 'publisher', 'location'])
    rows = Book.objects.all().values_list('title', 'number', 'author', 'publisher', 'location') 
    for row in rows:
        writer.writerow(row)
    return response