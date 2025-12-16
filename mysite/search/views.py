from django.db.models import Value # <-- 이 줄을 추가합니다.
from django.db.models.functions import Replace # <-- Replace만 functions에서 임포트합니다.
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
    # 기존: return HttpResponse("Cartoon Landing Page!")
    # 변경: 'search/landing.html' 템플릿을 렌더링합니다.
    return render(request, 'search/landing.html')

def gotomain(request):
    return render(request, 'search/search.html')

def search(request):
    book_list = Book.objects.all().order_by('title') 
    q = request.GET.get('q', "") 
    
    if q:
        # 1. 사용자가 입력한 검색어에서 띄어쓰기를 제거합니다.
        cleaned_q = q.replace(' ', '')
        
        # 2. 쿼리셋에 띄어쓰기가 제거된 임시 필드를 추가합니다 (DB 함수 사용).
        #    Replace('필드명', Value('찾을 문자'), Value('대체할 문자'))
        book_list = book_list.annotate(
            cleaned_title=Replace('title', Value(' '), Value('')),
            cleaned_author=Replace('author', Value(' '), Value('')),
        )
        
        # 3. 띄어쓰기가 제거된 임시 필드를 기준으로 필터링합니다.
        book_list = book_list.filter(
            Q(cleaned_title__icontains=cleaned_q) | 
            Q(cleaned_author__icontains=cleaned_q)
        ).distinct()
        
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
    if request.method == 'POST':
       title = request.POST.get('title')
       number = request.POST.get('number')
       author = request.POST.get('author')
       publisher = request.POST.get('publisher')
       location = request.POST.get('location')
        
       book = Book(title=title, number=number, author=author, publisher=publisher, location=location,)
       book.save()
       return redirect('search:new')
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
