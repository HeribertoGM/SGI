CREATE TABLE MemTraMDADet (
    idMDA BIGINT NOT NULL,
    claNodo VARCHAR(10) NOT NULL,
    fecha DATE NOT NULL,
    hora SMALLINT NOT NULL,
    pml DECIMAL(10,5),
    pml_ene DECIMAL(10,5),
    pml_per DECIMAL(10,5),
    pml_cng DECIMAL(10,5),
    FechaUltimaMod TIMESTAMP,
    NombrePcMod NCHAR(30),
    ClaUsuarioMod INT,
    PRIMARY KEY (claNodo, fecha, hora)
);

CREATE TABLE MemTraMTRDet (
    idMTR BIGINT,
    claNodo VARCHAR(10) NOT NULL,
    fecha DATE NOT NULL,
    hora SMALLINT NOT NULL,
    pml DECIMAL(10,5),
    pml_ene DECIMAL(10,5),
    pml_per DECIMAL(10,5),
    pml_cng DECIMAL(10,5),
    FechaUltimaMod TIMESTAMP,
    NombrePcMod NCHAR(10),
    ClaUsuarioMod INT,
    PRIMARY KEY (claNodo, fecha, hora)
);

CREATE TABLE MemTraTcDet (
    idTc INT,
    fecha DATE NOT NULL,
    valor DECIMAL(10,6),
    FechaUltimaMod TIMESTAMP,
    NombrePcMod VARCHAR(30),
    ClaUsuarioMod INT,
    PRIMARY KEY (fecha)
);

CREATE TABLE MemTraTBFin (
    fecha DATE NOT NULL,
    TbFin NUMERIC(38,14),
    TbFinTGR NUMERIC(38,9),
    PRIMARY KEY (fecha)
)
