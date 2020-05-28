from model import Model

model=Model()
state_data="hello"

next_state_list = model.get_n_states_from_list(2)
list_to_show = ["Cases in {}".format(i) for i in next_state_list]
list_to_show.append("India Cases")
final_response = "{'button1':'"+list_to_show[0]+"','button2':'"+list_to_show[1]+\
                 "','button3':'"+list_to_show[2]+"'," \
                 "'message':'" + state_data + "'}"
print(final_response)