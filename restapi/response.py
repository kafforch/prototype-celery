def response(body="", status=200, headers={"Content-Type": "application/json"}):
    return (
        body,
        status,
        headers
    )