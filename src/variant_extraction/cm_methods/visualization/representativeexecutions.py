import pandas as pd
import numpy as np

#####################
### REPRESENTATIVE PROCESS EXECUTIONS
#####################

#### REPRESENTATIONS
def create_caseoccurency_matrix_pergroup(
        df: pd.DataFrame, 
        ACT_COL="concept:name", 
        CASE_COL="case:concept:name", 
        STAGE_COL="stage:number"):
    ''' Creates a matrix with case occurencies for a group.
    '''
    stage_activity_matrix = (
        df.groupby([STAGE_COL, ACT_COL])[CASE_COL]
        .nunique()              # Count cases
        .unstack(fill_value=0)  # Convert activities to columns
        )
    return stage_activity_matrix

def get_most_common_activities_per_stage_column(
        df: pd.DataFrame, 
        ACT_COL="concept:name", 
        CASE_COL="case:concept:name", 
        STAGE_COL="stage:number"):
    '''Define most common activitites per group (stage).
    '''
    stage_activity_matrix = create_caseoccurency_matrix_pergroup(df, ACT_COL=ACT_COL, CASE_COL=CASE_COL, STAGE_COL=STAGE_COL)
    common_stages = stage_activity_matrix.idxmax().to_dict()
    #print(common_stages.items())
    #common_stages_tuples = {(k, i): 1 for k, values in common_stages.items() for i in values}
    common_stages_tuples = {
        (act, stage): 1
        for act, stage in common_stages.items()
    }
    return df.apply(
        lambda row: common_stages_tuples.get((row[ACT_COL], row[STAGE_COL]), 0), axis=1)

def define_multiactivity_column(
        df:pd.DataFrame, 
        ACT_COL = "concept:name",
        COMMON_ACT_COL = "common_activities",
        COMM_RANK_COL = "community_rank_within",
        ACT_RANK_COL = "activity_rank_within",
        num_comm_ranks = 3, # 0 for all
        num_act_ranks = 1, # 0 for all
        hide_activities_value="hidden",
        hide_common_activities=True):
    '''Create a new column with representative activities 
    based on number of nodes.
    '''
    
    conditions = []
    # cond1: check if common activities should be hidden or not
    if hide_common_activities:
        common_acts = [1]
    else:
        common_acts = [0, 1]
    conditions.append((COMMON_ACT_COL, common_acts))
    
    # cond2: get the number of communities
    if num_comm_ranks >= 1:
        comm_ranks = list(range(0, num_comm_ranks))
        #print(comm_ranks)
        conditions.append((COMM_RANK_COL,comm_ranks))
    
    # cond3: get the number of activities
    if num_act_ranks >= 1:
        act_ranks = list(range(0, num_act_ranks))
        conditions.append((ACT_RANK_COL,act_ranks))

    # create a mask
    mask = pd.Series(True, index=df.index)
    for col, values in conditions:
        mask &= df[col].isin(values)
    
    return df[ACT_COL].where(mask, hide_activities_value)

def shorten_list_int_values(values: list[int]) -> str:
    if not values:
        return ""
    values = sorted(values)

    ranges = []
    start = prev = values[0]

    for v in values[1:]:
        if v == prev + 1:
            # still in a consecutive run
            prev = v
        else:
            # end of a run
            if start == prev:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{prev}")
            start = prev = v

    # finalize last run
    if start == prev:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{prev}")

    return ",".join(ranges)

def shorten_list_int_values_in_dict(merge_dict: dict):
    merge_dict_sum = {}

    for stage, items in merge_dict.items():
        # Only compute the shortened string once per stage
        #print(items)
        shortened_comm_num = shorten_list_int_values(items)

        # Assign to each item in this stage
        for item in items:
            merge_dict_sum[item] = shortened_comm_num
    return merge_dict_sum

# TODO: better to create a column with 0 and 1 (need to change the following functions as well)
def create_hiddencommunities_perstage_dict(
        df: pd.DataFrame,
        STAGE_COL = "stage:number",
        COMM_RANK_COL = "community_rank_overall",
        HACT_COL = "concept:name:rep",
        hide_activities_value="hidden"
        ):
    # Group and extract unique activities for each stage and community
    group = df.groupby([STAGE_COL, COMM_RANK_COL])[HACT_COL].unique()
    empty_comms = group.index[group.isin([[hide_activities_value]])].to_list()

    merge_dict = {}
    for comm in empty_comms:
        stage_num = comm[0]
        comm_num = comm[1]
        try:
            merge_dict[stage_num].append(comm_num)
        except:
            merge_dict[stage_num] = [comm_num]
    #print(merge_dict)
    merge_dict_summarized = shorten_list_int_values_in_dict(merge_dict)
    
    return merge_dict_summarized

def create_column_withnames_for_hiddenactivities(
        df: pd.DataFrame, 
        MULTIACT_COL = "concept:name:multiact",
        ACT_COL = "concept:name",
        STAGE_COL = "stage:number",
        COMM_RANK_COL="community_rank_overall",
        changing_type="stage+name"):
    if changing_type == "stage":
        return df[STAGE_COL].where(df[MULTIACT_COL] == "hidden", df[MULTIACT_COL]).astype(str)
    elif changing_type == "stage+name":
        return np.where(
            df[MULTIACT_COL] == "hidden",
            "_" + df[STAGE_COL].astype(str) + "_" + df[ACT_COL].astype(str),
            df[MULTIACT_COL].astype(str)
        )
    elif changing_type == "community_sum":
        merge_dict = create_hiddencommunities_perstage_dict(df)
        return df[COMM_RANK_COL].map(lambda v: merge_dict.get(v, v)).astype(str)
    else:
        raise ValueError(f"changing_type must be: 'stage', 'stage+name', or 'community_sum'")