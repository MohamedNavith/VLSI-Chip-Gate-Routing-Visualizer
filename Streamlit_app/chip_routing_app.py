import streamlit as st
import networkx as nx
import plotly.graph_objects as go

edges = [
    ('A', 'B', 17), ('A', 'C', 18), ('A', 'D', 15),
    ('B', 'C', 18), ('B', 'E', 6), ('B', 'G', 28),
    ('C', 'E', 15), ('C', 'F', 4), ('C', 'D', 10),
    ('D', 'F', 14), ('D', 'I', 29),
    ('E', 'F', 12), ('E', 'G', 15),
    ('F', 'G', 17), ('F', 'H', 11), ('F', 'I', 13),
    ('G', 'J', 15), ('H', 'J', 11), ('H', 'I', 3), ('I', 'J', 13)
]
G = nx.Graph()
G.add_weighted_edges_from(edges)
nodes = list(G.nodes)

st.title("VLSI Chip Routing: Shortest Path (Dijkstra)")
src = st.selectbox("Select START gate", nodes, index=0)
dst = st.selectbox("Select END gate", nodes, index=1)

if src and dst and src != dst:
    try:
        path = nx.dijkstra_path(G, src, dst, weight='weight')
        cost = nx.dijkstra_path_length(G, src, dst, weight='weight')
        st.markdown(f"**Shortest path from {src} to {dst}:** {' → '.join(path)}")
        st.markdown(f"**Minimum wire length:** {cost}")
    except nx.NetworkXNoPath:
        st.markdown(":warning: **No path found!**")

    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1, color='#888'), hoverinfo='none')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=list(G.nodes()), textposition="bottom center", marker=dict(size=20, color='lightblue'))
    fig = go.Figure(data=[edge_trace, node_trace])
    if len(path) > 1:
        path_edges = list(zip(path[:-1], path[1:]))
        px = []
        py = []
        for u, v in path_edges:
            px += [pos[u], pos[v], None]
            py += [pos[u], pos[v], None]
        path_trace = go.Scatter(x=px, y=py, mode='lines', line=dict(width=5, color='red'), hoverinfo='none')
        fig.add_trace(path_trace)
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please pick two different gates.")
