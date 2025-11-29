import graphviz

#####################
### VISUALIZATION (GRAPHVIZ)
#####################

def build_concise_dfg(
        dfg,
        start_activities,
        end_activities,
        community_dict,
        stage_dict, 
        hide_hidden_activities=True):
    '''
    Build a concise DFG of community nodes organized into vertical stages.

    Parameters
    ----------
    dfg : dict
        Directly follows graph in the form {(source, target): count}.
    start_activities : dict
        Keys = community ids, values = frequencies.
    end_activities : dict
        Keys = community ids, values = frequencies.
    community_dict : dict
        community_id -> list of activities in the community.
    stage_dict : dict
        stage_number -> list of community_ids belonging to that stage.
    hide_hidden_activities : boolean
        True if hidden activites should not be displayd in the graph.
    '''
    
    dot = graphviz.Digraph('G')
    dot.attr(rankdir='TB', compound='true')

    # -------------------------------------------------------------
    # 1. PREPARE STRUCTURES
    # -------------------------------------------------------------
    community_node_ids = {}   # map community_id -> dot node id
    stage_node_ids = []       # store stage label node ids (for timeline)

    # -------------------------------------------------------------
    # 2. ADD STAGES AND COMMUNITY NODES
    # -------------------------------------------------------------
    for stage_number, communities in stage_dict.items():

        # ---- Create stage nodes ----
        stage_label_id = f"stage_{stage_number}"
        stage_node_ids.append(stage_label_id)
        dot.node(stage_label_id, 
                 label=f"Stage {stage_number}",
                 shape="plaintext",
                 fontsize="14")

        # ---- Create all community nodes in this stage ----
        community_ids_in_stage = []

        for comm in communities:
            comm_id = f"comm_{comm}"

            # Filter hidden activities (those starting with "_")
            activities = community_dict.get(comm, [])
            if hide_hidden_activities:
                activities = [a for a in activities if not a.startswith("_")]

            # List and depict activities in community node
            # (OLD PART)
            #rows = "".join(f"<TR><TD>{act}</TD></TR>" 
            #               for act in community_dict.get(comm, []))
            # Build HTML table rows
            rows = "".join(f"<TR><TD>{act}</TD></TR>" for act in activities)
            
            label = f"""<
                <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" STYLE="ROUNDED" BGCOLOR="white">
                    <TR><TD><B>{comm}</B></TD></TR>
                    {rows}
                </TABLE>>"""

            dot.node(comm_id, label=label, shape="none")
            community_node_ids[comm] = comm_id
            community_ids_in_stage.append(comm_id)

        # ---- Align all community nodes horizontally in this stage ----
        with dot.subgraph() as rank:
            rank.attr(rank="same")
            rank.node(stage_label_id)
            for comm_node in community_ids_in_stage:
                rank.node(comm_node)

    # -------------------------------------------------------------
    # 3. DRAW TIMELINE (VERTICAL CONNECTION OF STAGES)
    # -------------------------------------------------------------
    for s1, s2 in zip(stage_node_ids, stage_node_ids[1:]):
        dot.edge(s1, s2, style="bold", arrowhead="none")

    # -------------------------------------------------------------
    # 4. DRAW COMMUNITY EDGES
    # -------------------------------------------------------------
    for (source, target), freq in dfg.items():

        if source not in community_node_ids or target not in community_node_ids:
            continue

        dot.edge(
            community_node_ids[source],
            community_node_ids[target],
            label=str(freq)
        )

    # -------------------------------------------------------------
    # 5. DRAW START / END EDGES
    # -------------------------------------------------------------
    # Add start and end symbols
    dot.node("start", shape="circle", label="Start", style="filled", fillcolor="lightgray")
    dot.node("end", shape="circle", label="End", style="filled", fillcolor="lightgray")

    # Start edges
    for comm in start_activities:
        if comm in community_node_ids:
            frequency = str(start_activities.get(comm))
            dot.edge("start", community_node_ids[comm], style="dashed", arrowhead="none", label=frequency)

    # End edges
    for comm in end_activities:
        if comm in community_node_ids:
            frequency = str(end_activities.get(comm))
            dot.edge(community_node_ids[comm], "end", style="dashed", arrowhead="none", label=frequency)

    # -------------------------------------------------------------
    # 6. RETURN RESULT
    # -------------------------------------------------------------
    return dot