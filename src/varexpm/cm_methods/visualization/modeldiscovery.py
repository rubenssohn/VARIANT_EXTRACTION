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

import networkx as nx
import pandas as pd
import pm4py

#####################
### DISCOVERY
#####################

def discover_dependency_graph(
        df: pd.DataFrame, 
        dependency_threshold=0.5, 
        ACT_COL="concept:name"):
    """Discover a dependency graph from an event log.
    """
    # Create a directed graph
    DepG = nx.DiGraph()

    # create dependencies matrix
    heunet = pm4py.discover_heuristics_net(
        df, dependency_threshold=dependency_threshold, activity_key=ACT_COL)
    dependency_matrix = heunet.dependency_matrix.items()
    act_list = heunet.activities
    #print(dependency_matrix)

    # Add nodes and edges from the nested dependency dictionary
    for source, targets in dependency_matrix:
        DepG.add_node(source)  # Add source node
        if source in act_list:
            act_list.remove(source)
        for target, dependency_value in targets.items():
            DepG.add_node(target)  # Ensure target node exists
            if target in act_list:
                act_list.remove(target)
            # Only add edges with positive dependency
            if dependency_value > dependency_threshold:
                DepG.add_edge(source, target, weight=dependency_value)

    # Add remaining nodes not in dependency matrix
    for act in act_list:
        DepG.add_edge(act, act, weight=0)
    
    return DepG

def discover_multi_dependency_graphs(
        df, 
        dependency_threshold=0.5, 
        ACT_COL="concept:name", 
        LEVEL_COL="stage:number"):
    """Discover multiple dependency graphs, one for each stage.
    """
    multipleDepG = []
    levels = df[LEVEL_COL].unique()
    for level in levels:
        depG = discover_dependency_graph(
            df=df.loc[df[LEVEL_COL].isin([level])], 
            dependency_threshold=dependency_threshold, ACT_COL=ACT_COL)
        depG.graph["name"] = level
        multipleDepG.append(depG)
    return multipleDepG