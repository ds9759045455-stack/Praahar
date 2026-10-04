from typing import List, Dict, Any, Tuple
from app.models.schemas import MuleAccountNode, TransactionEdge

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

class MuleGraphEngine:
    def __init__(self):
        pass

    def analyze_mule_network(
        self, 
        nodes: List[MuleAccountNode], 
        edges: List[TransactionEdge]
    ) -> Dict[str, Any]:
        """
        Builds directed transaction graph, computes centrality metrics,
        detects multi-tier aggregation hubs and circular laundering cycles.
        """
        if HAS_NETWORKX:
            return self._analyze_with_networkx(nodes, edges)
        else:
            return self._analyze_pure_python(nodes, edges)

    def _analyze_with_networkx(self, nodes: List[MuleAccountNode], edges: List[TransactionEdge]) -> Dict[str, Any]:
        G = nx.DiGraph()

        for n in nodes:
            G.add_node(
                n.account_number,
                holder_name=n.holder_name,
                bank_name=n.bank_name,
                ifsc_code=n.ifsc_code,
                layer=n.layer_level,
                balance=n.current_balance,
                base_risk=n.risk_score
            )

        for e in edges:
            G.add_edge(
                e.from_account,
                e.to_account,
                tx_id=e.tx_id,
                amount=e.amount,
                timestamp=e.timestamp,
                channel=e.channel,
                layer=e.layer
            )

        try:
            pagerank = nx.pagerank(G, alpha=0.85) if len(G) > 1 else {n.account_number: 1.0 for n in nodes}
        except Exception:
            pagerank = {n.account_number: 0.5 for n in nodes}

        in_degrees = dict(G.in_degree())
        out_degrees = dict(G.out_degree())

        cycles = []
        try:
            simple_cycles = list(nx.simple_cycles(G))
            for c in simple_cycles:
                if len(c) > 1:
                    cycles.append(c)
        except Exception:
            cycles = []

        enriched_nodes = []
        high_risk_cashout_accounts = []

        for n in nodes:
            acc = n.account_number
            pr = pagerank.get(acc, 0.0)
            in_deg = in_degrees.get(acc, 0)
            out_deg = out_degrees.get(acc, 0)

            dynamic_risk = n.risk_score * 0.4 + min(pr * 3.0, 0.3) + (0.3 if n.layer_level == 3 else 0.15)
            dynamic_risk = min(max(dynamic_risk, 0.1), 0.99)

            is_cashout_mule = (n.layer_level == 3) or (out_deg == 0 and in_deg >= 1 and n.current_balance > 0)
            if is_cashout_mule:
                high_risk_cashout_accounts.append(acc)

            node_data = n.model_dump()
            node_data["dynamic_risk"] = round(dynamic_risk, 3)
            node_data["in_degree"] = in_deg
            node_data["out_degree"] = out_deg
            node_data["pagerank"] = round(pr, 4)
            node_data["is_cashout_mule"] = is_cashout_mule
            enriched_nodes.append(node_data)

        return {
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges(),
            "detected_rings": len(cycles),
            "cycles": cycles,
            "cashout_accounts": high_risk_cashout_accounts,
            "enriched_nodes": enriched_nodes,
            "vis_graph": self._format_vis_js(enriched_nodes, edges)
        }

    def _analyze_pure_python(self, nodes: List[MuleAccountNode], edges: List[TransactionEdge]) -> Dict[str, Any]:
        """Pure python fallback when networkx is compiling"""
        in_degrees = {n.account_number: 0 for n in nodes}
        out_degrees = {n.account_number: 0 for n in nodes}

        for e in edges:
            if e.from_account in out_degrees:
                out_degrees[e.from_account] += 1
            if e.to_account in in_degrees:
                in_degrees[e.to_account] += 1

        enriched_nodes = []
        high_risk_cashout_accounts = []

        for n in nodes:
            acc = n.account_number
            in_deg = in_degrees.get(acc, 0)
            out_deg = out_degrees.get(acc, 0)

            dynamic_risk = n.risk_score * 0.5 + (0.35 if n.layer_level == 3 else 0.15)
            dynamic_risk = min(max(dynamic_risk, 0.1), 0.99)

            is_cashout_mule = (n.layer_level == 3) or (out_deg == 0 and in_deg >= 1 and n.current_balance > 0)
            if is_cashout_mule:
                high_risk_cashout_accounts.append(acc)

            node_data = n.model_dump()
            node_data["dynamic_risk"] = round(dynamic_risk, 3)
            node_data["in_degree"] = in_deg
            node_data["out_degree"] = out_deg
            node_data["pagerank"] = 0.5
            node_data["is_cashout_mule"] = is_cashout_mule
            enriched_nodes.append(node_data)

        return {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "detected_rings": 0,
            "cycles": [],
            "cashout_accounts": high_risk_cashout_accounts,
            "enriched_nodes": enriched_nodes,
            "vis_graph": self._format_vis_js(enriched_nodes, edges)
        }

    def _format_vis_js(self, nodes: List[Dict], edges: List[TransactionEdge]) -> Dict[str, Any]:
        """Formats graph structure for interactive Vis.js visualization"""
        vis_nodes = []
        for n in nodes:
            color = "#ef4444" if n["layer_level"] == 3 else ("#f59e0b" if n["layer_level"] == 2 else "#3b82f6")
            if n.get("is_cashout_mule"):
                color = "#dc2626"

            vis_nodes.append({
                "id": n["account_number"],
                "label": f"{n['holder_name']}\n(L{n['layer_level']})",
                "title": f"Acc: {n['account_number']}<br>Bank: {n['bank_name']}<br>Balance: ₹{n['current_balance']:,.2f}<br>Risk: {int(n['dynamic_risk']*100)}%",
                "color": color,
                "shape": "dot",
                "size": 18 + int(n["dynamic_risk"] * 15),
                "layer": n["layer_level"],
                "balance": n["current_balance"],
                "bank": n["bank_name"],
                "risk": n["dynamic_risk"]
            })

        vis_edges = []
        for e in edges:
            vis_edges.append({
                "from": e.from_account,
                "to": e.to_account,
                "label": f"₹{e.amount:,.0f} ({e.channel})",
                "arrows": "to",
                "color": {"color": "#64748b", "highlight": "#38bdf8"},
                "font": {"color": "#94a3b8", "size": 10, "align": "top"}
            })

        return {"nodes": vis_nodes, "edges": vis_edges}

mule_graph_engine = MuleGraphEngine()
