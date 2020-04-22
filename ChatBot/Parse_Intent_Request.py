from model import Model
from MakeRichResponse import MakeRichResponse


class Parse_Intent_Request:
    def parse_phone_Intent(self, phone_number,data_to_store):
        model=Model()
        value_to_return_dict = Model().check_phone_format(phone_number)

        if value_to_return_dict["status"] == "1":
            quick_rplies_list = [
                ["World Data","Total world data"],
                ["India Data","Total india data"],
                ["Count by Age","Case By Age"]]
            final_response = MakeRichResponse().create_img_card_response(value_to_return_dict["message"],"","",
                                                                     quick_rplies_list)
        else:
            final_response = {'fulfillmentText': value_to_return_dict["message"]}

        data_to_store["response"] = value_to_return_dict["message"]
        model.log_data_in_db(data_to_store)
        return final_response
