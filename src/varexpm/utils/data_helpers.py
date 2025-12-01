'''
VARIANT_EXTRACTION — A Python package and CLI tool to extract and visualize process behaviors from complex event data.
Copyright (C) 2023  Christoffer Rubensson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Website: https://hu-berlin.de/rubensson
E-Mail: {firstname.lastname}@hu-berlin.de
'''

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