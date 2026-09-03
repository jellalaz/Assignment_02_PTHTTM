// ==============================================================================
// Neo4j Knowledge Graph Schema & Import Script — Assignment 02
// Application 3: E-Commerce Customer Behavior & Product Relationships
// ==============================================================================

// 1. Create Uniqueness Constraints
CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
FOR (c:Customer) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT product_id_unique IF NOT EXISTS
FOR (p:Product) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT category_name_unique IF NOT EXISTS
FOR (cat:Category) REQUIRE cat.name IS UNIQUE;

CREATE CONSTRAINT department_name_unique IF NOT EXISTS
FOR (d:Department) REQUIRE d.name IS UNIQUE;

CREATE CONSTRAINT review_id_unique IF NOT EXISTS
FOR (r:Review) REQUIRE r.id IS UNIQUE;

// 2. Sample Graph Ingestion Query (Subset demonstration)
// Nodes:
// (:Customer {id: 1, age: 34})
// (:Product {id: 1080, name: "Boho Maxi Dress"})
// (:Category {name: "Dresses"})
// (:Department {name: "Dresses"})
// (:Review {id: 101, rating: 5, recommended: 1, sentiment: "Positive", text: "Loved this gorgeous dress!"})

// Relationships:
// (:Customer)-[:WROTE]->(:Review)
// (:Review)-[:ABOUT]->(:Product)
// (:Product)-[:BELONGS_TO]->(:Category)
// (:Category)-[:PART_OF]->(:Department)

// 3. Example Analytical Cypher Queries:

// Query A: Find top recommended products with 5-star reviews
MATCH (p:Product)<-[:ABOUT]-(r:Review)
WHERE r.rating = 5 AND r.recommended = 1
RETURN p.id AS ProductID, count(r) AS FiveStarCount, p.name AS ProductName
ORDER BY FiveStarCount DESC
LIMIT 10;

// Query B: Find customer segments by age and category interest
MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(p:Product)-[:BELONGS_TO]->(cat:Category)
WHERE r.recommended = 1
RETURN cat.name AS Category, avg(c.age) AS AvgCustomerAge, count(r) AS TotalRecommendations
ORDER BY TotalRecommendations DESC;

// Query C: Trace negative feedback for quality control
MATCH (c:Customer)-[:WROTE]->(r:Review)-[:ABOUT]->(p:Product)
WHERE r.rating <= 2 AND r.recommended = 0
RETURN p.id AS ProductID, r.text AS Feedback, c.age AS CustomerAge
LIMIT 15;
