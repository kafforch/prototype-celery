from json import loads


def response(body="", status=200, headers={}):
    try:
        loads(body)
        headers['Content-Type'] = 'application/json'
    except ValueError:
        headers['Content-Type'] = 'application/text'

    return (
        body,
        status,
        headers
    )
