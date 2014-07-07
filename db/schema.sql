CREATE TABLE customers (
  id INTEGER PRIMARY KEY autoincrement,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  birth TEXT NOT NULL,
  sex INTEGER,
  email TEXT,
  phone INTEGER,
  entered TEXT NOT NULL
);

-- All references to customers.id in later tables must be 
-- called "customer_id"
create TABLE laser (       
  laserid INTEGER PRIMARY KEY autoincrement,
  codename TEXT,
  customer_id INTEGER REFERENCES customers
);

CREATE TABLE learnToSkate (
  skate_id INTEGER PRIMARY KEY autoincrement,
  skill INTEGER,
  customer_id INTEGER REFERENCES customers
);

CREATE TABLE visit (
  visit_id INTEGER PRIMARY KEY autoincrement,
  visit_time TEXT NOT NULL,
  customer_id INTEGER REFERENCES customers
);


