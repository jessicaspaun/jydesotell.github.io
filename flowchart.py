

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network


st.title('10th Planet System')
got_net = Network(height="30%",width='100%', bgcolor="#222222", font_color="white", select_menu=True)

# set the physics layout of the network
type_dict = {'Positional':'dot', 'Transition':'diamond','Submission':'star','Sweep':'square','Escape':'triangle'} 
system_dict = {'Lockdown':'red','Open Guard':'blue','Mount':'white','Rubber Guard':'purple','Bottom Mount':'teal', 'Back Mount':'gray','Truck':'gold', 'Side Mount':'green', 'Spiderweb':'fuschsia','X Guard':'cyan','Leg Entanglements':'salmon','Reverse Spiderweb':'orange'}
got_data = pd.read_csv("moves_flow.csv")
technique_db = pd.read_csv('technique_db.csv')
technique_db = technique_db.set_index('Technique')

src_counts = got_data['Source'].value_counts()
sources = got_data['Source']
targets = got_data['Target']



edge_data = zip(sources, targets)

got_net.add_node(0, shape='image', image ="10pStPete.png", x=50, y=50, size=100)

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

# Generate network with specific layout settings
got_net.repulsion(node_distance=420, central_gravity=0.33,
                   spring_length=110, spring_strength=0.10,
                   damping=0.95)

# step = 50
# x = -300
# y = -250
# legend_nodes = [
#     (
#         num_actual_nodes + legend_node, 
#         {
#             'group': legend_node, 
#             'label': str(legend_node),
#             'size': 30, 
#             # 'fixed': True, # So that we can move the legend nodes around to arrange them better
#             'physics': False, 
#             'x': x, 
#             'y': f'{y + legend_node*step}px',
#             'shape': 'box', 
#             'widthConstraint': 50, 
#             'font': {'size': 20}
#         }
#     )
#     for legend_node in range(num_legend_nodes)
# ]

# add neighbor data to node hover data
for node in got_net.nodes:
	try:
		node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
		node["value"] = len(neighbor_map[node["id"]])
	except:
		print(node)

#got_net.show("10thPlanetSystem.html")
got_net.save_graph('index.html')

# Save and read graph as HTML file (on Streamlit Sharing)
# try:
# 	print('shared')
# 	path = '/tmp'
# 	got_net.save_graph(f'{path}/10thPlanetSystem.html')
# 	HtmlFile = open(f'{path}/10thPlanetSystem.html','r',encoding='utf-8')
# 	# Save and read graph as HTML file (locally)
# except:
# 	print('local')
# 	path = '.'
# 	got_net.generate_html('10thPlanetSystem.html')
# 	HtmlFile = open('10thPlanetSystem.html','r',encoding='utf-8')


# # Load HTML into HTML component for display on Streamlit
# #print(HtmlFile.read())
# components.html(HtmlFile.read(), height=1000, width=10000)



