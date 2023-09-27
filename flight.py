import pickle
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://www.devdiscourse.com/remote.axd?https://devdiscourse.blob.core.windows.net/devnews/17_08_2022_14_11_33_7985115.jpg?width=920&format=webp');
    background-size: cover;
}
[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.0);
}
h1{
    color: indianred;
}
table{
    background-color: #00425A;
    text-align: center;
}

</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("Airlines Route Optimization System")
with open('airport.pkl', 'rb') as c:
    airport = pickle.load(c)   
with open('graph.pkl', 'rb') as c:
    nod = pickle.load(c)
with open('airport_code.pkl', 'rb') as f:
    airportname = pickle.load(f)
with open('state_code.pkl', 'rb') as f:
    statename = pickle.load(f)
with open('nearairport.pkl', 'rb') as f:
    nearairport = pickle.load(f)

# print no of Airports and Flights
st.header("Number Of Airports: ")
st.write(nod.number_of_nodes())
st.header("Number Of Flights: ")
st.write(nod.number_of_edges())


# listing busiest Airports
st.header("Busiest Airports ")
air1 = st.slider('Enter The No Of Airports Required', 0, 130, 25)
if st.button('Find Stations'):
    l = list(nod.degree(list(nod.nodes())))
    l.sort(key=lambda x: x[1], reverse=True)
    # top 10 nodes with highest degree (Airports with most number of Flights)
    busy=l[:air1]
    bstation = pd.DataFrame(busy, columns=['Airports', 'No Of Flights'])
    st.table(bstation)

# Centrality Measure Calculation
G2 = nx.Graph(nod)
st.header("Centrality Measure Calculation")
centrality = st.selectbox('Select Centrality Type', ('Degree Centrality',
                          'Closeness Centrality', 'Betweenness Centrality', 'Eigenvector Centrality'))
if st.button('Calculate'):
    if centrality == 'Degree Centrality':
        st.write("Degree Centrality: ", nx.degree_centrality(nod))
    elif centrality == 'Closeness Centrality':
        st.write("Closeness Centrality: ", nx.closeness_centrality(nod))
    elif centrality == 'Betweenness Centrality':
        st.write("Betweenness Centrality: ", nx.betweenness_centrality(nod))
    elif centrality == 'Eigenvector Centrality':
        st.write("Eigenvector Centrality: ", nx.eigenvector_centrality(G2))


# Shortest Path Calculation
st.header("Shortest Path Calculation For Flight Route")
option1 = st.selectbox('Select Source Airport', airportname.values())
option2 = st.selectbox('Select Destination Airport', airportname.values())

if st.button('Find Route'):
    # route()
    st.write("Route Found")
    st.write("Route is:")
    p = nx.shortest_path(nod,source=[i for i in airportname if airportname[i]==option1][0],target=[i for i in airportname if airportname[i]==option2][0], weight="l")
    q = nx.shortest_path_length(nod,source=[i for i in airportname if airportname[i]==option1][0],target=[i for i in airportname if airportname[i]==option2][0], weight="l")
    # p = nx.shortest_path(nod,source=option1,target=option2, weight="l")
    # q = nx.shortest_path_length(nod,source=option1,target=option2, weight="l")
    #Convert List To Table And Display
    temp=[]
    for z in p:
        temp.append(z)
    shrt_path = pd.DataFrame(temp)
    st.table(shrt_path)
    st.write('Distance travel is: ', q, 'km')


# # Clustering Coefficient Calculation
# G2 = nx.Graph(nod)
# st.header("Clustering Coefficient Calculation")
# if st.button('Calculate Clustering Coefficient'):
#     st.write("Clustering Coefficient: ", nx.average_clustering(G2))

# # Bridges Calculation
# st.header("Bridges Calculation")
# if st.button('Calculate Bridges'):
#     st.write("Bridges: ", list(nx.bridges(G2, root='IAD')))
#     st.write("Number of Bridges: ", len(list(nx.bridges(G2, root='IAD'))))

# Articulation Points Calculation
st.header("Articulation Points Calculation")
if st.button('Calculate Articulation Points'):
    st.write("Articulation Points: ", list(nx.articulation_points(G2)))
    st.write("Number of Articulation Points: ",
             len(list(nx.articulation_points(G2))))


#Efficiency Calculation
st.header("Efficiency Calculation")
if st.button('Calculate Global Efficiency'):
    st.write("Efficiency: ", nx.global_efficiency(G2))

G0 = nx.Graph(nod)
su1 = st.selectbox('Select Source Airport:', airport)
des1 = st.selectbox('Select Destination1 Airport:', airport)
des2 = st.selectbox('Select Destination2 Airport:', airport)
if st.button('Calculate Efficiency'):
    st.write("Efficiency: ", nx.efficiency(G0, su1, des1))
    st.write("Efficiency: ", nx.efficiency(G0, su1, des2))
# efficiency = nx.efficiency(G0, "ATL", "YUM")



#Stations In A State
st.header("Find Airports In A State")
option = st.selectbox('Select State',statename.values())
if st.button('Find Airports:'):
    # route()
    st.write("Airports Found")
    st.write("Airports are:")
    temp={}
    for z in statename:
        if statename[z]==option:
            temp[airportname[z]]=nod.degree(z)
    #Remove non numeric values from temp values
    temp = {k: v for k, v in temp.items() if isinstance(v, int)}
    #Sort temp based on values
    temp = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1],reverse=True)}

    st.write(temp)
    # state_airport = pd.DataFrame.from_dict(temp, orient='index', columns=['Airport','No Of Flights'])
    # st.table(state_airport)

#Airport withing a distance from a particular airport
st.header("Find Airports Nearer From A Particular Airport")
option8 = st.selectbox('Select Airport',airportname.values())
dist = st.slider('Enter The No Of Airports', 0, 20, 5)
if st.button('Find Airports Nearer:'):
    # route()
    st.write("Airports Found")
    st.write("Airports are:")
    n=nearairport[[i for i in airportname if airportname[i]==option8][0]].sort_values().head(dist)

    #convert n to dictionary
    n=n.to_dict()
    blank={}
    for i in n:
        blank[i]=int(n[i][0])
    state_airport = pd.DataFrame.from_dict(blank, orient='index', columns=['No Of Flights'])
    st.table(state_airport)
