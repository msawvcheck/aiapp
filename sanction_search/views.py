from django.shortcuts import render
from . JUSTICE import doj_search1
from . OFAC import ofac_search1
from . OFAC_NAME import ofac_search_name1
from . JUSTICE_NAME import doj_search_name1


# Create your views here.


def index(request):
    return render(request,'sanction_search_t/home.html')

def doj_search(request):
    doj_table = doj_search1()
    d=[doj_table['url'],doj_table['name'],doj_table['age'],doj_table['place']]
    d1=list(zip(*d))
    return render(request,'sanction_search_t/doj.html',{'doj_table' : d1})

def doj_search_name(request):
    if (request.method == "POST"):
        nam = request.POST.get('fname', None)
        doj_table = doj_search_name1(nam)
        d=[doj_table['url'],doj_table['name'],doj_table['age'],doj_table['place']]
        d1=list(zip(*d))
    return render(request,'sanction_search_t/doj.html',{'doj_table' : d1})

def ofac_search(request):
    ofac_table = ofac_search1()
    p=[ofac_table['name'],ofac_table['address'],ofac_table['type'],ofac_table['program'],ofac_table['list'],ofac_table['score']]
    p1=list(zip(*p))
    return render(request,'sanction_search_t/ofac.html',{'ofac_table' : p1})

def ofac_search_name(request):
    if (request.method == "POST"):
         nam = request.POST.get('fname', None)
         ofac_name_table = ofac_search_name1(nam)
         pn=[ofac_name_table['name'],ofac_name_table['address'],ofac_name_table['type'],ofac_name_table['program'],ofac_name_table['list'],ofac_name_table['score']]
         pn1=list(zip(*pn))
    return render(request,'sanction_search_t/ofac_name.html',{'ofac_table_nam' : pn1})
