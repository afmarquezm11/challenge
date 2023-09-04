"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix
    object_list = []
    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                object_list.append(obj)
        next_token = resp.get('NextContinuationToken', None)

        if not next_token:
            break
    return object_list

#SOLUTION:
"""
Refactor the next function using yield to return the array of objects found by the
`s3.list_objects_v2` function that matches the given prefix.
"""
def get_s3_objects(bucket, prefix=''):
    s3 = boto3.client('s3')

    kwargs = {'Bucket': bucket}
    next_token = None
    if prefix:
        kwargs['Prefix'] = prefix
    object_list = []
    while True:
        if next_token:
            kwargs['ContinuationToken'] = next_token
        resp = s3.list_objects_v2(**kwargs)
        contents = resp.get('Contents', [])
        for obj in contents:
            key = obj['Key']
            if key.startswith(prefix):
                #yield the found object
                yield obj
        next_token = resp.get('NextContinuationToken', None)

        if not next_token:
            break
    return object_list


"""
Please, full explain this function: document iterations, conditionals, and the
function as a whole
"""
def fn(main_plan, obj, extensions=[]):
    """
    This function modifies a list of items based on the main_plan, obj, and extensions.
    
    Args:
        main_plan: a main plan 
        obj: An object containing the item's data.
        extensions: A list of extensions, which can modify the items.
    Returns:
        list: a list of modified items

    """
    items = []
    #Initialize flags for specific cases
    sp = False #Checks if main_plan is present
    cd = False #Checks if any items were deleted

    #Initialize empty dictionary to keep the extension quantities.
    ext_p = {}

    #Populates the ext_p dictionary with extension prices and quantities.
    for ext in extensions:
        ext_p[ext['price'].id] = ext['qty']

    # Iterate through each item in the 'obj' object.
    for item in obj['items'].data:
        #in the product dictionary, it's setting the ID for each item in obj variable
        product = {
            'id': item.id
        }

        # Check if the item's price is different from the main_plan's price and is not in the extension prices.
        if item.price.id != main_plan.id and item.price.id not in ext_p:
            product['deleted'] = True #Product deleted
            cd = True
        # Check if the item's price is in the extension prices.
        elif item.price.id in ext_p:
            qty = ext_p[item.price.id]
            if qty < 1:
                product['deleted'] = True
            else:
                product['qty'] = qty #Adds quantity to the product
            del ext_p[item.price.id] #deletes the id from the extension prices
        #If item's prices is the same as the main plan's
        elif item.price.id == main_plan.id:
            sp = True

        items.append(product)
    
    # If the main_plan is not in the items, add it with quantity 1.
    if not sp:
        items.append({
            'id': main_plan.id,
            'qty': 1
        })

    #I think it adds to the item's list the rest of the items in the extension prices 
    for price, qty in ext_p.items():
        if qty < 1: #It will not add if the quantity is below 1
            continue
        items.append({
            'id': price,
            'qty': qty
        })
    
    return items


"""
Having the class `Caller` and the function `fn`
Refactor the function `fn` to execute any method from `Caller` using the argument `fn_to_call`
reducing the `fn` function to only one line.
"""
class Caller:
    add = lambda a, b : a + b
    concat = lambda a, b : f'{a},{b}'
    divide = lambda a, b : a / b
    multiply = lambda a, b : a * b

def fn(fn_to_call, *args):
    result = None

    if fn_to_call == 'add':
        result = Caller.add(*args)
    if fn_to_call == 'concat':
        result = Caller.concat(*args)
    if fn_to_call == 'divide':
        result = Caller.divide(*args)
    if fn_to_call == 'multiply':
        result = Caller.multiply(*args)

    return result

#SOLUTION:
def fn_refactor(fn_to_call: str, *args):
    return getattr(Caller, fn_to_call)(*args)


"""
A video transcoder was implemented with different presets to process different videos in the application. The videos should be
encoded with a given configuration done by this function. Can you explain what this function is detecting from the params
and returning based in its conditionals?
"""
def fn(config, w, h):
    v = None
    ar = w / h
    # It seems it is receiving a configuration, a width and height, and calculating the aspect ratio (ar)

    if ar < 1:
        #If aspect ratio is less than 1, it takes the configuration in r for portrait video
        v = [r for r in config['p'] if r['width'] <= w]
    elif ar > 4 / 3:
        #If aspect ratio is 4:3 or landscape
        v = [r for r in config['l'] if r['width'] <= w]
    else:
        #For every other aspect ratio
        v = [r for r in config['s'] if r['width'] <= w]

    return v 
    # V is a list storing data according to the aspect ratio of the video, I'm assuming p means portrait and l for landscape.
    # Maybe something like v = [ {different video params}, {}, {}, ...]

"""
Having the next helper, please implement a refactor to perform the API call using one method instead of rewriting the code
in the other methods.
"""
import requests
class Helper:
    DOMAIN = 'http://example.com'
    SEARCH_IMAGES_ENDPOINT = 'search/images'
    GET_IMAGE_ENDPOINT = 'image'
    DOWNLOAD_IMAGE_ENDPOINT = 'downloads/images'

    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

        
    def search_images(self, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f'{token_type} {access_token}',
        }

        URL = f'{self.DOMAIN}/{self.SEARCH_IMAGES_ENDPOINT}'

        send = {
            'headers': headers,
            'params': kwargs
        }

        response = request.get(requests, method)(URL, **send)
        return response
        
    def get_image(self, image_id, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f'{token_type} {access_token}',
        }

        URL = f'{self.DOMAIN}/{self.GET_IMAGE_ENDPOINT}/{image_id}'

        send = {
            'headers': headers,
            'params': kwargs
        }

        response = request.get(requests, method)(URL, **send)
        return response

    def download_image(self, image_id, **kwargs):
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f'{token_type} {access_token}',
        }

        URL = f'{self.DOMAIN}/{self.DOWNLOAD_IMAGE_ENDPOINT}/{image_id}'

        send = {
            'headers': headers,
            'data': kwargs
        }

        response = request.post(requests, method)(URL, **send)
        return response
    
#SOLUTION 

import requests

class Helper:
    DOMAIN = 'http://example.com'
    AUTHORIZATION_TOKEN = {
        'access_token': None,
        'token_type': None,
        'expires_in': 0,
        'refresh_token': None
    }

    def create_request(self, endpoint, method='GET', **kwargs):
        #This is common to every request
        token_type = self.AUTHORIZATION_TOKEN['token_type']
        access_token = self.AUTHORIZATION_TOKEN['access_token']

        headers = {
            'Authorization': f' {token_type} {access_token}',
        }

        URL = f'{self.DOMAIN}/{endpoint}'

        if method == 'GET':
            send_data = {'headers': headers, 'params': kwargs}
            response = requests.get(URL, **send_data)
        elif method == 'POST':
            send_data = {'headers': headers, 'data': kwargs}
            response = requests.post(URL, **send_data)

        return response

    def search_images(self, **kwargs):
        return self.create_request('search/images', 'GET', **kwargs)

    def get_image(self, image_id, **kwargs):
        return self.create_request(f'image/{image_id}', 'GET', **kwargs)

    def download_image(self, image_id, **kwargs):
        return self.create_request(f'downloads/images/{image_id}', 'POST', **kwargs)
