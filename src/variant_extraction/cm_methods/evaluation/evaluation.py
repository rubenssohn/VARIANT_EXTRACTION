import networkx as nx
import numpy as np
import pandas as pd
from ...utils.data_helpers import (
    get_nunique_values_from_col,
    get_dataframe_len,
    get_num_nodes_in_graph,
    get_num_edges_in_graph,
    get_weighted_graph_from_dfg_dict,
    get_num_cycles_in_graph,
    get_total_weight_selfloops_in_graph,
    get_num_selfloops_in_graph
)

#####################
### ORCHESTRATION: EVALUATION
#####################

# Log statistics
def extract_event_log_statistics(
        df: pd.DataFrame, 
        ACT_COL="concept:name",
        CASE_COL="case:concept:name",
        STAGE_COL="stage:number",
        COMM_RANK_OVERALL_COL='community_rank_overall',
        MULTI_ACT_COL="concept:name:multiact",
        log_name="log_name"):
    num_events = get_dataframe_len(df)
    num_cases = get_nunique_values_from_col(df, CASE_COL)
    num_activities = get_nunique_values_from_col(df, ACT_COL)
    num_stages = np.nan
    if STAGE_COL in df.columns:
        num_stages = get_nunique_values_from_col(df, STAGE_COL)
    num_communities = np.nan
    if COMM_RANK_OVERALL_COL in df.columns:
        num_communities = get_nunique_values_from_col(df, COMM_RANK_OVERALL_COL)
    num_comtactivities = np.nan
    if MULTI_ACT_COL in df.columns:
        num_comtactivities = get_nunique_values_from_col(df, MULTI_ACT_COL)
    return pd.DataFrame(
        {"log_name": [log_name],
         "num_cases": [num_cases],
         "num_events": [num_events],
         "num_activities": [num_activities],
         "num_comtactivities": [num_comtactivities],
         "num_stages": [num_stages],
         "num_communities": [num_communities],
         }
    )

def extract_graph_statistics_from_dfg(
        dfg,
        log_name="log"):
    
    # Get graph
    G = get_weighted_graph_from_dfg_dict(dfg)

    # Get node statistics
    num_nodes = get_num_nodes_in_graph(G)

    # Get edge statistics
    num_edges = get_num_edges_in_graph(G)
    num_cycles = get_num_cycles_in_graph(G, length_bound=5, exclude_selfloops=False)
    num_selfloops = get_num_selfloops_in_graph(G)
    sum_selfloops_weight = get_total_weight_selfloops_in_graph(G, weight_attr="weight")
    num_cycles_noloops = num_cycles - num_selfloops
    return pd.DataFrame(
        {"log_name": [log_name],
         "num_nodes": [num_nodes],
         "num_edges": [num_edges],
         "num_cycles": [num_cycles],
         "num_selfloops": [num_selfloops],
         "sum_selfloops_weight": [sum_selfloops_weight],
         #"num_cycles_noloops": [num_cycles_noloops]
         }
    )

def generate_evaluation_statistics_df(
        df: pd.DataFrame, 
        dfg,
        ACT_COL = "concept:name",
        CASE_COL = "case:concept:name",
        STAGE_COL = "stage:number",
        COMM_RANK_OVERALL_COL='community_rank_overall',
        MULTI_ACT_COL = "concept:name:multiact",
        log_name = "log",
        log_name_col="log_name"):
    
    # generate log statistics
    log_statistics = extract_event_log_statistics(
        df, 
        ACT_COL=ACT_COL,
        CASE_COL=CASE_COL,
        STAGE_COL=STAGE_COL,
        COMM_RANK_OVERALL_COL=COMM_RANK_OVERALL_COL,
        MULTI_ACT_COL=MULTI_ACT_COL,
        log_name=log_name)
    
    # generate graph statistics
    graph_statistics = extract_graph_statistics_from_dfg(
        dfg, log_name=log_name)
    
    # combine statistics into on dataframe
    eva_statistics = log_statistics.merge(graph_statistics, on=log_name_col)
    return eva_statistics