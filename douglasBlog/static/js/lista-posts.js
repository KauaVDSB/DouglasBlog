const posts_por_pagina = 6;
let pagina_atual = 1;
let pagina_total = 1;


// Carregamento dos posts
async function carregarPosts(page) {
    const response = await fetch(`/api/get/lista-posts?page=${page}`);
    const posts = await response.json();
    
    
    // Atualiza total de páginas na primeira chamada
    if (page === 1){
        const posts_total = parseInt(response.headers.get('X-Total-Count')); // Pega total de posts do cabeçalho
        pagina_total = Math.ceil(posts_total / posts_por_pagina); // Menor número inteiro maior ou igual ao resultado
    }

    // Atualiza container de posts
    const post_container = document.getElementById(`post-container`);
    post_container.innerHTML = ''; // Limpa posts antigos
    posts.forEach(post => {
        const post_div = document.createElement('div');
        post_div.style = 'overflow-wrap: break-word;'
        post_div.className = 'post-div col-4';

        const link = document.createElement('a');
        link.href = post.link;

        const titulo = document.createElement('h2');
        titulo.textContent = post.titulo;

        const prev_conteudo = document.createElement('p');
        prev_conteudo.textContent = post.conteudo;

        post_container.appendChild(post_div);
        post_div.appendChild(link);
        link.appendChild(titulo);
        link.appendChild(prev_conteudo);
    });

    // Atualiza botões de paginação
    atualizarBotoesDePaginacao();
}


// Botões de paginação
function atualizarBotoesDePaginacao(){
    const botao_voltar = document.getElementById('botao-voltar');
    const botao_avancar = document.getElementById('botao-avancar');

    // Desabilita botão voltar na primeira página
    botao_voltar.disabled = pagina_atual === 1;

    // Desabilita botão avançar na última página
    botao_avancar.disabled = pagina_atual === pagina_total;
}

document.getElementById('botao-voltar').addEventListener('click', () => {
    if (pagina_atual > 1){
        pagina_atual--; // Volta uma página
        carregarPosts(pagina_atual); // Carrega os posts da página atual
    }
})

document.getElementById('botao-avancar').addEventListener('click', () => {
    if (pagina_atual < pagina_total){
        pagina_atual++; // Avança uma página
        carregarPosts(pagina_atual); // Carrega posts da página atual
    }
})


carregarPosts(pagina_atual);