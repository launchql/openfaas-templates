import json

def getArticles():
    query = '''
        query GetArticles {
            articles {
            nodes {
                image
                id
                ownerId
            }
            }
        }
    '''
    return query

def handle(params, context):
    """handle a request to the function
    Args:
        params (json): request body
        context (json): context, including GraphQL client
    """
    
    result = context.client.execute(getArticles())

    return {
        'function': 'ok',
        'params': params,
        'result': json.loads(result)}

