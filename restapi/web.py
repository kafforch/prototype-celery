from flask import Flask, request, jsonify
from workers.application import store_new_plan
from model.plan_parser import PlanParserDeco
from restapi.response import response
import logging

app = Flask(__name__)


@app.route('/orchestrate', methods=['POST'])
def orchestrate():
    try:
        json_payload = request.get_json()
    except:
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
            logging.exception("Error occured while trying to submit celery task")
            return response(body="Unable to submit plan", status=500)

        return response(
            body='{{"plan_id": "{0}"}}'.format(plan_id),
            status=200
        )


if __name__ == '__main__':
    app.run(debug=True)
