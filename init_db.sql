-- Drop tables if they exist
DROP TABLE IF EXISTS Assignments;
DROP TABLE IF EXISTS SkillAssignments;
DROP TABLE IF EXISTS Tasks;
DROP TABLE IF EXISTS Machines;
DROP TABLE IF EXISTS Skills;
DROP TABLE IF EXISTS Operators;

-- Create Operators table if it doesn't exist
CREATE TABLE Operators (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE Skills (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create Tasks table if it doesn't exist
CREATE TABLE Tasks (
    id SERIAL PRIMARY KEY,
    affaire TEXT NOT NULL,
    sousEnsemble TEXT,
    operation TEXT,
    periode TEXT CHECK (periode IN ('MATIN', 'SOIR', '')) DEFAULT '',
    couleur TEXT
);

-- Create Assignments table if it doesn't exist
CREATE TABLE Assignments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    operator_id INTEGER,
    task_id INTEGER,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (operator_id) REFERENCES Operators(id),
    FOREIGN KEY (task_id) REFERENCES Tasks(id)
);

CREATE TABLE SkillAssignments (
    op_id INTEGER,
    s_id INTEGER,
    PRIMARY KEY (op_id, s_id),
    FOREIGN KEY (op_id) REFERENCES Operators(id),
    FOREIGN KEY (s_id) REFERENCES Skills(id)
);

-- Create Machines table if it doesn't exist
CREATE TABLE Machines (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Insert operators with name and id
INSERT INTO Operators (id, name) VALUES (308, 'MAZEL Nadine');
INSERT INTO Operators (id, name) VALUES (285, 'ESPOSITO Lorenzo');
INSERT INTO Operators (id, name) VALUES (307, 'MAGHANDZI Davy');
INSERT INTO Operators (id, name) VALUES (144, 'LE FLOCH Yves');
INSERT INTO Operators (id, name) VALUES (98, 'GUERREIRO-NETO Marianne');
INSERT INTO Operators (id, name) VALUES (304, 'SEPINA Jerome');
INSERT INTO Operators (id, name) VALUES (309, 'DURAND Lise');
INSERT INTO Operators (id, name) VALUES (211, 'EHLINGER Giovanna');
INSERT INTO Operators (id, name) VALUES (202, 'MERONO Thierry');
INSERT INTO Operators (id, name) VALUES (291, 'FOURNIER Stephanie');
INSERT INTO Operators (id, name) VALUES (147, 'CAMEZUL Caroline');
INSERT INTO Operators (id, name) VALUES (317, 'GARNIER Stephanie');
INSERT INTO Operators (id, name) VALUES (342, 'VALEUR Valerie');
INSERT INTO Operators (id, name) VALUES (303, 'GAICHE Brigitte');
INSERT INTO Operators (id, name) VALUES (284, 'MARTINO Fabien');
INSERT INTO Operators (id, name) VALUES (326, 'MOREIRA Katia');
INSERT INTO Operators (id, name) VALUES (296, 'RAGE Maureen');
INSERT INTO Operators (id, name) VALUES (190, 'LETELLIER Estelle');
INSERT INTO Operators (id, name) VALUES (340, 'DAVRINCHE Kevin');
INSERT INTO Operators (id, name) VALUES (336, 'CAMPISTRON Cyril');
INSERT INTO Operators (id, name) VALUES (338, 'PEREZ Michel');
INSERT INTO Operators (id, name) VALUES (316, 'RIBES Dany');
INSERT INTO Operators (id, name) VALUES (328, 'GUILLOTIN Dany');
INSERT INTO Operators (id, name) VALUES (311, 'BOSCOURN Remi');
INSERT INTO Operators (id, name) VALUES (322, 'PACHECO Jerome');
INSERT INTO Operators (id, name) VALUES (292, 'PARRIAUD Johanna');
INSERT INTO Operators (id, name) VALUES (302, 'BOUDEAUD Kevin');
INSERT INTO Operators (id, name) VALUES (348, 'DOUX Clemence');
INSERT INTO Operators (id, name) VALUES (293, 'GENDROP Cindy');
INSERT INTO Operators (id, name) VALUES (221, 'RENAULT Magali');
INSERT INTO Operators (id, name) VALUES (155, 'TOMEI Thierry');
INSERT INTO Operators (id, name) VALUES (134, 'GUEFFIER Mickael');
INSERT INTO Operators (id, name) VALUES (250, 'HOOGLAND Watte');
INSERT INTO Operators (id, name) VALUES (130, 'DIEBOLD Catherine');
INSERT INTO Operators (id, name) VALUES (347, 'MAURICE Alexandre');
INSERT INTO Operators (id, name) VALUES (305, 'BOUILLOUX Alison');
INSERT INTO Operators (id, name) VALUES (315, 'LAGARRIGUE Mathieu');
INSERT INTO Operators (id, name) VALUES (321, 'ANDREU Sophie');
INSERT INTO Operators (id, name) VALUES (306, 'MIMOSO Marie Christine');
INSERT INTO Operators (id, name) VALUES (225, 'MARCHISIO Remy');
INSERT INTO Operators (id, name) VALUES (261, 'CANO Joelle');

INSERT INTO Skills (id, name) VALUES
(1, 'Welding'),
(2, 'Machining'),
(3, 'Assembly'),
(4, 'Painting'),
(5, 'Quality Control');

INSERT INTO Machines (id, name) VALUES
(0, 'Poste TA 0'),
(1, 'Poste TA 1'),
(2, 'Poste TA 2'),
(3, 'Poste TA 3'),
(4, 'Poste TA 4'),
(5, 'Poste TA 5'),
(6, 'Poste TA 6'),
(7, 'Poste TA 7'),
(8, 'Poste TA 8'),
(9, 'Poste TA 9'),
(10, 'Machine de coupe Schleudinger');
