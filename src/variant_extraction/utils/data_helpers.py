import pandas as pd
import networkx as nx

########
### Dataframe helpers
########
def get_nunique_values_from_col(
        df: pd.DataFrame, col_name: str):
    return df[col_name].nunique()

def get_dataframe_len(df):
    return len(df)

########
### Graph helpers
########
def get_num_nodes_in_graph(G):
    return len(G.nodes)

def get_num_edges_in_graph(G):
    return len(G.edges)

def get_weighted_graph_from_dfg_dict(dfg):
    G = nx.DiGraph()
    weighted_edges = [(src, tgt, weight) for (src, tgt), weight in dfg.items()]
    G.add_weighted_edges_from(weighted_edges)
    return G

def get_num_selfloops_in_graph(G):
    return nx.number_of_selfloops(G)

def get_num_cycles_in_graph(G, length_bound=None, exclude_selfloops=True):
    num_cycles = len(list(nx.simple_cycles(G, length_bound=length_bound)))
    if exclude_selfloops: 
        num_cycles = num_cycles - len(list(nx.simple_cycles(G, length_bound=1)))
    return num_cycles

def get_total_weight_selfloops_in_graph(G, weight_attr: str):
    sum_weight = 0
    for u, v in list(nx.selfloop_edges(G)):
        sum_weight += G[u][v][weight_attr]
    return sum_weight