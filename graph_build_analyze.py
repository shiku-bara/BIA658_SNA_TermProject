import pandas as pd
import pickle
import numpy as np
import os
import networkx as nx
import matplotlib.pyplot as plt
from nxviz.plots import ArcPlot

class DataFrameExtractor():

    year_to_movie_info_dict = None
    movie_info_pickle_file_path = None
    data_frame = None


    def __init__(self, movie_info_pickle_file_path, start_year=None, end_year=None):
        DataFrameExtractor.movie_info_pickle_file_path = movie_info_pickle_file_path
        self.cast_df = None
        self.degree_list=[]
        
        DataFrameExtractor.__load_pickle_object()
        self.cast_df = DataFrameExtractor.__extract_data_frame(start_year, end_year)
        
        self.graph_creation()
#        self.highest_degree_centrality()
#        self.degree_hist(start_year, end_year)
#        self.subgraph()
#        self.arcplot_graph()

    @staticmethod
    def __load_pickle_object():
        with open(DataFrameExtractor.movie_info_pickle_file_path, "rb") as f:
            DataFrameExtractor.year_to_movie_info_dict = pickle.load(f)

    @staticmethod
    def __extract_data_frame(start_year, end_year):
        year_list = sorted(DataFrameExtractor.year_to_movie_info_dict.keys())

        if not start_year:
            start_year = year_list[0]

        if not end_year:
            end_year = year_list[-1]
        
        print("Timeframe: {} to {}".format(str(start_year),str(end_year)))

        actor_names_pair_tuple_to_movie_list_dict = {}
        movie_info_column_name = None

        for year in range(int(start_year), int(end_year)+1):

            if year in DataFrameExtractor.year_to_movie_info_dict:

                movie_info = DataFrameExtractor.year_to_movie_info_dict[year]

                for actor_names_tuple, movie_details in movie_info.items():
                    if not movie_info_column_name:
                        movie_info_column_name = movie_details.keys()

                    if not actor_names_tuple in actor_names_pair_tuple_to_movie_list_dict:
                        actor_names_pair_tuple_to_movie_list_dict[actor_names_tuple] = movie_details
                        
                    else:
                        for detail_name, detail in movie_details.items():
                            actor_names_pair_tuple_to_movie_list_dict[actor_names_tuple][detail_name].extend(detail)


        column_names = ["actor_1", "actor_2"]
        column_names.extend(movie_info_column_name)
        column_names.append("weight")

        data_frame_in_list = []

        for actor_names_pair_tuple, movie_info in actor_names_pair_tuple_to_movie_list_dict.items():

            row = [actor_names_pair_tuple[0], actor_names_pair_tuple[1]]
            for detail in movie_info_column_name:
                if detail == "movie_id":
                    weight = len(movie_info[detail])

                row.append(movie_info[detail])

            row.append(weight)
            data_frame_in_list.append(row)

        DataFrameExtractor.data_frame = pd.DataFrame.from_records(data_frame_in_list, columns=column_names)
        
#        print(DataFrameExtractor.data_frame.iloc[1752])
        return DataFrameExtractor.data_frame
            

    def graph_creation(self):
        
        self.G = nx.Graph()
        
        for i, data in self.cast_df.iterrows():
            self.G.add_edge(data[0],data[1], weight = data[3], attr_dict={"Movies":data[2]})
            
        
        print ('Total Nodes: {}'.format(len(self.G.nodes())))
        print ('Total Edges: {}'.format(len(self.G.edges())))
        
        
        
    def highest_degree_centrality(self):
        a = 0
        b = 0
        for n, d in self.G.nodes(data=True):
            self.G.node[n]['degree'] = nx.degree(self.G,n)
            b = nx.degree(self.G,n)
            if b > a:
                a = b
            
        self.max_degree_centrality = max(nx.degree_centrality(self.G).values())
        
        for name, deg in nx.degree_centrality(self.G).items():
            if deg == self.max_degree_centrality:
                print("Actor with highest degree centrality - {} edges: {} ".format(a,name))
                
    
    def degree_hist(self, s_year, e_year):        
        for cast, deg in self.G.nodes(data=True):
            self.degree_list.append(self.G.node[cast]['degree'])
            
        plt.hist(self.degree_list)
        plt.xlabel('Number of Edges')
        plt.ylabel('Number of Nodes')
        plt.title('{}-{} \n Total Nodes (Actors): {} \n Total Edges (Connections): {}' \
                  .format(s_year,e_year,str(len(self.G.nodes())),str(len(self.G.edges()))))
        plt.show()
        
    def subgraph(self):
        node = [n for n, d in self.G.nodes(data=True) if n == 'Lee Phelps']
        
        for n in node:
            nbrs = self.G.neighbors(n)
            
        self.G_sub = self.G.subgraph(nbrs)
        
    def arcplot_graph(self):
        a = ArcPlot(self.G_sub, node_order='degree')
        a.draw()
        plt.show()
        
        
        
        
if __name__ == "__main__":
    pickle_obj = os.path.join(os.getcwd(),"movie_info.pkl")
    time_window = {0:[1914,1930],1:[1931,1940],2:[1941,1950],3:[1951,1960],4:[1961,1970],5:[1971,1980],6:[1981,1990], \
                   7:[1991,2000],8:[2001,2010],9:[2011,2018],10:[1931,1945],11:[1946,1960],12:[1961,1975],13:[1976,1990],\
                   14:[1991,2005],15:[2006,2018],16:[1914,1945],17:[1946,1975],18:[1976,2000],19:[2001,2018],20:[1914,2018]}

    a = DataFrameExtractor(pickle_obj)


   
#    for key, value in time_window.items():
#        print("--------------------------------------------------")
#        a = DataFrameExtractor(pickle_obj, value[0], value[1])
        

 
"""
Scope of the project - To identify the commonalities among famous or most connected actors across the 
timeline

Calculate the degree and degree centrality of each actor during the given time window

"""
#        valid_list = ['Lee Phelps','Frank Sinatra','John Wayne','Mike Starr','M.Emmet Walsh','Samuel L. Jackson','Matt Damon','Joe Chrest']    

"""        
        filtered_dataframe = DataFrameExtractor.data_frame[((DataFrameExtractor.data_frame["actor_1"] == 'Lee Phelps') | \
                                                            (DataFrameExtractor.data_frame["actor_1"] == 'Frank Sinatra') | \
                                                            (DataFrameExtractor.data_frame["actor_1"] == 'John Wayne') | \
                                                            (DataFrameExtractor.data_frame["actor_1"] == 'Mike Starr') | \
                                                            (DataFrameExtractor.data_frame["actor_1"] == 'M.Emmet Walsh') | \
                                                            (DataFrameExtractor.data_frame["actor_1"] == 'Samuel L. Jackson') | \
                                                            (DataFrameExtractor.data_frame["actor_1"] == 'Matt Damon') | \
                                                            (DataFrameExtractor.data_frame["actor_1"] == 'Joe Chrest') | \
                                                            (DataFrameExtractor.data_frame["actor_2"] == 'Lee Phelps') | \
                                                            (DataFrameExtractor.data_frame["actor_2"] == 'Frank Sinatra') | \
                                                            (DataFrameExtractor.data_frame["actor_2"] == 'John Wayne') | \
                                                            (DataFrameExtractor.data_frame["actor_2"] == 'Mike Starr') | \
                                                            (DataFrameExtractor.data_frame["actor_2"] == 'M.Emmet Walsh') | \
                                                            (DataFrameExtractor.data_frame["actor_2"] == 'Samuel L. Jackson') | \
                                                            (DataFrameExtractor.data_frame["actor_2"] == 'Matt Damon') | \
                                                            (DataFrameExtractor.data_frame["actor_2"] == 'Joe Chrest')) & \
                                                            (DataFrameExtractor.data_frame["weight"] != 1)]
        
        filtered_dataframe.to_csv('actor_graph_data_1914_2018.csv', index=False, encoding='utf-8', \
                                             header=['Source','Target','Movie_ids','weight'])
        print("------- NODES --------")
        for n, v in self.G.nodes(data=True):
            if ((n == 'Richard Bull') | (n == 'Walter Brooke')):
                print ('{} {}'.format(n,v))
        
        print("------- EDGE --------")
        
        for u,v,e in self.G.edges(data=True):
            if ((u == 'Richard Bull') & (v == 'Walter Brooke')):
                print ('{} {} {}'.format(u,v,e))

""" 