CREATE TABLE freemage_files
(
    UsID INTEGER NOT NULL,
    UniqueID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    FileNamesCSV TEXT NOT NULL,
    Timestamp INTEGER NOT NULL,
    TagsCSV TEXT
);
CREATE TABLE freemage_data
(
    UsID INTEGER NOT NULL,
    TagName TEXT NOT NULL PRIMARY KEY,
    FileUIDsCSV TEXT
);
