CREATE SCHEMA covinfo;

CREATE TABLE base_regiao(
	id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE base_estado(
	id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    sigla VARCHAR(10) NOT NULL,
    regiao_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(regiao_id) REFERENCES base_regiao(id)
);

CREATE TABLE base_municipio(
	id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    populacao DOUBLE NOT NULL,
    estado_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(estado_id) REFERENCES base_estado(id)
);

CREATE TABLE base_casos(
	id INT NOT NULL AUTO_INCREMENT,
    casos DOUBLE NOT NULL,
    casos_novos DOUBLE NOT NULL,
    obitos DOUBLE NOT NULL,
    obitos_novos DOUBLE NOT NULL,
    recuperados DOUBLE NOT NULL,
    acompanhamento DOUBLE NOT NULL,
    semana INT NOT NULL,
    data date NOT NULL,
    regiao_id INT NOT NULL,
    estado_id INT NOT NULL,
    municipio_id INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(regiao_id) REFERENCES base_regiao(id),
    FOREIGN KEY(estado_id) REFERENCES base_estado(id),
    FOREIGN KEY(municipio_id) REFERENCES base_base_casosmunicipio(id)
);