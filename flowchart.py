

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
from bs4 import BeautifulSoup


st.title('10th Planet System')
got_net = Network(height="100%",width='100%', bgcolor="black", font_color="white", select_menu=False)

# set the physics layout of the network
type_dict = {'Positional':'dot', 'Transition':'diamond','Submission':'star','Sweep':'square','Escape':'triangle'} 
system_dict = {'Lockdown':'red','Open Guard':'blue','Mount':'white','Rubber Guard':'purple','Bottom Mount':'teal', 'Back Mount':'hotpink','Truck':'gold', 'Side Mount':'green', 'Spiderweb':'aquamarine','X Guard':'cyan','Leg Entanglements':'salmon','Reverse Spiderweb':'orange'}
got_data = pd.read_csv("moves_flow.csv")
technique_db = pd.read_csv('technique_db.csv')
technique_db = technique_db.set_index('Technique')

src_counts = got_data['Source'].value_counts()
sources = got_data['Source']
targets = got_data['Target']



edge_data = zip(sources, targets)


for e in edge_data:



	src = e[0]
	dst = e[1]
	src_system = technique_db.loc[[src]]['System'][0]
	src_type = technique_db.loc[[src]]['Type'][0]
	dst_system = technique_db.loc[[dst]]['System'][0]
	dst_type = technique_db.loc[[dst]]['Type'][0]





	got_net.add_node(src, src, title=src, shape=type_dict[src_type], color=system_dict[src_system], value=src_counts[src])
	got_net.add_node(dst, dst, title=dst, shape=type_dict[dst_type], color=system_dict[dst_system], value=src_counts[src])
	got_net.add_edge(src, dst)

neighbor_map = got_net.get_adj_list()

#Generate network with specific layout settings
got_net.repulsion(node_distance=420, central_gravity=0.33,
                   spring_length=110, spring_strength=0.10,
                   damping=0.95)


# add neighbor data to node hover data
for node in got_net.nodes:

	node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
	node["value"] = len(neighbor_map[node["id"]])


got_net.save_graph('graphs/index.html')


# Opening the html file
HTMLFile = open("graphs/index.html", "r")

HTMLFile_styled = open('System_Flows/index_v2.html', 'r')
  
# Reading the file
index = HTMLFile.read()
index_styled = HTMLFile_styled.read()
  
# Creating a BeautifulSoup object and specifying the parser
S = BeautifulSoup(index, 'html.parser')
SS = BeautifulSoup(index_styled, 'html.parser')
  

graph_html = S.find_all('script')[-1]
SS.find_all('script')[-1].replace_with(graph_html)

with open("index.html", "w") as file:
    file.write(str(SS))

print('Full Graph Complete')


print('Starting Sub Graphs')
for key in system_dict.keys():
	got_net = Network(height="100%",width='100%', bgcolor="black", font_color="white", select_menu=False)


	sub_tech_db = technique_db[technique_db['System'] == key]
	sub_tech_db.loc[:,'Source']= list(sub_tech_db.index)


	sub_data = pd.merge(got_data, sub_tech_db, how='right')


	sub_data = sub_data.dropna()


	src_counts = sub_data['Source'].value_counts()
	sources = sub_data['Source']
	targets = sub_data['Target']



	edge_data = zip(sources, targets)


	for e in edge_data:



		src = e[0]
		dst = e[1]
		src_system = technique_db.loc[[src]]['System'][0]
		src_type = technique_db.loc[[src]]['Type'][0]
		dst_system = technique_db.loc[[dst]]['System'][0]
		dst_type = technique_db.loc[[dst]]['Type'][0]





		got_net.add_node(src, src, title=src, shape=type_dict[src_type], color=system_dict[src_system], value=src_counts[src])
		got_net.add_node(dst, dst, title=dst, shape=type_dict[dst_type], color=system_dict[dst_system], value=src_counts[src])
		got_net.add_edge(src, dst)

	neighbor_map = got_net.get_adj_list()

	#Generate network with specific layout settings
	got_net.repulsion(node_distance=420, central_gravity=0.33,
	                   spring_length=110, spring_strength=0.10,
	                   damping=0.95)


	for node in got_net.nodes:

		node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
		node["value"] = len(neighbor_map[node["id"]])


	#got_net.show("10thPlanetSystem.html")
	got_net.save_graph('graphs/'+key+'.html')

	# Opening the html file
	HTMLFile = open('graphs/'+key+'.html', "r")

	HTMLFile_styled = open('Styled/'+key+'.html', 'r')
	  
	# Reading the file
	index = HTMLFile.read()
	index_styled = HTMLFile_styled.read()
	  
	# Creating a BeautifulSoup object and specifying the parser
	S = BeautifulSoup(index, 'html.parser')
	SS = BeautifulSoup(index_styled, 'html.parser')
	  

	graph_html = S.find_all('script')[-1]
	SS.find_all('script')[-1].replace_with(graph_html)

	with open('System_Flows/'+key+".html", "w") as file:
	    file.write(str(SS))

print('Sub Graphs Complete')





