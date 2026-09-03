// 1. Create Unique Constraints
CREATE CONSTRAINT customer_id IF NOT EXISTS FOR (c:Customer) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT product_id IF NOT EXISTS FOR (p:Product) REQUIRE p.class_name IS UNIQUE;
CREATE CONSTRAINT department_id IF NOT EXISTS FOR (d:Department) REQUIRE d.name IS UNIQUE;

// Note: The actual import of data from the CSV is handled dynamically via Python (scripts/neo4j_demo.py)
// because Neo4j local CSV import requires the CSV to be in the Neo4j `import` directory, 
// which is difficult to guarantee in a Docker/Desktop environment without strict mounting.
// The neo4j_demo.py script reads the CSV using pandas and pushes the nodes/edges via the Neo4j Driver.
