# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import re

import datetime
from django.shortcuts import render_to_response, render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from Analysis_Code import mycode
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# from shatel_app.comma_seperate import comma_seperate
mgws = ['MGW_HMN_EALI', 'MGW_KOR_SAN', 'MGW_YZD_SADQ', 'MGW_QOM_QOM', 'MGW_ARB_PC', 'MGW_ZNJ_PC', 'MGW_SMN_AMLO', 'MGW_OUR_MDRS', 'MGW_KRM_VASR', 'MGW_BOU_BHMN', 'MGW_HAM_TAHER', 'MGW_MZN_EMAM2', 'MGW_TEH_SC21','MGW_FRS_VALI', 'MGW_ESF_EMAM1', 'MGW_ESF_EMAM2', 'MGW_ABZ_KRJ', 'MGW_KHZ_VALI2', 'MGW_KHZ_VALI1', 'MGW_CMB_PC', 'MGW_MZN_EMAM1','MGW_GLN_GLSR', 'MGW_GRN_EMAM', 'MGW_KHS_PC', 'MGW_TEH_SC22','MGW_TAB_RHMI', 'MGW_TEH_ISC2', 'MGW_HAM_TAHER2', 'MGW_KHR_FRSH', 'MGW_KHR_FRSH2']
prefixes = ['76', '87', '35', '25', '45', '24', '23', '44', '34', '77', '81', '11', '21','71', '11', '31', '31', '26', '61','61', '38', '11','13', '17', '58','21', '41', '21','81', '51', '51']
operators = ['shatel', 'mci', 'mtn', 'rtl', 'TCI', 'TIC', 'Undefined']
dates=["oneDay", "oneWeek", "oneMonth","threeMonth","sixMonth", "oneYear"]
deltas = [-1 , -7, -30,-90,-180,-365]

@login_required(login_url="/login/")
@csrf_exempt
def home(request):
    return redirect('/dashcoard')


@login_required(login_url="/login/")
@csrf_exempt
def Operator_analysis(request):
    mgw = []
    source_operator = []
    destination_operator = []
    start_date = (datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        mgw = request.POST.getlist('MGW')
        source_operator = request.POST.getlist('source_operator')
        destination_operator = request.POST.getlist('destination_operator')
        start_date = request.POST.getlist('start_date')
        end_date = request.POST.getlist('end_date')
        data = mycode.operatordanalysis(mgw, start_date[0], end_date[0], source_operator,destination_operator)
        return render(request,'Operator_analysis.html', {'user_selected_mgw':mgw,'end_date':end_date,'start_date':start_date, 'source_operator':source_operator,'destination_operator':destination_operator,'duration' : json.dumps(data[0]), 'crinfo' : json.dumps(data[1]) , 'NER' : json.dumps(data[2]), 'now' : datetime.datetime.today().strftime('%Y-%m-%d'), 'now_30' : (datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d'), "mgws":mgws, "operators":operators})
    return render(request, 'Operator_analysis_form.html', {'user_selected_mgw':mgw,'end_date':end_date,'start_date':start_date, 'source_operator':source_operator,'destination_operator':destination_operator,"mgws":mgws, "operators":operators})

@login_required(login_url="/login/")
@csrf_exempt
def Prefix_analysis(request):
    mgw = ["MGW_FRS_VALI"]
    source_prefix=[]
    destination_prefix=[]
    end_date=datetime.datetime.today().strftime('%Y-%m-%d')
    start_date=(datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d')
    if request.method == 'POST':
        mgw = request.POST.getlist('province')
        source_prefix = re.split(',',request.POST.getlist('source_prefix')[0])
        destination_prefix = re.split(',', request.POST.getlist('destination_prefix')[0])
        start_date = request.POST.getlist('start_date')
        end_date = request.POST.getlist('end_date')
        data = mycode.prefixanalysis(mgw, start_date[0], end_date[0], source_prefix, destination_prefix)
        return render(request , 'Prefix_analysis.html', {'user_selected_mgw':mgw,'end_date':end_date,'start_date':start_date, 'source_prefix':source_prefix,'destination_prefix':destination_prefix,'duration' : json.dumps(data[0]), 'crinfo' : json.dumps(data[1]) , 'NER' : json.dumps(data[2]) , 'now' : datetime.datetime.today().strftime('%Y-%m-%d'), 'now_30' : (datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d'), "mgws":mgws, "operators":operators})
    return render(request, 'Prefix_analysis_form.html', {'user_selected_mgw':mgw,'end_date':end_date,'start_date':start_date, 'source_prefix':source_prefix,'destination_prefix':destination_prefix,"mgws":mgws, "operators":operators})


@login_required(login_url="/login/")
@csrf_exempt
def Myquery(request):
    if request.method == 'POST':
        query = request.POST.getlist('myquery')
        data = mycode.myQuery(query[0])
        print data, type(data)
        return render(request, "Myquery.html", {'query' : query[0], 'duration' : json.dumps(data[1]), 'NER' : json.dumps(data[2])})
    return render(request, "Myquery_form.html")

@login_required(login_url="/login/")
@csrf_exempt
def dailyshatel(request):
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    mgw =[]
    if request.method == 'POST':
        mgw = request.POST.getlist('MGW')
        date = request.POST.getlist('date')
        print mgw, date[0]
        data = mycode.dailyshatel(mgw, date[0])
        print data
        return render(request, 'dailyshatel_analysis.html', {'user_selected_mgw':mgw,'date' : date, 'duration' : json.dumps(data), 'now' : datetime.datetime.today().strftime('%Y-%m-%d'), "mgws":mgws, "operators":operators})
    return render(request, 'Dailyshatel_analysis_form.html', {'user_selected_mgw':mgw,'date' : date, "mgws":mgws, "operators":operators})


@login_required(login_url="/login/")
@csrf_exempt
def Periodshatel(request):
    mgw = []
    operator = []
    start_date = (datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d')
    end_date = request.POST.getlist('end_date')
    if request.method == 'POST':
        mgw = request.POST.getlist('MGW')
        operator = request.POST.getlist('operator')
        start_date = request.POST.getlist('start_date')
        end_date = request.POST.getlist('end_date')
        print mgw, start_date[0], end_date[0], operator
        data = mycode.showDistDur(mgw, start_date[0], end_date[0], operator)
        print data
        return render(request, 'Period_analysis.html', {'user_selected_mgw':mgw,'end_date':end_date,'start_date':start_date,'operator':operator,"mgws":mgws, "operators":operators, 'period_data' : json.dumps(data), 'now' : datetime.datetime.today().strftime('%Y-%m-%d'), 'now_30' : (datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d')})
    return render(request, 'Period_analysis_form.html', {'user_selected_mgw':mgw,'end_date':end_date,'start_date':start_date,'operator':operator,"mgws":mgws, "operators":operators, 'now' : datetime.datetime.today().strftime('%Y-%m-%d'), 'now_30' : (datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d')})


@login_required(login_url="/login/")
@csrf_exempt
def dynamic(request):
    return render(request, 'dynamic.html')


@login_required(login_url="/login/")
@csrf_exempt
def Dashboard(request):
    from Analysis_Code import period_result2Postgres
    from Analysis_Code import duration_per_operator_result2Postgres
    from Analysis_Code import duration_per_province_result2Postgres
    # duration_per_operator = mycode.dailyshatel(mgws,(datetime.datetime.today() + datetime.timedelta(-30)).strftime('%Y-%m-%d'))

    DateList = ["1day", "1week", "1month" , "3month", "6month", "1year"]
    ################# duration per operator ##############
    duration_per_operator= duration_per_operator_result2Postgres.duration_per_operator_data_read(dates)
    for i in range(0,len(duration_per_operator)):
        # print duration_per_operator[i]
        duration_per_operator[i] = eval(duration_per_operator[i])


    ###############  period_data Generate ###############
    period_data = period_result2Postgres.period_data_read()
    mgw_operator = []
    for i in range(0,len(mgws)):
        for j in range(0,len(operators)):
            mgw_operator.append([mgws[i], operators[j]])
    period_data = eval(period_data)
    #########################################################3


    ############### duration per provinces #############
    Incoming_duration_per_province = duration_per_province_result2Postgres.Incoming_duration_per_province_data_read(dates)
    for i in range(0,len(Incoming_duration_per_province)):
        # print duration_per_province[i]
        Incoming_duration_per_province[i] = eval(Incoming_duration_per_province[i])
    Outgoing_duration_per_province = duration_per_province_result2Postgres.Outgoing_duration_per_province_data_read(dates)
    for i in range(0,len(Outgoing_duration_per_province)):
        # print duration_per_province[i]
        Outgoing_duration_per_province[i] = eval(Outgoing_duration_per_province[i])

    ############## crinfo per provinces ################
    Incoming_crinfo_per_province = duration_per_province_result2Postgres.Incoming_crinfo_per_province_data_read(dates)
    for i in range(0,len(Incoming_crinfo_per_province)):
        Incoming_crinfo_per_province[i] = eval(Incoming_crinfo_per_province[i])
    Outgoing_crinfo_per_province = duration_per_province_result2Postgres.Outgoing_crinfo_per_province_data_read(dates)
    for i in range(0,len(Outgoing_crinfo_per_province)):
        Outgoing_crinfo_per_province[i] = eval(Outgoing_crinfo_per_province[i])
    return render(request, 'Dashboard.html', {"DateList": DateList,"period_data" : json.dumps(period_data), "Incoming_duration_per_province" : json.dumps(Incoming_duration_per_province), "Outgoing_duration_per_province" : json.dumps(Outgoing_duration_per_province), "duration_per_operator": json.dumps(duration_per_operator), "Incoming_crinfo_data": json.dumps(Incoming_crinfo_per_province), "Outgoing_crinfo_data": json.dumps(Outgoing_crinfo_per_province), "mgws":mgws, "operators":operators, "mgw_operator":json.dumps(mgw_operator)})
