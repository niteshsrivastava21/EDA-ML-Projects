import requests
from BsSoupModel import BsSoupModel


class RapidAPI:

    ## function to get Covid data based on state names in India
    def getStatsbasedData(self, state_name, case_type_entity):
        url = "https://covid19india.p.rapidapi.com/getStateData/{0}".format(state_name)

        headers = {
            'x-rapidapi-host': "covid19india.p.rapidapi.com",
            'x-rapidapi-key': "6209f104damsh4bc552882960a5ap1e0542jsnecb749b0e397"
        }

        response = requests.request("GET", url, headers=headers)
        json_response = response.json()
        actual_response = json_response.get('response')
        if (case_type_entity.lower() == "all") or (case_type_entity.lower() == "all details"):
            active_case = actual_response["active"]
            confirmed_case = actual_response["confirmed"]
            recovered_cases = actual_response["recovered"]
            death_case = actual_response["deaths"]
            name_state = actual_response["name"]
            value_to_return = "Total Confirmed cases in {4} are {0}, Active cases {1}, Recovered cases {2} and " \
                              "Total deaths {3}" \
                .format(confirmed_case, active_case, recovered_cases, death_case, name_state)
            return value_to_return
        else:
            value_to_return = actual_response[case_type_entity.lower()]
            name_state = actual_response["name"]
            return "{0} cases in {1} are {2}".format(case_type_entity, name_state, value_to_return)

    def get_image_url(slef, url, html_entity_type, html_entity_name, html_entity_value):
        bsSoupModel = BsSoupModel()
        page_soup = bsSoupModel.get_page_soup(url)
        image_tages = page_soup.find_all(html_entity_type, {html_entity_name: html_entity_value})
        image_url = image_tages.__getitem__(0).attrs["data-src"]
        return image_url

    def get_world_covid_count(self):
        url = "https://covid-19-data.p.rapidapi.com/totals"

        querystring = {"format": "json"}

        headers = {
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
            'x-rapidapi-key': "6209f104damsh4bc552882960a5ap1e0542jsnecb749b0e397"
        }
        json_response = requests.request("GET", url, headers=headers)
        if json_response.status_code == 200:
            actual_response_list = json_response.json()
            actual_response = actual_response_list[0]
            confirmed_case = actual_response["confirmed"]
            critical = actual_response["critical"]
            recovered_cases = actual_response["recovered"]
            death_case = actual_response["deaths"]
            value_to_return = "Total Confirmed cases in {4} are {0}, Critial cases {1}, Recovered cases {2} and " \
                              "Total deaths {3}" \
                .format(confirmed_case, critical, recovered_cases, death_case, "World")
            return value_to_return

        else:
            return "Not able to get data. Please try again."

    ## to get count of India
    def get_India_Count(self):
        url = "https://api.rootnet.in/covid19-in/stats/latest"
        response = requests.request("GET", url)
        json_response = response.json()
        status = json_response.get('success')
        if status:
            actual_response = json_response.get('data')["summary"]
            confirmed_case=actual_response["total"]
            cofirm_case_indian=actual_response["confirmedCasesIndian"]
            confirmedCasesForeign=actual_response["confirmedCasesForeign"]
            recovered=actual_response["discharged"]
            deaths=actual_response["deaths"]
            value_to_return = "Total Confirmed cases in {5} are {0}, out of which Indians are {1} and Foreign Nationals are {2}. The recovered cases" \
                              " are {3} and total deaths are {4}.".format(confirmed_case, cofirm_case_indian,confirmedCasesForeign
                                                                         , recovered, deaths, "India")
        else:
            value_to_return="Not able to get the data. Please try again."
        return value_to_return
