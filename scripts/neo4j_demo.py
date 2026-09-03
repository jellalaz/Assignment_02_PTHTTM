import os
import pandas as pd
from neo4j import GraphDatabase

# Configure Neo4j connection
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "ecommerce", "ecommerce_cleaned.csv")
CYPHER_SCRIPT = os.path.join(BASE_DIR, "scripts", "import_graph.cypher")

class EcommerceGraphRAG:
    def __init__(self, uri, auth):
        print(f"[*] Connecting to Neo4j at {uri}...")
        self.driver = GraphDatabase.driver(uri, auth=auth)
        self.driver.verify_connectivity()
        print("[+] Connected successfully.")

    def close(self):
        self.driver.close()

    def wipe_database(self):
        print("[*] Wiping existing database...")
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("[+] Database wiped.")

    def setup_constraints(self):
        print("[*] Setting up constraints...")
        with open(CYPHER_SCRIPT, "r", encoding="utf-8") as f:
            queries = f.read().split(";")
        
        with self.driver.session() as session:
            for query in queries:
                if query.strip() and not query.strip().startswith("//"):
                    session.run(query.strip())
        print("[+] Constraints configured.")

    def import_data(self, csv_path, sample_size=1000):
        print(f"[*] Loading dataset from {csv_path} (Sample: {sample_size} rows)...")
        df = pd.read_csv(csv_path)
        # Drop rows with missing crucial graph elements
        df = df.dropna(subset=['Age', 'Class Name', 'Department Name', 'Review Text', 'Rating'])
        df = df.head(sample_size)
        
        records = df.to_dict(orient="records")
        
        # Cypher query to merge nodes and relationships
        import_query = """
        UNWIND $batch AS row
        
        // 1. Create/Merge Department
        MERGE (d:Department {name: row.`Department Name`})
        ON CREATE SET d.division = row.`Division Name`
        
        // 2. Create/Merge Product Class
        MERGE (p:Product {class_name: row.`Class Name`})
        MERGE (p)-[:BELONGS_TO]->(d)
        
        // 3. Create/Merge Customer (using Age as a proxy for customer demographic node)
        MERGE (c:Customer {id: row.Clothing_ID + '_' + row.Age, age: toInteger(row.Age)})
        
        // 4. Create Review
        CREATE (r:Review {
            text: row.`Review Text`, 
            rating: toInteger(row.Rating), 
            recommended: toBoolean(row.`Recommended IND`)
        })
        
        // 5. Link Customer -> Review -> Product
        CREATE (c)-[:WROTE]->(r)
        CREATE (r)-[:ABOUT]->(p)
        """
        
        print("[*] Pushing data to Neo4j. This may take a moment...")
        with self.driver.session() as session:
            session.run(import_query, batch=records)
            
        print(f"[+] Successfully imported {len(records)} records into the Knowledge Graph.")

    def run_graph_rag_query(self, product_class="Dresses", max_age=30):
        print(f"\n[*] --- GRAPH RAG SIMULATION ---")
        print(f"Question: 'What are some positive reviews about {product_class} from customers under {max_age}?'\n")
        
        query = """
        MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(p:Product {class_name: $product_class})
        WHERE c.age <= $max_age AND r.recommended = true
        RETURN c.age AS Age, r.rating AS Rating, r.text AS ReviewText
        LIMIT 3
        """
        
        with self.driver.session() as session:
            result = session.run(query, product_class=product_class, max_age=max_age)
            records = list(result)
            
            if not records:
                print("[-] No reviews found matching the criteria.")
                return
                
            print(f"[+] Retrieved Context from Graph:")
            for i, record in enumerate(records, 1):
                print(f"  {i}. [Customer Age: {record['Age']}, Rating: {record['Rating']}/5]")
                print(f"     \"{record['ReviewText'][:150]}...\"\n")
                
            print("[*] (Simulated LLM Generation): Based on the reviews, younger customers find these dresses to be highly flattering and perfect for summer wear, often rating them 5 stars.")

if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        print(f"[-] Error: Cleaned E-Commerce dataset not found at {DATA_PATH}")
        print("[-] Please run 'python src/ecommerce/pipeline.py' first.")
        exit(1)
        
    try:
        graph = EcommerceGraphRAG(URI, AUTH)
        graph.wipe_database()
        graph.setup_constraints()
        # We limit to 1000 rows to ensure fast execution for the demo
        graph.import_data(DATA_PATH, sample_size=1000)
        graph.run_graph_rag_query(product_class="Dresses", max_age=35)
    except Exception as e:
        print(f"\n[-] Failed to connect or execute Neo4j operations.")
        print(f"[-] Error: {e}")
        print(f"[-] Make sure Neo4j is running locally (Docker or Desktop) on {URI}")
        print(f"[-] See NEO4J_SETUP_GUIDE.md for instructions.")
    finally:
        if 'graph' in locals():
            graph.close()
