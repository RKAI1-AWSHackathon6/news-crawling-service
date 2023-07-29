import json
import requests


def add_token_list(json_file):
    url = "http://10.101.14.21:8000/api/v1/tokens"
    with open(json_file, "r") as f:
        token_list = json.load(f)
        data_token_list = token_list["data"]
        print(f"Processing {len(data_token_list)} tokens")
        for _id in data_token_list.keys():
            token_data = data_token_list[_id]
            payload = {"name": token_data["name"], "symbol": token_data["symbol"], "icon": token_data["logo"]}
            print(f"Processing {token_data['name']}")
            response = requests.post(url, json=payload)
            print(response.status_code)
            
if __name__=="__main__":
    add_token_list("/home/tannn/4t_hdd1/projects/rk-aws/test.json")
            
        