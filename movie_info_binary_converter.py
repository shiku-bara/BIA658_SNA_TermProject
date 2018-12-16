from collections import defaultdict, OrderedDict
from itertools import combinations
import pickle
import os



class MovieInfoExtractor:

    txt_file_path = None
    list_of_features_to_extract = None
    num_actors = None
    removal_set = []
    removal_set.append('jr')
    removal_set.append('jr.')
    removal_set.append('sr')
    removal_set.append('sr.')
    removal_set.append('Jr')
    removal_set.append('Jr.')
    removal_set.append('Sr')
    removal_set.append('Sr.')
    removal_set.append(' jr')
    removal_set.append(' jr.')
    removal_set.append(' sr')
    removal_set.append(' sr.')
    removal_set.append(' Jr')
    removal_set.append(' Jr.')
    removal_set.append(' Sr')
    removal_set.append(' Sr.')
    removal_set.append(' III')
    removal_set.append(' PhD')
    removal_set.append(' lll')
    removal_set.append(' ScD')
        
    def __init__(self, txt_file_path, list_of_features_to_extract=["movie_id"], num_actors=3):
        MovieInfoExtractor.txt_file_path = txt_file_path
        MovieInfoExtractor.list_of_features_to_extract = list_of_features_to_extract
        MovieInfoExtractor.num_actors = num_actors
        MovieInfoExtractor.__extract_movie_info()

    @staticmethod
    def __extract_movie_info():
        with open(MovieInfoExtractor.txt_file_path, 'r') as f:
            header = f.readline()
            header = header.strip().split('\t')
            column_name_idx_dict = {column_name: idx for idx, column_name in enumerate(header)}
            idx_to_column_name_dict = {idx: column_name for idx, column_name in enumerate(header)}
            
            indices_to_extract = []

            for feature in MovieInfoExtractor.list_of_features_to_extract:
                indices_to_extract.append(column_name_idx_dict[feature])

            year_to_movie_info_dict = defaultdict(dict)
            
            i=0
            year_list = []
            year_set = set()
            
            for line in f.readlines():
                i += 1
                line = line.strip().split('\t')
                date = line[6]
                if date == "NONE" or line[column_name_idx_dict["actor_names"]] == "NONE":
                    continue
                else:
                    year = int(date.split(' ')[2][0:4])
                    year_list.append(year)
                    year_set.add(year)
              
#            print(i)
#            print(len(year_list))
            

                actor_names_list = line[column_name_idx_dict["actor_names"]].strip().split(',')
                actor_names_updated_list = []
                for actor_name in actor_names_list:
#                    if actor_name not in MovieInfoExtractor.removal_set:
#                        if len(actor_name.strip()) == 3:
#                            print (actor_name)
#                           print(MovieInfoExtractor.removal_set)
                    if actor_name not in MovieInfoExtractor.removal_set:
                        actor_names_updated_list.append(actor_name)

                actor_names_pair_tuples_list = MovieInfoExtractor.__get_actor_names_pair_tuples_list(list(OrderedDict(zip(actor_names_updated_list, [None]*len(actor_names_updated_list))).keys()))
                #[:MovieInfoExtractor.num_actors]
                           
                
                for actor_names_pair_tuple in actor_names_pair_tuples_list:

                    if not actor_names_pair_tuple in year_to_movie_info_dict[year]:
                        year_to_movie_info_dict[year][actor_names_pair_tuple] = defaultdict(list)

                    for idx in indices_to_extract:
                        year_to_movie_info_dict[year][actor_names_pair_tuple][idx_to_column_name_dict[idx]].append(line[idx])

            MovieInfoExtractor.__write_movie_info_in_binary_file(year_to_movie_info_dict)
            print(sorted(year_set))

    @staticmethod
    def __write_movie_info_in_binary_file(movie_info):
        with open("movie_info.pkl", "wb") as f:
            pickle.dump(movie_info, f)

    @staticmethod
    def __get_actor_names_pair_tuples_list(actor_names_list):
        return [comb for comb in combinations(sorted(actor_names_list), 2)]


if __name__ == "__main__":
    raw_file_path = os.path.join(os.getcwd(), "rotten.txt")
    MovieInfoExtractor(raw_file_path)
 
 
