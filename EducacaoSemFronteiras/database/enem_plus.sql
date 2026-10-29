CREATE DATABASE IF NOT EXISTS enem_plus;
USE enem_plus;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS temas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    dificuldade VARCHAR(30) NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS redacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tema_id INT NOT NULL,
    texto TEXT NOT NULL,
    nota_total INT DEFAULT 0,
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (tema_id) REFERENCES temas(id)
);

CREATE TABLE IF NOT EXISTS notas_competencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    redacao_id INT NOT NULL,
    competencia1 INT DEFAULT 0,
    competencia2 INT DEFAULT 0,
    competencia3 INT DEFAULT 0,
    competencia4 INT DEFAULT 0,
    competencia5 INT DEFAULT 0,
    FOREIGN KEY (redacao_id) REFERENCES redacoes(id)
);

INSERT INTO usuarios (nome,email,senha) VALUES
('Aluno Teste','aluno@teste.com','123456')
ON DUPLICATE KEY UPDATE nome=nome;

INSERT INTO temas (titulo,descricao,dificuldade) VALUES
('Desafios da educação digital no Brasil','Os impactos da tecnologia no processo educacional brasileiro.','Media'),
('Desafios para combater a desinformação no Brasil','Os efeitos das notícias falsas na sociedade brasileira.','Dificil'),
('A importância da educação financeira para os jovens','A necessidade de preparar jovens para decisões financeiras.','Facil');

DROP PROCEDURE IF EXISTS buscar_temas;
DROP PROCEDURE IF EXISTS criar_redacao;
DROP PROCEDURE IF EXISTS ranking_alunos;
DROP PROCEDURE IF EXISTS relatorio_aluno;
DROP PROCEDURE IF EXISTS evolucao_aluno;
DROP PROCEDURE IF EXISTS competencia_fraca;

DELIMITER //

CREATE PROCEDURE buscar_temas(IN termo VARCHAR(255), IN dificuldade_filtro VARCHAR(30))
BEGIN
    SELECT id,titulo,descricao,dificuldade,criado_em
    FROM temas
    WHERE (termo IS NULL OR titulo LIKE CONCAT('%',termo,'%') OR descricao LIKE CONCAT('%',termo,'%'))
      AND (dificuldade_filtro IS NULL OR dificuldade=dificuldade_filtro)
    ORDER BY criado_em DESC;
END //

CREATE PROCEDURE criar_redacao(IN p_usuario INT, IN p_tema INT, IN p_texto TEXT)
BEGIN
    INSERT INTO redacoes(usuario_id,tema_id,texto,nota_total)
    VALUES(p_usuario,p_tema,p_texto,0);
    SELECT id,usuario_id,tema_id,texto,nota_total,data_envio
    FROM redacoes WHERE id=LAST_INSERT_ID();
END //

CREATE PROCEDURE ranking_alunos()
BEGIN
    SELECT u.id,u.nome,COUNT(r.id) AS quantidade_redacoes,
           ROUND(AVG(r.nota_total),2) AS media
    FROM usuarios u
    INNER JOIN redacoes r ON u.id=r.usuario_id
    GROUP BY u.id,u.nome
    HAVING COUNT(r.id)>0
    ORDER BY media DESC;
END //

CREATE PROCEDURE relatorio_aluno(IN p_usuario INT)
BEGIN
    SELECT u.nome,
           COUNT(r.id) AS total_redacoes,
           COALESCE(ROUND(AVG(r.nota_total),2),0) AS media,
           COALESCE(MAX(r.nota_total),0) AS melhor_nota,
           COALESCE(MIN(r.nota_total),0) AS menor_nota
    FROM usuarios u
    LEFT JOIN redacoes r ON u.id=r.usuario_id
    WHERE u.id=p_usuario
    GROUP BY u.id,u.nome;
END //

CREATE PROCEDURE evolucao_aluno(IN p_usuario INT)
BEGIN
    SELECT r.id,t.titulo AS tema,r.nota_total,r.data_envio
    FROM redacoes r
    INNER JOIN temas t ON r.tema_id=t.id
    WHERE r.usuario_id=p_usuario
    ORDER BY r.data_envio ASC;
END //

CREATE PROCEDURE competencia_fraca(IN p_usuario INT)
BEGIN
    SELECT
      COALESCE(ROUND(AVG(n.competencia1),2),0) AS competencia1,
      COALESCE(ROUND(AVG(n.competencia2),2),0) AS competencia2,
      COALESCE(ROUND(AVG(n.competencia3),2),0) AS competencia3,
      COALESCE(ROUND(AVG(n.competencia4),2),0) AS competencia4,
      COALESCE(ROUND(AVG(n.competencia5),2),0) AS competencia5
    FROM notas_competencias n
    INNER JOIN redacoes r ON n.redacao_id=r.id
    WHERE r.usuario_id=p_usuario;
END //

DELIMITER ;
