import pandas as pd
from .patterndefinition.coalescing import (
    apply_coalescing_to_dataframe)
from .patterndefinition.communitydetection import (
    discover_communities_in_graph, 
    return_community_column)
from .patterndefinition.ranking import (
    rank_entities)
from .patterndefinition.stagecreation import (
    return_timewindows_column)
from .visualization.modeldiscovery import (
    discover_multi_dependency_graphs)
from .visualization.representativeexecutions import (
    get_most_common_activities_per_stage_column, 
    define_multiactivity_column, 
    create_column_withnames_for_hiddenactivities)
from ..utils.data_processing import (
    simplifyLog, 
    normalize_reltimes_log, 
    add_activity_position_percase, 
    map_values_to_col
)

#####################
### ORCHESTRATION: LOG ENHANCEMENT
#####################

def enhance_log_for_concise_model(
        df: pd.DataFrame,
        ACT_COL = "concept:name",
        CASE_COL = "case:concept:name",
        TIME_COL = "time:timestamp",
        RES_COL = "org:resource",
        RTIME_COL = "time:relative:seconds",
        NRTIMECASE_COL = "time:relative:normalized:case",
        NRTIMELOG_COL = "time:relative:normalized:log",
        STAGE_COL = "stage:number",
        COMM_COL = 'community:number',
        MULTI_ACT_COL = "concept:name:multiact",
        MULTI_COMM_COL = "concept:name:communities",
        num_stages = 2,
        dependency_threshold=0.5,
        num_comm_ranks=0,
        num_act_ranks=0,
        hide_common_activities=False
        ):
    '''
    Enhance log with attributes to be used for the concise model builder.

    Parameters
    ----------
    df : pd.DataFrame
        The event log dataframe.

    ACT_COL : str, default="concept:name"
        Column name representing the activity.

    CASE_COL : str, default="case:concept:name"
        Column name representing the case identifier.

    TIME_COL : str, default="time:timestamp"
        Column name for the event timestamp.

    RES_COL : str, default="org:resource"
        Column name for the resource performing the activity. (not used)

    RTIME_COL : str, default="time:relative:seconds"
        Column name for the event’s relative time in seconds.

    NRTIMECASE_COL : str, default="time:relative:normalized:case"
        Column describing normalized relative times per case.

    NRTIMELOG_COL : str, default="time:relative:normalized:log"
        Column describing normalized relative times across the entire log.

    STAGE_COL : str, default="stage:number"
        Column used to store assigned stage numbers.

    COMM_COL : str, default="community:number"
        Column used to store assigned community numbers.

    MULTI_ACT_COL : str, default="concept:name:multiact"
        Column containing lists of activities for multi-activity grouping.

    MULTI_COMM_COL : str, default="concept:name:communities"
        Column containing lists of communities (use the overall ranks).

    num_stages : int, default=2
        Number of stages to assign to the log.

    dependency_threshold : float, default=0.5
        Minimum dependency measure required to establish relations.

    num_comm_ranks : int, default=0
        Number of ranking attributes computed for communities. 
        (0 will keep all communities per stage. 
        1 will create 1 representative community and 
        store the others in a second one nodes, 
        2 will create 2 representative communities and
        store the other in a third one, etc.)

    num_act_ranks : int, default=0
        Number of ranking attributes computed for activities.
        (0 will keep all activities per community. 
        1 will keep exactly 1 representative activity, 
        2 keeps 2, etc.)

    hide_common_activities : bool, default=False
        If True, common/less-informative activities are hidden in the graphical model.
    '''
    # -------------------------------------------------------------
    # i. IMPORT LOG
    # -------------------------------------------------------------
    df_log = simplifyLog(df.copy())

    # -------------------------------------------------------------
    # ii. TEMPORAL SEQUENCE ALIGNMENT
    # -------------------------------------------------------------
    #Align sequences through normalized relative timestamps
    df_log = normalize_reltimes_log(df_log) # rel time
    df_log = add_activity_position_percase(df_log) # orderings

    # -------------------------------------------------------------
    # iii. COALESCING 
    # -------------------------------------------------------------
    # coalesce events
    df_log = apply_coalescing_to_dataframe(df_log)
    # filter out events
    if "events:ignore" in df_log.columns:
        indices_to_drop = df_log.loc[df_log["events:ignore"].isin([1])].index
        df_log = df_log.drop(indices_to_drop)

    # -------------------------------------------------------------
    # iv. STAGE DEFINITION 
    # -------------------------------------------------------------
    df_log[STAGE_COL] = return_timewindows_column(
        df_log, NRTIMECASE_COL=NRTIMECASE_COL, num_stages=num_stages)

    # -------------------------------------------------------------
    # v. COMMUNITY DETECTION 
    # -------------------------------------------------------------
    multipleDepG = discover_multi_dependency_graphs(df_log, dependency_threshold=dependency_threshold)
    community_list = discover_communities_in_graph(multipleDepG)
    df_log[COMM_COL] = return_community_column(df_log, community_list)

    # -------------------------------------------------------------
    # vi. RANKING 
    # -------------------------------------------------------------
    # Ranking communities - overall
    communities_ranks_ov = rank_entities(
        df_log,
        group_cols=[STAGE_COL, COMM_COL],
        value_col=NRTIMECASE_COL,
        agg_type="median",
        sort_cols=[STAGE_COL],
        rank_col_name="community_rank_overall"
    )
    df_log["community_rank_overall"] = map_values_to_col(
        df_log,
        communities_ranks_ov,
        key_cols=[STAGE_COL, COMM_COL],
        rank_col_name="community_rank_overall"
    )
    # Ranking communities - within
    communities_ranks_in = rank_entities(
    df_log,
        group_cols=[STAGE_COL, COMM_COL],
        value_col=NRTIMECASE_COL,
        agg_type="median",
        sort_cols=[STAGE_COL],
        rank_col_name="community_rank_within",
        rank_within_col = STAGE_COL
    )
    df_log["community_rank_within"] = map_values_to_col(
        df_log,
        communities_ranks_in,
        key_cols=[STAGE_COL, COMM_COL],
        rank_col_name="community_rank_within"
    )
    # Ranking activities in communities - overall
    activities_ranks_ov = rank_entities(
        df_log,
        group_cols=["community_rank_overall", ACT_COL],
        value_col=NRTIMECASE_COL,
        agg_type="median",
        sort_cols=["community_rank_overall"],
        rank_col_name="activity_rank_overall",
    )
    df_log["activity_rank_overall"] = map_values_to_col(
        df_log,
        activities_ranks_ov,
        key_cols=["community_rank_overall", ACT_COL],
        rank_col_name="activity_rank_overall"
    )
    # Ranking activities in communities - within
    activities_ranks_in = rank_entities(
        df_log,
        group_cols=["community_rank_overall", ACT_COL],
        value_col=NRTIMELOG_COL,
        agg_type="median",
        sort_cols=["community_rank_overall"],
        rank_col_name="activity_rank_within",
        rank_within_col = "community_rank_overall"
    )
    df_log["activity_rank_within"] = map_values_to_col(
        df_log,
        activities_ranks_in,
        key_cols=["community_rank_overall", ACT_COL],
        rank_col_name="activity_rank_within"
    )

    # -------------------------------------------------------------
    # vii. REPRESENTATIVE NODES AND LABELS 
    # -------------------------------------------------------------
    # get most common activites
    df_log["common_activities"] = get_most_common_activities_per_stage_column(df_log)
    # define representative activites
    REP_ACT_COL="concept:name:rep"
    df_log["concept:name:rep"] = define_multiactivity_column(
        df_log, 
        num_comm_ranks = num_comm_ranks,
        num_act_ranks = num_act_ranks, 
        hide_common_activities=hide_common_activities)
    # label activities in communities (only of hidden activites)
    df_log[MULTI_ACT_COL] = create_column_withnames_for_hiddenactivities(
        df_log, MULTIACT_COL=REP_ACT_COL, changing_type="stage+name")
    # label columns
    df_log[MULTI_COMM_COL] = create_column_withnames_for_hiddenactivities(
        df_log, MULTIACT_COL=REP_ACT_COL, changing_type="community_sum")

    # -------------------------------------------------------------
    # viii. RETURN ENHANCED LOG
    # -------------------------------------------------------------
    return df_log