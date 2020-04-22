from model import Model
import configparser
import pymongo
import json


class lex_model:
    def parse_phone_format(phone_number="1234",
                           data_to_store=None):
        model = Model()
        value_to_return_dict = Model().check_phone_format(phone_number)
        # final_response="'status':{0},'def':{1}".format(value_to_return_dict["status"],value_to_return_dict["message"])
        final_response="{'status':" + value_to_return_dict["status"] + ",'message':'" + value_to_return_dict["message"] + "'}"


        data_to_store["response"] = value_to_return_dict["message"]
        model.log_data_in_db(data_to_store)
        return final_response

    def log_data_in_db(self, data_dict):
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            host_name = config["db_aprams_lex"]["db_host"]
            db_name = config["db_aprams_lex"]["db_name"]
            db_collection = config["db_aprams_lex"]["db_collection"]
            myclient = pymongo.MongoClient(host_name)
            mydb = myclient[db_name]
            mycol = mydb[db_collection]
            data_dict["identifier"]="lex_bot"
            mydict = data_dict
            x = mycol.insert_one(mydict)
        except Exception as e:
            print(str(e))