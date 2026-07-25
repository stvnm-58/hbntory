def response(message, data=None):

    result = {

        "message": message

    }


    if data:

        result["data"] = data


    return result
