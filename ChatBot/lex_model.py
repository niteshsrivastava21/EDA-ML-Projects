import asyncio
import functools

from model import Model
import configparser
import pymongo
import json
from RapidAPI import RapidAPI
from threading import Thread



def log_data_in_db(data_to_store):
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        host_name = config["db_aprams_lex"]["db_host"]
        db_name = config["db_aprams_lex"]["db_name"]
        db_collection = config["db_aprams_lex"]["db_collection"]
        myclient = pymongo.MongoClient(host_name)
        mydb = myclient[db_name]
        mycol = mydb[db_collection]
        data_to_store["identifier"] = "lex_bot"
        mydict = data_to_store
        x = mycol.insert_one(mydict)
    except Exception as e:
        print(str(e))


class lex_model:
    def parse_phone_format(phone_number="1234",
                           data_to_store=None):
        model = Model()
        value_to_return_dict = Model().check_phone_format(phone_number)
        # final_response="'status':{0},'def':{1}".format(value_to_return_dict["status"],value_to_return_dict["message"])
        final_response = "{'status':" + value_to_return_dict["status"] + ",'message':'" + value_to_return_dict[
            "message"] + "'}"
        data_to_store["response"] = value_to_return_dict["message"]
        log_data_in_db(data_to_store)
        return final_response

    def getWorldCovidData(data_to_store):
        model = Model()
        img_url = model.get_config_data("image_url", "world_distribution_img_url")
        yesterday_date = model.get_ysterday_date()
        img_url = img_url.format(yesterday_date)
        word_data_txt = RapidAPI().get_world_covid_count()
        final_response = "{'button1':'Cases for India','button2':'Case By Age','button3':'About COVID-19?'," \
                         "'message':'" + word_data_txt + "','img_url':'" + img_url + "'}"
        data_to_store["response"] = final_response
        log_data_in_db(data_to_store)
        return final_response

    def getIndiaCovidData(data_to_store):
        model = Model()
        live_min_page_url = model.get_config_data("image_url", "live_mint_page_url")
        html_entity_type = model.get_config_data("image_url", "html_entity_type")
        html_entity_name = model.get_config_data("image_url", "html_entity_name")
        html_entity_value = model.get_config_data("image_url", "html_entity_value")
        img_url = RapidAPI().get_image_url(url=live_min_page_url, html_entity_type=html_entity_type,
                                           html_entity_name=html_entity_name, html_entity_value=html_entity_value)
        quick_replies_list = [["Cases in Delhi", "delhi data"], ["Safety Tips", "safety tips"]]
        india_data = RapidAPI().get_India_Count()

        final_response = "{'button1':'Cases in Delhi','button2':'Safety Tips','button3':'About COVID-19?'," \
                         "'message':'" + india_data + "','img_url':'" + img_url + "'}"
        data_to_store["response"] = final_response
        log_data_in_db(data_to_store)
        return final_response

    def getStateBasedData(state_name, case_type_activity, data_to_store):
        rapidApi = RapidAPI()
        model = Model()
        if case_type_activity.lower() == "total":
            case_type_activity = "all"
        state_data = rapidApi.getStatsbasedData(state_name, case_type_activity)
        next_state_list = model.get_n_states_from_list(2)
        list_to_show = ["Cases in {}".format(i) for i in next_state_list]
        list_to_show.append("India Cases")
        final_response = "{'button1':'" + list_to_show[0] + "','button2':'" + list_to_show[1] + \
                         "','button3':'" + list_to_show[2] + "'," \
                                                             "'message':'" + state_data + "'}"
        data_to_store["response"] = final_response
        log_data_in_db(data_to_store)
        return final_response

    def getDemographicDistribution(data_to_store):
        model = Model()
        img_url = model.get_config_data("image_url", "india_today_demographic_distib")
        list_to_show = ["Cases for India", "Safety Tips", "What is COVID-19?"]
        final_response = "{'button1':'" + list_to_show[0] + "','button2':'" + list_to_show[1] + \
                         "','button3':'" + list_to_show[2] + "'," \
                                                             "'img_url':'" + img_url + "'}"
        data_to_store["response"] = "Demographic Distribution in India"
        data_to_store["image_url"] = img_url
        log_data_in_db(data_to_store)
        return final_response

    def getDosAndDonts(data_to_store, email_add):
        model = Model()
        img_url = model.get_config_data("image_url", "dont_dos")
        list_to_show = ["Email to {}".format(email_add),
                        "Cases for India"]

        final_response = "{'button1':'" + list_to_show[0] + "','button2':'" + list_to_show[1] + \
                         "','img_url':'" + img_url + "'}"
        data_to_store["response"] = "Dos and Don'ts from MoHFW"
        data_to_store["image_url"] = img_url
        data_to_store["email"] = email_add

        log_data_in_db(data_to_store)
        return final_response

    async def send_email_process(email_addr, person_name, data_to_store):
        print("in send email process")
        model = Model()
        # await asyncio.run(model.send_email_process(email_addr=email_addr, person_name=person_name))
        bound=functools.partial(model.send_email_process(email_addr=email_addr, person_name=person_name))
        loop=asyncio.get_event_loop()
        await loop.run_in_executor(None,bound)
        repnse_value = "A email is sent"
        data_to_store["response"] = repnse_value
        data_to_store["email"] = email_addr
        log_data_in_db(data_to_store)

        # return final_response
