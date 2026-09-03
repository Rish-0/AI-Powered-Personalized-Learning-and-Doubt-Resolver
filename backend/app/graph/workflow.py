from langgraph.graph import END
from langgraph.graph import StateGraph

from app.graph.state import GraphState

from app.graph.nodes import (
    router_node,
    pdf_node,
    web_node,
    chat_node
)

from app.graph.edges import route_edge


builder = StateGraph(GraphState)

builder.add_node(

    "router",

    router_node

)

builder.add_node(

    "pdf",

    pdf_node

)

builder.add_node(

    "web",

    web_node

)

builder.add_node(

    "chat",

    chat_node

)

builder.set_entry_point(

    "router"

)

builder.add_conditional_edges(

    "router",

    route_edge,

    {

        "PDF_RAG": "pdf",

        "WEB_SEARCH": "web",

        "GENERAL_CHAT": "chat"

    }

)

builder.add_edge(

    "pdf",

    END

)

builder.add_edge(

    "web",

    END

)

builder.add_edge(

    "chat",

    END

)

graph = builder.compile()
print(graph.get_graph().draw_mermaid())