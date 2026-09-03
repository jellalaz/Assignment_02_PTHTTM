# Neo4j Graph Database Setup Guide

This guide explains how to set up the **Neo4j Graph Database** extension for the E-Commerce Customer Behavior module of this project.

The traditional Machine Learning models (Logistic Regression, TF-IDF) in this project treat each customer review as an isolated event. By introducing Neo4j, we convert the tabular data into a **Knowledge Graph**, linking `Customers`, `Products`, `Departments`, and `Reviews` together. This architecture serves as the foundation for an advanced **Graph RAG (Retrieval-Augmented Generation)** Chatbot.

---

## 1. Prerequisites

You can run Neo4j using either Docker (Recommended) or Neo4j Desktop.

### Option A: Using Docker (Recommended)
Run the following command to start a Neo4j Enterprise edition container with the APOC (Awesome Procedures on Cypher) plugin enabled:

```bash
docker run \
    -p 7474:7474 -p 7687:7687 \
    -d \
    --name neo4j-ecommerce \
    --env NEO4J_AUTH=neo4j/password \
    --env NEO4J_apoc_export_file_enabled=true \
    --env NEO4J_apoc_import_file_enabled=true \
    --env NEO4J_apoc_import_file_use__neo4j__config=true \
    --env NEO4J_PLUGINS='["apoc"]' \
    neo4j:5.12.0
```

### Option B: Using Neo4j Desktop
1. Download and install [Neo4j Desktop](https://neo4j.com/download/).
2. Create a new Local DBMS and set the password to `password` (or update `scripts/neo4j_demo.py` if you use a different password).
3. Start the database.

---

## 2. Importing the E-Commerce Graph

Once your database is running on `bolt://localhost:7687` (or `neo4j://localhost:7687`), you need to run the Cypher script to create the schema constraints and import sample data.

We provide a ready-to-use Python script that automatically connects to your local Neo4j instance, wipes any existing data, establishes the constraints, and populates the graph using the E-commerce dataset.

Ensure your Python environment is activated:
```bash
conda activate ai-env
pip install neo4j pandas
```

Run the graph construction script:
```bash
python scripts/neo4j_demo.py
```

---

## 3. The Graph Schema

The Cypher script builds the following schema:

### Nodes (Entities)
- `(:Customer {age: Integer})`: The shopper leaving the review.
- `(:Product {class_name: String})`: The specific clothing item.
- `(:Department {name: String, division: String})`: The department the product belongs to (e.g., Tops, Bottoms).
- `(:Review {text: String, rating: Integer, recommended: Boolean})`: The actual review text and sentiment.

### Relationships (Edges)
- `(Customer)-[:WROTE]->(Review)`
- `(Review)-[:ABOUT]->(Product)`
- `(Product)-[:BELONGS_TO]->(Department)`

---

## 4. Querying the Graph (Cypher Examples)

Open your Neo4j Browser at [http://localhost:7474](http://localhost:7474) (Login: `neo4j` / `password`). Try the following Cypher queries:

### Find Top Recommended Products in the "Dresses" Department
```cypher
MATCH (p:Product)-[:BELONGS_TO]->(d:Department {name: 'Dresses'})
MATCH (r:Review {recommended: true})-[:ABOUT]->(p)
RETURN p.class_name, count(r) AS PositiveReviews
ORDER BY PositiveReviews DESC
LIMIT 5;
```

### Graph RAG Context: Find all reviews by customers aged 25-30 for a specific product class
```cypher
MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(p:Product {class_name: 'Blouses'})
WHERE c.age >= 25 AND c.age <= 30
RETURN c.age, r.rating, r.text
LIMIT 10;
```

---

## 5. Next Steps: Graph RAG Chatbot Integration

With this graph operational, the next architectural step is to connect an LLM (e.g., OpenAI GPT-4 or local LLaMA 3). 

When a user asks: *"What are the most comfortable dresses for women under 30?"*
1. **Entity Extraction**: The LLM identifies `Product=Dresses` and `Customer.age < 30`.
2. **Graph Retrieval**: A Cypher query fetches exactly those sub-graphs (the specific positive reviews connected to those demographics).
3. **Augmented Generation**: The LLM synthesizes the highly-contextual retrieved review texts into a natural, conversational recommendation.
