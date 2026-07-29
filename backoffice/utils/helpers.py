def response(message, data=None):
    # Petit format de réponse standard {message, data?} — pas encore utilisé par les controllers
    result = {

        "message": message

    }


    if data:

        result["data"] = data


    return result
