import pytest
from citeNet.works import Works
import requests
import networkx as nx

# Mock response data for successful API requests
MOCK_DATA = {
    "title": "Secure Data Sharing over Vehicular Networks Based on Multi-sharding Blockchain",
    "primary_location": {
        "source": {
            "display_name": "Secure Data Sharing over Vehicular Networks Based on Multi-sharding Blockchain"
        }
    },
    "doi": "https://doi.org/10.1145/3579035"
}

@pytest.fixture()
def test_works_init():
    # Test __init__ method of Works class
    oaid="W4313590322"
    works = Works(oaid)
    assert works.data['oaid'] == oaid
    assert works.data['title'] == MOCK_DATA['title']  # Make sure data attribute is populated correctly
    assert works.data['doi'] == MOCK_DATA['title']
    assert works.data['primary_location']['source']['display_name'] == MOCK_DATA['primary_location']['source']['display_name']  # Make sure data attribute is populated correctly

def test_get_cited_by_works():
    # Test get_cited_by_works method of Works class
    oaid = "W4313590322"
    works = Works(oaid)
    cited_by_doi, cited_by_title, cited_by_oaid, cited_by_journal = works.get_cited_by_works()
    assert cited_by_doi == ['https://doi.org/10.1016/j.vehcom.2023.100614', 'https://doi.org/10.21203/rs.3.rs-3029457/v1']  # Replace with expected values based on MOCK_DATA
    assert cited_by_title == ['VERCO: A privacy and data-centric architecture for verifiable cooperative maneuvers', 'EGQCY: A Smart Contract-Based Scientific Big Data System Approach for Incentive Sharing and Transaction on the Cost of Data Quality']
    assert cited_by_oaid == ['https://openalex.org/W4376891898', 'https://openalex.org/W4380610142']  # Replace with expected values based on MOCK_DATA
    assert cited_by_journal == ['Vehicular communications', 'Research Square (Research Square)']  # Replace with expected values based on MOCK_DATA

def test_get_referenced_works():
    # Test get_referenced_works method of Works class
    oaid = "W4313590322"
    works = Works(oaid)
    doireferenced, titlereferenced, oaidreferenced, journalreferenced = works.get_referenced_works()
    assert doireferenced == ['https://doi.org/10.1007/978-3-540-27800-9_28', 'https://doi.org/10.1109/tvt.2007.907273', 'https://doi.org/10.1007/978-3-540-28628-8_3', 'https://doi.org/10.1007/978-3-662-49896-5_11', 'https://doi.org/10.1109/jas.2017.7510736', 'https://doi.org/10.1109/tits.2018.2818888', 'https://doi.org/10.14778/3229863.3236266', 'https://doi.org/10.1109/jiot.2018.2874398', 'https://doi.org/10.1109/mnet.001.1800290', 'https://doi.org/10.1109/jiot.2019.2946611', 'https://doi.org/10.1016/j.jnca.2019.102471', 'https://doi.org/10.1109/tdsc.2020.2980255', 'https://doi.org/10.48550/arxiv.2007.03520', 'https://doi.org/10.1109/tvt.2020.3037804', 'https://doi.org/10.1109/tits.2021.3074974']
    assert titlereferenced == ['Linkable Spontaneous Anonymous Group Signature for Ad Hoc Groups', 'Performance Evaluation of SUVnet With Real-Time Traffic Data', 'Short Group Signatures', 'On the Size of Pairing-Based Non-interactive Arguments', 'Internet of vehicles in big data era', 'A Survey on Recent Advances in Vehicular Network Security, Trust, and Privacy', 'A demonstration of sterling', 'Blockchain-Based Internet of Vehicles: Distributed Network Architecture and Performance Analysis', 'A Survey on the Scalability of Blockchain Systems', 'Toward Secure Data Sharing for the IoV: A Quality-Driven Incentive Mechanism With On-Chain and Off-Chain Guarantees', 'Sidechain technologies in blockchain networks: An examination and state-of-the-art review', 'LVBS: Lightweight Vehicular Blockchain for Secure Data Sharing in Disaster Rescue', 'A Survey of State-of-the-Art on Blockchains: Theories, Modelings, and Tools', 'An Identity-Based and Revocable Data-Sharing Scheme in VANETs', 'Linkable Privacy-Preserving Scheme for Location-Based Services']
    assert oaidreferenced ==  ['https://openalex.org/W1533905858', 'https://openalex.org/W2154089474', 'https://openalex.org/W2172174332', 'https://openalex.org/W2496543269', 'https://openalex.org/W2778363563', 'https://openalex.org/W2799867512', 'https://openalex.org/W2889110589', 'https://openalex.org/W2894786170', 'https://openalex.org/W2971569867', 'https://openalex.org/W2980046995', 'https://openalex.org/W2981399413', 'https://openalex.org/W3011995057', 'https://openalex.org/W3038382510', 'https://openalex.org/W3098526301', 'https://openalex.org/W3159189932']
    assert journalreferenced == ['Lecture notes in computer science', 'IEEE transactions on vehicular technology', 'Lecture notes in computer science', 'Lecture notes in computer science', 'IEEE/CAA journal of automatica sinica', 'IEEE transactions on intelligent transportation systems', 'Proceedings of the VLDB Endowment', 'IEEE internet of things journal', 'IEEE network', 'IEEE internet of things journal', 'Journal of network and computer applications', 'IEEE Transactions on Dependable and Secure Computing/IEEE transactions on dependable and secure computing', 'arXiv (Cornell University)', 'IEEE transactions on vehicular technology', 'IEEE transactions on intelligent transportation systems']

def test_build_cite_network():
    # Test build_cite_network method of Works class
    oaid = "W4313590322"
    works = Works(oaid)
    G = works.build_cite_network(nx.DiGraph(), depth=1)
    assert isinstance(G, nx.DiGraph)  # Make sure G is a NetworkX DiGraph object
    assert len(G.nodes()) == 18
    assert len(G.edges()) == 17
    
