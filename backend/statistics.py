from app import app
from flask import request, jsonify
from dbse import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


@app.route('/img_task')
def img_task():
    return app.send_static_file('task_statistics.png')


@app.route('/statistics', methods=['POST', 'GET'])
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

    categories = ['Year', 'Month', 'Day', 'Completed']
    values = [task_sy, task_sm, task_sd, task_st]

    # 绘图
    plt.figure(figsize=(8, 6))
    plt.bar(categories, values, color=['blue', 'green', 'red', 'purple'])
    plt.xlabel('Categories')
    plt.ylabel('Number of Tasks')
    plt.title('Number of Tasks by Category')
    plt.ylim(0, max(values) * 1.1)  # 设置y轴上限，留出一些空间显示数据
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # 添加水平虚线网格
    plt.tight_layout()
    plt.savefig('./static/task_statistics.png')

    return jsonify({
        'task_sy': task_sy,
        'task_sm': task_sm,
        'task_sd': task_sd,
        'task_st': task_st,
        'account_s': account_s,
        'image_url': 'img_task',
    })
