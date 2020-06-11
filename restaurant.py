import os
import requests
import json
import datetime
import pandas as pd

ZOMATO_API_KEY=""
_headers={'user-key': ZOMATO_API_KEY}

city_url="https://developers.zomato.com/api/v2.1/cities?q="
collection_url="https://developers.zomato.com/api/v2.1/collections?city_id={city_id}&count=100"
search_url="https://developers.zomato.com/api/v2.1/search?entity_id={city_id}&entity_type=city&start={start}&count={count}&collection_id={collection_id}"

restaurant_detail={
    "id":"",
    "name":"",
    "average_cost_for_two":"",
    "price_range":"",
    "currency":"",
    "cuisines":"",
    "address": "",
    "locality": "",
    "city": "",
    "city_id": "",
    "latitude": "",
    "longitude": "",
    "zipcode": "",
    "country_id": "",
    "locality_verbose": "",
    "user_rating":""
    }

csv_cols=list(restaurant_detail.keys())

def get_city_id(city_name):
    """
    getting the city id
    using city name
    """
    city_id=0
    city_url_new=city_url+city_name
    resp=requests.get(city_url_new, headers=_headers)
    if resp.status_code == 200:
        api_resp=json.loads(resp.text)
        if "location_suggestions" in api_resp:
            if len(api_resp["location_suggestions"]) > 0:
                city_id=api_resp["location_suggestions"][0]["id"]
        return city_id
    else:
        raise requests.HTTPError


def get_collections_in_city(city_id):
    """
    get list of all restaurants
    in zomato collection
    """
    collection_ids=[]
    collection_url_new=collection_url.format(city_id=city_id)
    resp=requests.get(collection_url_new, headers=_headers)
    if resp.status_code == 200:
        api_resp=json.loads(resp.text)
        if len(api_resp["collections"]) > 0:
            collections=api_resp["collections"]
            for c in collections:
                coll=c["collection"]
                collection_ids.append({"collection_id": coll["collection_id"], "res_count": coll["res_count"]}) 
        return collection_ids
    else:
        raise requests.HTTPError
    

def search_restaurants_in_collection(city_id, collection_id, start, count):
    """
    search restaurant 
    collection wise
    """
    restaurantslist=[]
    search_url_new=search_url.format(city_id=city_id, collection_id=collection_id, start=start, count=count) 
    resp=requests.get(search_url_new, headers=_headers)
    if resp.status_code == 200:
        api_resp=json.loads(resp.text)
        if len(api_resp["restaurants"]) > 0:
            for _restaurant in api_resp["restaurants"]: 
                res_one=_restaurant["restaurant"] 
                rdetail=restaurant_detail.copy() 
                rdetail.update(res_one["location"]) 
                for i in rdetail: 
                    if i == "user_rating": 
                        if res_one[i]: 
                            rdetail[i]=res_one[i]["aggregate_rating"] 
                            continue 
                    if i in res_one: 
                        rdetail[i]=res_one.get(i) 
                restaurantslist.append(rdetail)
        return restaurantslist
    else:
        raise requests.HTTPError


def get_restaurants_in_collection(city_id, collection_d):
    """
    get restaurants 
    in collection
    """
    restaurantslistall=[]
    collection_id=collection_d["collection_id"]
    res_count=collection_d["res_count"]
    start=0
    count=20
    for i in range(0, res_count, 20):
        restaurantslist=search_restaurants_in_collection(city_id, collection_id, i, i+20)
        restaurantslistall.extend(restaurantslist)

    return restaurantslistall



if __name__ == "__main__":
    city_name="Indore"
    city_id=get_city_id(city_name)
    print("city_id:", city_id)
    collection_ids=get_collections_in_city(city_id)
    print("collection_ids:", collection_ids)

    for collection_d in collection_ids:
        restaurantslist=get_restaurants_in_collection(city_id, collection_d)
        df=pd.DataFrame(restaurantslist)
        df.to_csv('my_csv_indore.csv', mode='a', header=False, index=False)
    print("OK")
