-- 1. Selecionar todos os posts ordenados por data (mais recente primeiro)
SELECT * 
FROM hub_post 
ORDER BY created_at DESC;

-- 2. Selecionar todos os comentários de um post específico (ex: ID 1)
SELECT * 
FROM hub_comment 
WHERE post_id = 1;

-- 3. Selecionar comentários de um post trazendo o título do post e renomeando a data do post para post_date (JOIN)
SELECT 
    c.text AS comentario,
    c.created_at AS data_comentario,
    p.title AS titulo_post,
    p.created_at AS post_date
FROM 
    hub_comment c
JOIN 
    hub_post p ON c.post_id = p.id
WHERE 
    p.id = 1;

-- 4. Selecionar todos os posts da categoria "Transmissão" (JOIN entre Post, Category e tabela intermediária)
-- Nota: Usando LIKE para pegar "Transmissão ao Vivo"
SELECT 
    p.title,
    p.created_at
FROM 
    hub_post p
JOIN 
    hub_post_categories pc ON p.id = pc.post_id
JOIN 
    hub_category c ON pc.category_id = c.id
WHERE 
    c.name LIKE '%Transmissão%';

-- 5. Selecionar categorias que possuem 2 ou mais posts vinculados (GROUP BY/HAVING)
SELECT 
    c.name,
    COUNT(pc.post_id) as total_posts
FROM 
    hub_category c
JOIN 
    hub_post_categories pc ON c.id = pc.category_id
GROUP BY 
    c.id, c.name
HAVING 
    COUNT(pc.post_id) >= 2;
