SELECT * FROM musicas;

INSERT INTO musicas (nome_musica, cantor_musica, genero_musica) VALUES
('Noite de Neon', 'Aurora & Os Sintéticos', 'Synthpop'),
('Raiz do Silêncio', 'João Veredas', 'MPB'),
('Tempestade de Fumaça', 'Infernal Diesel', 'Rock'),
('Horizonte em Chamas', 'Delta Aurora', 'Rock Alternativo'),
('Caminho Sem Volta', 'Rosa de Ferro', 'Metal Melódico');

CREATE TABLE musicas (
    id_musica INT PRIMARY KEY AUTO_INCREMENT,
    nome_musica VARCHAR(100),
    cantor_musica VARCHAR(100),
    genero_musica VARCHAR(50)
);

DROP TABLE IF EXISTS musicas;

select nome_musica, genero_musica from musica;

select * from musicas where genero_musica = "*";

select * from musica where genero_musica <> 'Funk';

select * from musica where id_musica > 5;

SELECT * FROM MUSICAS WHERE cantor_musica LIKE 'A%' OR 'a%'; 

update musicas set genero_musica = 'Sertanejo' where id_musica = 5;

update musicas set genero_musica = 'Sertanejo' where id_musica = 3;

delete from musicas where id_musica = 3;

CREATE  (insert)
READ    (select)
UPDATE  (update)
DELETE  (delete)

CREAD

truncate table usuario;

alter table usuario
add unique(login_usuario);