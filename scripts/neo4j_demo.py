"""
Optional Neo4j Graph Integration Demo — Assignment 02
Demonstrates how to ingest a clean subset of E-Commerce reviews into Neo4j
and query customer-product-category relationships.
"""

import os
import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "ecommerce" / "Womens Clothing E-Commerce Reviews.csv"

# Configuration defaults
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password123")


def run_neo4j_demo(sample_size=100):
    print("=" * 60)
    print("NEO4J GRAPH INTEGRATION DEMO (OPTIONAL EXTENSION)")
    print("=" * 60)
    print(f"Connecting to: {NEO4J_URI} as user: {NEO4J_USER}")

    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("\n[!] The 'neo4j' Python driver is not installed.")
        print("    Install it via: pip install neo4j")
        print("    See NEO4J_SETUP_GUIDE.md for detailed instructions.")
        return False

    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            # Test connectivity
            result = session.run("RETURN 1 AS connected")
            connected = result.single()["connected"]
            print(f"✓ Connected to Neo4j successfully! (Result: {connected})")

            # Load sample data
            df = pd.read_csv(DATA_PATH).dropna(subset=['Review Text']).head(sample_size)
            print(f"  Ingesting sample of {len(df)} records into Knowledge Graph...")

            for idx, row in df.iterrows():
                query = """
                MERGE (c:Customer {id: $cust_id, age: $age})
                MERGE (p:Product {id: $prod_id})
                MERGE (cat:Category {name: $cat_name})
                MERGE (d:Department {name: $dept_name})
                MERGE (p)-[:BELONGS_TO]->(cat)
                MERGE (cat)-[:PART_OF]->(d)
                CREATE (r:Review {
                    id: $rev_id,
                    rating: $rating,
                    recommended: $rec,
                    text: $text
                })
                CREATE (c)-[:WROTE]->(r)
                CREATE (r)-[:ABOUT]->(p)
                """
                session.run(query, {
                    "cust_id": int(idx),
                    "age": int(row["Age"]),
                    "prod_id": int(row["Clothing ID"]),
                    "cat_name": str(row.get("Class Name", "General")),
                    "dept_name": str(row.get("Department Name", "Tops")),
                    "rev_id": int(idx),
                    "rating": int(row["Rating"]),
                    "rec": int(row["Recommended IND"]),
                    "text": str(row["Review Text"])[:100]
                })

            print("✓ Sample Knowledge Graph constructed successfully!")
        driver.close()
        return True

    except Exception as e:
        print(f"\n[!] Neo4j database is not running or credentials invalid: {e}")
        print("    This is an optional extension. Please refer to NEO4J_SETUP_GUIDE.md")
        return False


if __name__ == "__main__":
    run_neo4j_demo()
