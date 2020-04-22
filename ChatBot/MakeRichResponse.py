from df_response_lib import *


class MakeRichResponse:
    def makeResponse(self):
        tele_resp = telegram_response()
        main_resp = fulfillment_response()
        response = tele_resp.image_response(
            "https://www.ecdc.europa.eu/sites/default/files/styles/is_full/public/images/novel-coronavirus-COVID-19"
            "-geographical-distribution-world-2020-04-17.jpg")
        hi = fulfillment_response(self, [None, response, None])
        val_to_return = main_resp.fulfillment_messages(self, hi)
        return val_to_return

    def create_card_response(self, titletext, button_list):
        fulfillmentText = titletext
        ff_response = fulfillment_response()
        tegram_object = telegram_response()
        fb_object = facebook_response()
        slk_object = slack_response()
        # image = ['https://imagepath.com/path.png', 'sample image']
        # buttons = [
        #     ['button_1', 'https://www.google.com/'],
        #     ['button 2', 'https://www.facebook.com/']
        # ]
        buttons = [[i, i] for i in button_list]
        tog_card = tegram_object.card_response(title=titletext, buttons=buttons)
        fb_card = fb_object.card_response(title=titletext, buttons=buttons)
        slk_card = slk_object.card_response(title=titletext, buttons=buttons)
        ff_text = ff_response.fulfillment_text(fulfillmentText)
        ff_messages = ff_response.fulfillment_messages([fb_card, tog_card, slk_card])
        reply = ff_response.main_response(ff_text, ff_messages)
        return reply

    def create_quick_replies(self, title, reply_lists):
        ff_response = fulfillment_response()
        tegram_object = telegram_response()
        fb_object = facebook_response()
        slk_object = slack_response()
        tog_quick_reply = tegram_object.quick_replies(title=title, quick_replies_list=reply_lists)
        fb_quick_reply = fb_object.quick_replies(title=title, quick_replies_list=reply_lists)
        slk_quick_reply = slk_object.quick_replies(title=title, quick_replies_list=reply_lists)
        ff_text = ff_response.fulfillment_text(title)
        ff_messages = ff_response.fulfillment_messages([fb_quick_reply, tog_quick_reply, slk_quick_reply])
        reply = ff_response.main_response(ff_text, ff_messages)
        return reply

    def create_image_response(self, img_url, img_text):
        ff_response = fulfillment_response()
        tegram_object = telegram_response()
        fb_object = facebook_response()
        slk_object = slack_response()
        tog_img_resp = tegram_object.image_response(url=img_url)
        fb_img_resp = fb_object.image_response(url=img_url)
        slk_img_resp = slk_object.image_response(url=img_url)
        ff_text = ff_response.fulfillment_text(img_text)
        ff_messages = ff_response.fulfillment_messages([fb_img_resp, tog_img_resp, fb_img_resp])
        reply = ff_response.main_response(ff_text, ff_messages)

    def create_img_card_response(self, title, img_url, img_text, reply_lists):
        ff_response = fulfillment_response()
        tegram_object = telegram_response()
        fb_object = facebook_response()
        slk_object = slack_response()
        ff_msg_list = []
        if not len(img_url) == 0:
            tog_img_resp = tegram_object.image_response(url=img_url)
            fb_img_resp = fb_object.image_response(url=img_url)
            slk_img_resp = slk_object.image_response(url=img_url)
            ff_text = ff_response.fulfillment_text(img_text)
            # ff_messages = ff_response.fulfillment_messages([fb_img_resp, tog_img_resp, slk_img_resp])
            ff_msg_list.append(fb_img_resp)
            ff_msg_list.append(tog_img_resp)
            ff_msg_list.append(slk_img_resp)

        tog_quick_reply = tegram_object.card_response(title, reply_lists)
        fb_quick_reply = fb_object.card_response(title, reply_lists)
        slk_quick_reply = slk_object.card_response(title, reply_lists)
        ff_msg_list.append(slk_quick_reply)
        ff_msg_list.append(fb_quick_reply)
        ff_msg_list.append(tog_quick_reply)

        # tog_quick_reply = tegram_object.quick_replies(title=title, quick_replies_list=reply_lists)
        # fb_quick_reply = fb_object.quick_replies(title=title, quick_replies_list=reply_lists)
        # slk_quick_reply = slk_object.quick_replies(title=title, quick_replies_list=reply_lists)
        ff_text = ff_response.fulfillment_text(title)
        ff_messages = ff_response.fulfillment_messages(ff_msg_list)
        return ff_messages

    def create_Text_Response(self, data_to_set):
        ff_response = fulfillment_response()
        tegram_object = telegram_response()
        fb_object = facebook_response()
        slk_object = slack_response()
        tog_img_resp = tegram_object.text_response(data_to_set)
        fb_img_resp = fb_object.text_response(data_to_set)
        slk_img_resp = slk_object.text_response(data_to_set)
        ff_text = ff_response.fulfillment_text(data_to_set)
        ff_messages = ff_response.fulfillment_text(data_to_set)
        return ff_messages
