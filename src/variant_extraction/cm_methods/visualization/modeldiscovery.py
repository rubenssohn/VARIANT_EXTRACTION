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