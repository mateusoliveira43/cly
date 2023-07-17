from diagrams import Diagram, Edge, Cluster, Node
from diagrams.onprem.vcs import Git, Github
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.container import Docker
# diagrams.programming.language.Bash
from diagrams.programming.language import Python
from diagrams.programming.flowchart import Action
from diagrams.c4 import Person, Container

graph_attr = {
    "bgcolor": "transparent",
    "fontsize": "50",
}
node_attr = {
    "fontsize": "20",
}
edge_attr = {
    "fontsize": "50",
}

with Diagram("Contributing", show=False, graph_attr=graph_attr):
    # fork = Github("Create fork")

    # # with Cluster("Issue"):
    # Node("Search issue") - Node("Create new issue") >> fork

    # fork >> Git("Create branch") >> Edge(label="Development Cycle") >> Git("userdb")

    fork = Github("Create fork")

    issue = Container("Issue", description="Search or create new issue")
    issue >> Edge(style="dashed") >> fork

    main = fork >> Git("Create branch") >> Edge(label="Development Cycle") >> Github("Create PR")
    main >> GithubActions("CI Pipeline")
    main >> Github("Merge PR") >> GithubActions("CD Pipeline")

with Diagram("Development Cycle", show=False, graph_attr=graph_attr):
    with Cluster("Development environment"):
        dev_env = [
            Docker("Container image"),
            Python("Poetry"),
            Python("Pure Python"),
        ]

    commit = Git("Commit")
    push = Git("Push")
    coding = Container("Coding", description="Implement feature, fix bug, etc.")
    commit << Edge(style="dashed") << Container("pre-commit")
    dev_env >> coding >> Container("Quality check") >> Git("Add") >> commit >> push >> Edge(style="dashed") >> coding
