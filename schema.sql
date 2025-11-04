
CREATE TABLE users(
id INTEGER PRIMARY KEY,
username TEXT UNIQUE,
password_hash TEXT
);
CREATE TABLE star (
id INTEGER PRIMARY KEY,
name TEXT,
content TEXT,
user_id REFERENCES users);
CREATE TABLE type (
id INTEGER PRIMARY KEY,
name TEXT,
content TEXT);
CREATE TABLE method (
id INTEGER PRIMARY KEY,
name  TEXT);
CREATE TABLE planet (
id INTEGER PRIMARY KEY,
name TEXT,
content TEXT,
discovery INTEGER,
method TEXT,
user_id REFERENCES users);
CREATE TABLE planet_star (
planet_id INTEGER,
star_id INTEGER,
FOREIGN KEY (planet_id) REFERENCES planet(id) ON DELETE CASCADE,
FOREIGN KEY (star_id) REFERENCES star(id) ON DELETE CASCADE);
CREATE TABLE planet_type (
planet_id INTEGER,
type_id INTEGER,
FOREIGN KEY (planet_id) REFERENCES planet(id) ON DELETE CASCADE,
FOREIGN KEY (type_id) REFERENCES type(id));
CREATE TABLE planet_method (
planet_id INTEGER,
method_id INTEGER,
FOREIGN KEY (planet_id) REFERENCES planet(id) ON DELETE CASCADE,
FOREIGN KEY (method_id) REFERENCES method(id));

INSERt into METHOD (name) VALUES ("Suora kuvaus");
INSERt into METHOD (name) VALUES ("Gravitaatiolinssi");
INSERt into METHOD (name) VALUES ("Säteisnopeus");
INSERt into METHOD (name) VALUES ("Ylikulku");
INSERt into METHOD (name) VALUES ("Pulsarin ajoitus");

INSERt into type (name) VALUES ("Kaasujättiläinen");
INSERt into type (name) VALUES ("Maankaltainen planeetta");
INSERt into type (name) VALUES ("Jääjättiläinen");
INSERt into type (name) VALUES ("Kuuma Jupiter");

INSERT INTO star ( name, content, user_id) VALUES ("Aurinko", "Lähin tähtemme", 0);

INSERT INTO planet ( name, content, discovery, method, user_id) VALUES ("Maa", "Tutuin planeettamme",0,"Suora kuvaus", 0);

INSERT INTO planet_star (planet_id, star_id) VALUES (1,1);
INSERT INTO planet_method(planet_id, method_id) VALUES (1,1);