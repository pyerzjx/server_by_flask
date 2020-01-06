from flask import Blueprint, request, jsonify, g
from utils.token_utils import TokenMaker
import datetime
import json
from tasks.celery import celery
from tasks.tasks_general import add
from utils.celery_sqlalchemy_scheduler.models import PeriodicTask, IntervalSchedule
from tasks.celery import beat_session
from tasks.celery import CeleryResult
import importlib

apitest = Blueprint("apitest", __name__)


@apitest.route("/test_general_task/", methods=['POST'])
def test_general_task():
    res = add.apply_async((3, 7), countdown=120)
    return jsonify({'code': 1, 'id': res.task_id})


@apitest.route("/test_schedule_task/", methods=['POST'])
def taskschedule():
    token = g.token.get('token')
    schedule = IntervalSchedule(every=20, period=IntervalSchedule.SECONDS)  # 每20秒执行一次
    task_id = TokenMaker().generate_token(token, datetime.datetime.now())
    task = PeriodicTask(id=task_id, interval=schedule, name='my_task', task='tasks.tasks_general.add',
                        args=json.dumps([16, 16]))
    beat_session.add(task)
    beat_session.commit()
    return jsonify({'code': 1, 'id': task_id})


@apitest.route("/query_result/", methods=['POST'])
def query_result():
    json_data = request.get_json()
    task_id = json_data.get('task_id')
    state = CeleryResult(task_id).state
    return jsonify({'code': 1, 'state': state})


@apitest.route("/task_revoke/", methods=['POST'])
def task_revoke():
    json_data = request.get_json()
    task_id = json_data.get('task_id')
    celery.control.terminate(task_id, signal='SIGKILL')

    return jsonify({'code': 1})


@apitest.route("/schedule_task_revoke/", methods=['POST'])
def schedule_task_revoke():
    json_data = request.get_json()
    task_id = json_data.get('task_id')
    beat_row = beat_session.query(PeriodicTask).filter(PeriodicTask.id == task_id).first()
    beat_row.enabled = 0
    beat_session.commit()
    return jsonify({'code': 1})


@apitest.route("/query_schedule_result/", methods=['POST'])
def query_schedule_result():
    json_data = request.get_json()
    task_id = json_data.get('task_id')
    beat_row = beat_session.query(PeriodicTask).filter(PeriodicTask.id == task_id).first()
    state = beat_row.enabled
    return jsonify({'code': 1, 'state': state})
