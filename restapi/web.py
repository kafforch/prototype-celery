from flask import Flask, request, jsonify
from workers.application import store_new_plan
from model.plan_parser import PlanParserDeco
from restapi.response import response
from model.plan_repo import PlanRepo
from utils.config import KafforchConfigurator
from utils.file_utils import find
from redis import StrictRedis
import logging

app = Flask(__name__)

config = KafforchConfigurator(find("kafforch.cfg", ".."))
redis_config = config.get_redis_config_kwargs()
plan_repo = PlanRepo(StrictRedis(**redis_config))


@app.route('/plan/<plan_id>', methods=['GET'])
def get_plan(plan_id):
    plan = plan_repo.get_plan_by_id(plan_id)

    if plan is None:
        return response(
            body="Unable to find plan",
            status=400
        )

    return response(
        body=plan.to_json(),
        status=200
    )


@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    try:
        json_payload = request.get_json()
    except Exception as ex:
        logging.exception("Error occurred while parsing request")
        json_payload = None

    if json_payload is None:
        return response(body="Needs json payloads and application/json to be set.", status=400)
    else:
        try:
            plan = PlanParserDeco(json_payload)
            result = store_new_plan.delay(plan)
            plan_id = result.get(10)
            if plan_id is None:
                raise RuntimeError()
        except Exception as ex:
            logging.exception("Error occurred while trying to submit celery task")
            return response(body="Unable to submit plan", status=500)

        return response(
            body='{{"plan_id": "{0}"}}'.format(plan_id),
            status=200
        )


if __name__ == '__main__':
    app.run(debug=True)
