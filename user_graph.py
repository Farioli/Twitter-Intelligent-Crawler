import networkx as nx

class UserGraph:
    
    graph = nx.DiGraph()

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_user(self, user) -> None:
        id = user.id
        self.graph.add_node(id, user=user)
        print(self.graph.nodes)


    def add_user_siblings(self, user, mentions) -> None:
        for sibling in mentions:
            self.graph.add_node(sibling.id, user=sibling)
            self.graph.add_edge(user.id, user=sibling.id)

    def get_user(self, user_id:int):
        return self.graph.nodes[user_id]['user']

    # Returns users that points the specified users
    def get_user_parents(self, user_id:int):
        try:
            parents_nodes = self.graph.predecessors(user_id)
            parents_users = []
            for node in parents_nodes:
                user = self.graph.nodes[user_id]['user']
                parents_users.append(user)
            return parents_users
        except:
            return []
    
    # Returns users that are pointed by the specified users
    def get_user_siblings(self, user_id:int):
        try:
            siblings_nodes = self.graph.successors(user_id)
            siblings_users = []
            for node in siblings_nodes:
                user = self.graph.nodes[user_id]['user']
                siblings_users.append(user)
            return siblings_users
        except:
            return []