import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
# def get_request(url, **kwargs):
#     print(kwargs)
#     print("GET from {} ".format(url))
#     try:
#         # Call get method of requests library with URL and parameters
#         if api_key:
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                     params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
#             print("TESTE")
#         else:
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                     params=kwargs)
#     except:
#         # If any error occurs
#         print("Network exception occurred")
#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data
def get_request(url, **kwargs):
    
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
# def get_dealers_from_cf(url, **kwargs):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url)
#     if json_result:
#         # Get the row list in JSON as dealers
#         dealers = json_result["body"]
#         # For each dealer object
#         for dealer in dealers:
#             # Get its content in `doc` object
#             dealer_doc = dealer["doc"]
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"], 
#                                     id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], 
#                                     short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)
            
#         return results
def get_dealers_from_cf(url, **kwargs):
    info = []
    result = "ok"
    # - Call get_request() with specified arguments
    print("Get Dealers from CF")
    json_result = get_request(url)
    if json_result:
        dealers = json_result['body']
        print(len(dealers))
        for dealer in dealers:
            dlr_data = dealer['doc']
            #print('ADDRESS', dlr_data["address"])
            if dlr_data.get('address'):
            # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dlr_data.get("address"), city=dlr_data.get("city"), full_name=dlr_data.get("full_name"),
                            id=dlr_data.get("id"), lat=dlr_data.get("lat"), long=dlr_data.get("long"),
                            short_name=dlr_data.get("short_name"),
                            st=dlr_data.get("st"), zip=dlr_data.get("zip"))
            
            # dealer_obj = CarDealer(address=dealer["doc"]["address"], city=dealer["doc"]["city"], full_name=dealer["doc"]["full_name"],
            #                     id=dealer["doc"]["id"], lat=dealer["doc"]["lat"], long=dealer["doc"]["long"],
            #                     short_name=dealer["doc"]["short_name"], 
            #                     st=dealer["doc"]["st"], state=dealer["doc"]["state"], zip=dealer["doc"]["zip"])
                info.append(dealer_obj)
    elif json_result:
        result = json_result["message"]
    else:
        result = "Unknown error"
    return info

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
# def get_dealer_reviews_from_cf(url, dealerId):
#     results = []
#     json_result = get_request(url, dealerId=dealerId)
#     if json_result:
#         reviews = json_result["body"]
#         for review in reviews:
#             review_doc = review["doc"]
#             review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
#                                    id=review_doc["id"], review=review_doc["review"], purchase_date=review_doc["purchase_date"],
#                                    car_make=review_doc["car_make"], car_model=review_doc["car_model"], car_year=review_doc["car_year"],
#                                    sentiment=review_doc["sentiment"])
#             review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             results.append(review_obj)

#         return results
def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    print('json_result from line 54',json_result)

    if json_result:
        dealers = json_result["body"]
    
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],  short_name=dealer_doc["short_name"],full_name=dealer_doc["full_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    # print(json_result)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
    return response
