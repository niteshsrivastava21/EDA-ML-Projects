import smtplib
import pymongo
import configparser
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import random
from RapidAPI import RapidAPI
from MakeRichResponse import MakeRichResponse



class Model:

    def get_n_states_from_list(self, k=3):
        state_code = Model().get_config_data("state_list", "state_code")
        state_code_array = str(state_code).split(",")
        state_name = Model().get_config_data("state_list", "state_name")
        state_name_array = str(state_name).split(",")
        dict_value = dict(zip(state_code_array, state_name_array))
        list_val = random.choices(list(dict_value.values()), k=k)
        return list_val

    def get_ysterday_date(self):
        today = date.today()
        # Yesterday date
        yesterday = today - timedelta(days=1)
        return yesterday

    def get_config_data(self, parent_tag, child_tag):
        config = configparser.ConfigParser()
        config.read("config.ini")
        value_to_return = config[parent_tag][child_tag]
        return value_to_return

    def send_email_process(self, email_addr, person_name):
        print("in sesd email", email_addr)
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            host_name = config["email_params"]["host"]
            port_num = int(config["email_params"]["port"])
            user_name = config["email_params"]["user"]
            password = config["email_params"]["password"]
            subject = config["email_params"]["subject"]
            message_template = open("email_body.html").read()
            # message_template="Dear PERSON_NAME, how are you?"
            msg = MIMEMultipart()  # create a message
            # add in the actual person name to the message template
            message = message_template.replace("PERSON_NAME", person_name)
            msg['Subject'] = subject
            msg['From'] = user_name
            msg['To'] = email_addr
            msg.attach(MIMEText(message, 'html'))
            session = smtplib.SMTP(host_name, port_num)  # use gmail with port
            session.starttls()  # enable security
            session.login(user_name, password)  # login with mail_id and password
            text = msg.as_string()
            session.sendmail(user_name, email_addr, text)
            # session.send_message(text)
            session.quit()
            return "Dear {0}, An Email is sent to {1}. In case if you don't receive, please refer https://www.mohfw.gov.in/pdf/FAQ.pdf.".format(person_name, email_addr)
        except Exception as e:
            return "Email not sent to {0}. Error occured {1}".format(email_addr, e)

    def log_data_in_db(self, data_dict):
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            host_name = config["db_aprams"]["db_host"]
            db_name = config["db_aprams"]["db_name"]
            db_collection = config["db_aprams"]["db_collection"]
            myclient = pymongo.MongoClient(host_name)
            mydb = myclient[db_name]
            mycol = mydb[db_collection]
            data_dict["identifier"] = "googlebot"
            mydict = data_dict
            x = mycol.insert_one(mydict)
        except Exception as e:
            print(str(e))

    def parse_request(self, output_context_list):
        final_params = {}
        if not len(output_context_list) == 0:
            for each_opt_cntxt in output_context_list:
                parameter_dict = dict(each_opt_cntxt["parameters"])
                parameter_dict_keys = parameter_dict.keys()
                for each_param_dict_key in parameter_dict_keys:
                    value = str(parameter_dict[each_param_dict_key])
                    if not each_param_dict_key in final_params.keys():
                        if not len(value) == 0:
                            final_params[each_param_dict_key] = value

        return final_params


    # function for responses
    def check_phone_format(self, phone_number):
        if len(phone_number) == 0:
            return {"status": "0", "message": "I am still waiting to see your phone number"}
        elif not (phone_number.isdigit()):
            return {"status": "0", "message": "I am expecting phone number in numeric format only"}
        elif len(phone_number) != 10:
            return {"status": "0", "message": "Phone number must be of 10 digits"}
        else:
            return {"status": "1", "message": "Thanks a lot. Your are ready to get information"}



    def getWorldDataFulfillmentmessage(self,data_to_store):
        img_url = self.get_config_data("image_url", "world_distribution_img_url")
        yesterday_date = self.get_ysterday_date()
        img_url = img_url.format(yesterday_date)
        quick_replies_list = [["Cases for India", "Total india data"], ["Case By Age", "Case By Age"],
                             ["About COVID-19?", "About COVID-19?"]]
        word_data_txt = RapidAPI().get_world_covid_count()
        final_response = MakeRichResponse().create_img_card_response(word_data_txt, img_url,
                                                                     "COVID-19 Distribution across World",
                                                                     quick_replies_list)

        return final_response

    def getIndiaDataFulfillmentmessage(self,data_to_store):
        live_min_page_url = self.get_config_data("image_url", "live_mint_page_url")
        html_entity_type = self.get_config_data("image_url", "html_entity_type")
        html_entity_name = self.get_config_data("image_url", "html_entity_name")
        html_entity_value = self.get_config_data("image_url", "html_entity_value")
        img_url = RapidAPI().get_image_url(url=live_min_page_url, html_entity_type=html_entity_type,
                                           html_entity_name=html_entity_name, html_entity_value=html_entity_value)
        quick_replies_list = [["Cases in Delhi", "delhi data"], ["Safety Tips", "safety tips"]]
        return_data = RapidAPI().get_India_Count()
        final_response = MakeRichResponse().create_img_card_response(return_data, img_url, "Covid cases in India",
                                                                     quick_replies_list)
        data_to_store["response"] = return_data
        data_to_store["image_url"] = img_url
        self.log_data_in_db(data_to_store)
        return final_response

    def getIndiaStatesFullfillmentmessage(self, state_name_query, query_entitiy_type,data_to_store):
        rapidApi=RapidAPI()
        str_to_return = rapidApi.getStatsbasedData(state_name_query, query_entitiy_type)
        next_state_list = self.get_n_states_from_list(2)
        list_to_show = [["Cases in {}".format(i), "Cases in {}".format(i)] for i in next_state_list]
        list_to_show.append(["India Cases", "Total india data"])
        final_response = MakeRichResponse().create_img_card_response(str_to_return, "", "", list_to_show)
        data_to_store["response"] = str_to_return
        self.log_data_in_db(data_to_store)
        return final_response
