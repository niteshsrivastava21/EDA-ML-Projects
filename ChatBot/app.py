import asyncio

from flask import Flask, request, make_response, jsonify,Response
from lex_model import lex_model

from model import Model
from MakeRichResponse import MakeRichResponse
from datetime import date
from RapidAPI import *
from Parse_Intent_Request import Parse_Intent_Request
import json


app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook1():
    req = request.get_json(silent=True, force=True)
    return make_response(jsonify(parse_results(req)))


@app.route('/webhook_lex', methods=['GET', 'POST'])
def webhook_lex_fn():
    print("hello")
    if request.json["action_name"] is not None:
        action_name = request.json["action_name"]
        data_to_Store={}
        if action_name == "check_phone_format":
            phone_number=request.json["phone-number"]
            phone_check_response=lex_model.parse_phone_format(phone_number= phone_number,data_to_store= data_to_Store)
            return Response(phone_check_response)
        elif action_name == "get_covid_data":
            state_name="india"
            case_type_activity="all"
            if request.json["state_name"] is not None:
                state_name = request.json["state_name"]
            if request.json["case_type"] is not None:
                case_type_activity = request.json["case_type"]

            if state_name.lower() == "world":
                response_message=lex_model.getWorldCovidData(data_to_store=data_to_Store)
            elif state_name.lower()=="india":
                response_message = lex_model.getIndiaCovidData(data_to_store=data_to_Store)
            else:
                response_message= lex_model.getStateBasedData(state_name,case_type_activity,data_to_store=data_to_Store)
            return Response(response_message)
        elif "showDemographicDistribution" in action_name:
            response_message=lex_model.getDemographicDistribution(data_to_Store)
            return response_message
        elif "getDosDonts" in action_name:
            email_add = "nitesh@ahs.com"
            final_response=lex_model.getDosAndDonts(data_to_Store,email_add)
            return final_response
        if "sendEmailInfo" in action_name:
            model=Model()
            email_add="niteshsrivastava21@gmail.com"
            person_name="Nitesh"
            loop_event=asyncio.new_event_loop()
            loop_event.set_debug(True)
            asyncio.set_event_loop(loop_event)
            loop_event.create_task(lex_model.send_email_process(email_addr=email_add, person_name=person_name,data_to_store=data_to_Store))
            email_msg="Dear {0}, An Email is sent to {1}. In case if you dont receive, please refer https://www.mohfw.gov.in/pdf/FAQ.pdf.".format(person_name, email_add)
            next_state_list = model.get_n_states_from_list(2)
            list_to_show = ["Cases in {}".format(i) for i in next_state_list]
            list_to_show.append("India Cases")
            final_response = "{'button1':'" + list_to_show[0] + "','button2':'" + list_to_show[1] + \
                             "','button3':'" + list_to_show[2] + "'," \
                                                                 "'message':'"+email_msg+"'}"
            return final_response




def parse_results(req):
    model = Model()
    parse_intent_request = Parse_Intent_Request()
    if req is None:
        return {'fulfillmentText': "Not a valid request"}
    else:
        action_name = req.get('queryResult').get('action')
        parameters = req.get('queryResult').get('parameters')
        query = req.get('queryResult').get('queryText')
        data_to_store = {}
        output_context_list = req.get('queryResult').get('outputContexts')
        context_param = model.parse_request(output_context_list)
        print(query)
        data_to_store["query"] = query
        if "checkfoneformat" in action_name:
            phone_number = parameters["phone-number"]
            phone_intent_response = parse_intent_request.parse_phone_Intent(phone_number=phone_number,
                                                                            data_to_store=data_to_store)

            return phone_intent_response
        if "getCovidCases" in action_name:
            state_name_query = "india"
            query_entitiy_type = "All"
            if not len(parameters["state_name"]) == 0:
                state_name_query = parameters["state_name"]
            elif not len(context_param["state_name"]) == 0:
                state_name_query = context_param["state_name"]

            if ("case_type_entity" in parameters.keys()) and (not len(parameters["case_type_entity"]) == 0):
                query_entitiy_type = parameters["case_type_entity"]
            elif ("case_type_entity" in context_param.keys()) and (not len(context_param["case_type_entity"]) == 0):
                query_entitiy_type = context_param["case_type_entity"]

            if state_name_query == "world":
                final_response = model.getWorldDataFulfillmentmessage(data_to_store)
            elif state_name_query == "india":
                final_response = model.getIndiaDataFulfillmentmessage(data_to_store)
            else:
                final_response = model.getIndiaStatesFullfillmentmessage(state_name_query, query_entitiy_type,
                                                                         data_to_store)

            return final_response
        if "showDemographicDistribution" in action_name:
            img_url = model.get_config_data("image_url", "india_today_demographic_distib")
            quick_rplies_list = [["Cases for India", "cases for india"], ["Safety Tips",
                                                                          "safety tips"]]
            final_response = MakeRichResponse().create_img_card_response("Demographic Distribution in India", img_url,
                                                                         "Demographic Distribution in India",
                                                                         reply_lists=quick_rplies_list)
            data_to_store["response"] = "Demographic Distribution in India"
            data_to_store["image_url"] = img_url

            model.log_data_in_db(data_to_store)
            return final_response
        if "getDosDonts" in action_name:
            email_add = ""
            if "email-addr" in context_param.keys():
                email_add = context_param["email-addr"]
            elif "c_email_addr" in context_param.keys():
                email_add = context_param["c_email_addr"]
            img_url = model.get_config_data("image_url", "dont_dos")
            quick_rplies_list = [["Email to {}".format(email_add), "Email to {}".format(email_add)],
                                 ["Cases for India", "cases for india"]]
            final_response = MakeRichResponse().create_img_card_response("Dos and Don\'ts from MoHFW", img_url,
                                                                         "Dos and Don\'ts from MoHFW",
                                                                         reply_lists=quick_rplies_list)
            data_to_store["response"] = "Dos and Don'ts from MoHFW"
            data_to_store["image_url"] = img_url
            data_to_store["email"] = email_add

            model.log_data_in_db(data_to_store)
            return final_response

        if "sendEmailInfo" in action_name:
            email_add = context_param["c_email_addr"]
            if len(email_add) == 0:
                email_add = context_param["email-addr"]
            person_name = context_param["person_name"]
            response_value = model.send_email_process(email_addr=email_add, person_name=person_name)

            data_to_store["response"] = "response_value"
            data_to_store["email"] = email_add

            model.log_data_in_db(data_to_store)
            return {'fulfillmentText': response_value}


if __name__ == '__main__':
    print("here")
    app.run()
