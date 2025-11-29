from cdlib import algorithms
from ..visualization.modeldiscovery import discover_dependency_graph
import networkx as nx
import pandas as pd

#####################
### COMMUNITY DETECTION
#####################

def discover_communities_in_graph(
        Graphs: list, type="leiden"):
    '''Discover communities in a list of NetworkX graphs.
    '''
    community_list = {}

    for G in Graphs:
        # Map string node labels to integers
        node_mapping = {name: i for i, name in enumerate(G.nodes())}
        G_int = nx.relabel_nodes(G, node_mapping)

        if type == "leiden":
            coms = algorithms.leiden(G_int)
            # Map back to original node labels
            reverse_mapping = {v: k for k, v in node_mapping.items()}
            communities_original = [
                [reverse_mapping[n] for n in com]
                for com in coms.communities
            ]
            community_list[getattr(G, "name", str(G))] = communities_original
        else:
            raise ValueError(f"Community detection type '{type}' not implemented.")

    return community_list

def create_map_from_community_dictionary(community_dict):
    '''
    Create a community map from (stage, activity) -> community_number
    based on a nested dictionary of communities.
    '''
    community_map = {}

    for stage, communities in community_dict.items():
        for community_number, community in enumerate(communities):
            for activity in community:
                community_map[(stage, activity)] = community_number

    return community_map

def return_community_column(
        df: pd.DataFrame, 
        community_dict, 
        ACT_COL="concept:name", 
        LEVEL_COL="stage:number"):
    '''Returns community column for a dataframe.
    '''
    community_map = create_map_from_community_dictionary(community_dict)
    return df.apply(
        lambda row: community_map.get(
            (row[LEVEL_COL], row[ACT_COL]), None), axis=1)