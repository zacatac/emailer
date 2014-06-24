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

CREATE TABLE laser (       
  laserid INTEGER PRIMARY KEY autoincrement,
  codename TEXT,
  customerid INTEGER REFERENCES customers
);

CREATE TABLE learnToSkate (
  skate_id INTEGER PRIMARY KEY autoincrement,
  recent_attendance INTEGER,
  customerid INTEGER REFERENCES customers
);

CREATE TABLE visit (
  visit_id INTEGER PRIMARY KEY autoincrement,
  visit_time TEXT NOT NULL,
  customer_id INTEGER,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
