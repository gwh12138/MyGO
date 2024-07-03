from app import app
from flask import request, jsonify
from dbse import *
from datetime import datetime,timedelta


@app.route('/statistics', methods=['POST'])
def statistics():
    now_date = request.json.get('date')
    now_date = datetime.strptime(now_date, '%Y-%m-%d').date()
    year_b = now_date.strftime('%Y-01-01')
    year_e = now_date.strftime('%Y-12-31')
    mon_b = now_date.strftime('%Y-%m-01')
    first_day_of_next_month = datetime(now_date.year + (now_date.month // 12), ((now_date.month % 12) + 1), 1).date()
    mon_e = first_day_of_next_month - timedelta(days=1)
    day = now_date
    task_sy = len(task.search_task_by_date(year_b, year_e))
    task_sm = len(task.search_task_by_date(mon_b, mon_e))
    task_sd = len(task.search_task_by_date(day, day))
    task_st = len(task.search_task(task_state=u'已完成'))
    account_s = len(account.search_account())
    return jsonify({
        'task_sy': task_sy,
        'task_sm': task_sm,
        'task_sd': task_sd,
        'task_st': task_st,
        'account_s': account_s,
    })
