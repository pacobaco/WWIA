import networkx as nx
import pandas as pd
from typing import Dict, Any

def matrix_to_signed_graph(M: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    for i in M.index:
        for j in M.columns:
            w = M.loc[i, j]
            if i != j and abs(w) > 1e-6:
                G.add_edge(i, j, weight=w, sign=1 if w > 0 else -1)
    return G

def multipolar_metrics(M: pd.DataFrame) -> Dict[str, Any]:
    G = matrix_to_signed_graph(M)
    conflict = []
    for i in M.index:
        for j in M.columns:
            if i < j:
                val = -min(M.loc[i, j], M.loc[j, i])
                if val > 0.15:
                    conflict.append({"pair": f"{i}-{j}", "conflict": round(val, 3)})
    return {
        "density": round(nx.density(G), 4),
        "reciprocity": round(nx.reciprocity(G), 4) if G.number_of_edges() else 0.0,
        "avg_outgoing": M.mean(axis=1).round(3).to_dict(),
        "avg_incoming": M.mean(axis=0).round(3).to_dict(),
        "top_conflict_pairs": sorted(conflict, key=lambda x: -x["conflict"])[:10],
    }
