"""Works class and associated functions used to build the citationsnetwork."""
import requests
import time
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class Works:
    """Works class that helps in obtaining the details of scholarly articles."""

    def __init__(self, oaid):
        self.oaid = oaid
        self.data = None  # Initialize data attribute
        try:
            self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
            self.data = self.req.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for OAID {oaid}: {e}")
        except ValueError as e:
            print(f"Error decoding JSON response for OAID {oaid}: {e}")

    def get_cited_by_works(self):
        """Retrieve information about works that cite this work."""
        cited_by_doi = []
        cited_by_title = []
        cited_by_oaid = []
        cited_by_journal = []
        
        if self.data and 'cited_by_api_url' in self.data:
            try:
                req_cited_by = requests.get(self.data['cited_by_api_url'])
                if req_cited_by.status_code == 200:
                    results = req_cited_by.json().get('results', [])
                    for result in results[:20]:
                        if result.get('primary_location') and result.get('doi') and result.get('title') and result.get('id') and result['primary_location'].get('source'):
                            cited_by_doi.append(result['doi'])
                            cited_by_title.append(result['title'])
                            cited_by_oaid.append(result['id'])
                            cited_by_journal.append(result['primary_location']['source']['display_name'])
                        time.sleep(0.5)  # Sleep for rate limiting
                else:
                    print(f"Failed to fetch cited_by data for OAID {self.oaid}. Status code: {req_cited_by.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching cited_by data for OAID {self.oaid}: {e}")
        else:
            print(f"cited_by_api_url not found in data for OAID {self.oaid}")
        
        return cited_by_doi, cited_by_title, cited_by_oaid, cited_by_journal

    def get_referenced_works(self):
        doireferenced = []
        titlereferenced = []
        oaidreferenced = []
        journalreferenced = []

        if self.data and 'referenced_works' in self.data:
            for j in self.data['referenced_works']:
                try:
                    req_referenced = requests.get(f"https://api.openalex.org/works/{j}")
                    time.sleep(0.5)  # Sleep for rate limiting
                    if req_referenced.status_code == 200:
                        referenced_data = req_referenced.json()
                        if referenced_data['primary_location'] and referenced_data['doi'] and referenced_data['title'] and referenced_data['id'] and referenced_data['primary_location']['source']:
                            doireferenced.append(referenced_data['doi'])
                            titlereferenced.append(referenced_data['title'])
                            oaidreferenced.append(referenced_data['id'])
                            journalreferenced.append(referenced_data['primary_location']['source']['display_name'])
                                                    
                        print(f"Failed to fetch referenced work data for OAID {j}. Status code: {req_referenced.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching referenced work data for OAID {j}: {e}")
        else:
            print("No referenced works found in data.")

        return doireferenced, titlereferenced, oaidreferenced, journalreferenced


    def build_cite_network(self, G, depth):
        """Build the citations network by recursively calling the previous two functions."""
        if depth > 0:
            cited_by_doi, cited_by_title, cited_by_oaid, cited_by_journal = self.get_cited_by_works()
            doireferenced, titlereferenced, oaidreferenced, journalreferenced = self.get_referenced_works()
            
            for doi, title, journal in zip(doireferenced, titlereferenced, journalreferenced):
                G.add_node(title, journal=journal, doi=doi)
            for doi, title, journal in zip(cited_by_doi, cited_by_title, cited_by_journal):
                G.add_node(title, journal=journal, doi=doi)
            
            edgelist = [(title_cited_by, self.data['title']) for title_cited_by in cited_by_title]
            edgelist += [(self.data['title'], ref_title) for ref_title in titlereferenced]
            G.add_edges_from(edgelist)
            
            for ref in oaidreferenced:
                G = Works(ref).build_cite_network(G, depth - 1)
            for cb in cited_by_oaid:
                G = Works(cb).build_cite_network(G, depth - 1)
        
        return G
    
    def plot_cite_network(self, max_depth):
        """Plot the citations network based on the built citations network."""
        G = nx.DiGraph()
        G.add_node(self.data['title'], journal=self.data['primary_location']['source']['display_name'], doi=self.data['doi'])
        G = self.build_cite_network(G, max_depth)
        
        journalnames = nx.get_node_attributes(G, "journal")
        doivals = nx.get_node_attributes(G, "doi")
        unique_journals = list(set(journalnames.values()))
        color_map = {journal: plt.cm.tab20(i) for i, journal in enumerate(unique_journals)}
        
        pos = nx.spring_layout(G)
        
        node_x = []
        node_y = []
        node_colors = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            journal = journalnames[node]
            color = color_map[journal]
            node_colors.append(f'rgb({int(color[0]*255)},{int(color[1]*255)},{int(color[2]*255)})')
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            marker=dict(size=10, color=node_colors),
            hoverinfo='text',
            text=[f"<br> <a href='{doivals[node]}' target='_blank'> Node: '{node}' Journal: '{journalnames[node]}'</a>" for node in G.nodes()]
        )
        
        edge_traces = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            edge_trace = go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode='lines',
                line=dict(width=1),
                marker=dict(symbol='arrow-up', color='black'),
                hoverinfo='none'
            )
            edge_traces.append(edge_trace)
        
        layout = go.Layout(
            title='Interactive NetworkX Graph with Hover Text and Annotations',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            annotations=[
                dict(
                    x=x1, y=y1,
                    xref='x', yref='y',
                    text='',
                    showarrow=True,
                    arrowhead=1,
                    ax=x0, ay=y0,
                    axref='x', ayref='y',
                    arrowwidth=1,
                    arrowcolor='gray',
                    arrowsize=1
                )
                for (x0, y0), (x1, y1) in [(pos[edge[0]], pos[edge[1]]) for edge in G.edges()]
            ]
        )
        
        fig = go.Figure(data=edge_traces + [node_trace], layout=layout)
        fig.show()
