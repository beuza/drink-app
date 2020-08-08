CREATE TABLE events(
   event_id SERIAL PRIMARY KEY,
   name VARCHAR (50) NOT NULL,
   invitation_key VARCHAR (50) NOT NULL
);
CREATE TABLE devices(
   device_id SERIAL PRIMARY KEY,
   unique_identifier VARCHAR (50) NOT NULL UNIQUE,
   count_of_wins INTEGER
);
CREATE TABLE users(
   user_id SERIAL PRIMARY KEY,
   device_id INTEGER REFERENCES devices(device_id),
   name VARCHAR (50) NOT NULL,
   isadmin VARCHAR (50) NOT NULL,   
   event_id INTEGER REFERENCES events(event_id) ON DELETE CASCADE
);
CREATE TABLE cycles(
   cycle_id SERIAL PRIMARY KEY,
   state VARCHAR (50) NOT NULL,
   EndDateTime TIMESTAMP,
   event_id INTEGER REFERENCES events(event_id) ON DELETE CASCADE
);
CREATE TABLE votes(
   user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
   cycle_id INTEGER REFERENCES cycles(cycle_id) ON DELETE CASCADE,
   PRIMARY KEY (user_id,cycle_id),
   voted_user_id INTEGER REFERENCES users(user_id)
);