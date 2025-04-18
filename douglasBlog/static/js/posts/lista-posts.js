const urlParams = new URLSearchParams(window.location.search);
const pagina_url = parseInt(urlParams.get("page")) || 1;
const posts_por_pagina = 8;

let pagina_atual = pagina_url;
let pagina_total = 1;
let carregando = false;

// Objeto de Cache
const cache = {
    posts: {}, // armazena posts por pagina
    totalPosts: null
};

const loader_foguete = document.getElementById('loader-foguete'); 
// Carregamento dos posts
async function carregarPosts(page) {
    if (carregando) return;
    carregando = true;
    loader_foguete.style.display = 'block';
    const inicio_carregamento = performance.now(); // PERFORMANCE

    try{
        let posts;
        let totalPosts;

        if (cache.posts[page]) {
            posts = cache.posts[page];
            totalPosts = cache.totalPosts;
        }
        else {
            const response = await fetch(`/api/get/lista-posts?page=${page}`);
            posts = await response.json();

            cache.posts[page] = posts;
            if (!cache.totalPosts){
                totalPosts = parseInt(response.headers.get('X-Total-Count'));
                cache.totalPosts = totalPosts;
            }
            else{
                totalPosts = cache.totalPosts;
            }
        }
        
    
        pagina_total = Math.ceil(totalPosts / posts_por_pagina); // Menor número inteiro maior ou igual ao resultado

        // Atualiza container de posts
        const post_container = document.getElementById(`post-container`);
        post_container.innerHTML = ''; // Limpa posts antigos
        posts.forEach(post => {
            const post_div = document.createElement('div');
            post_div.className = 'post-div';

            const link = document.createElement('a');
            link.href = post.link;
            link.className = 'link-post';

            const imagem = document.createElement('img');
            imagem.src = post.imagem;
            imagem.className = 'imagem-post';
            imagem.loading = 'lazy';

            const conteudo_container = document.createElement('div');
            conteudo_container.className = 'conteudo-container';

            const titulo = document.createElement('h2');
            titulo.textContent = post.titulo;
            titulo.className = 'titulo-post';

            const prev_conteudo = document.createElement('p');
            prev_conteudo.textContent = post.conteudo;
            prev_conteudo.className = 'conteudo-post';

            post_container.appendChild(post_div);
            post_div.appendChild(link);
            link.appendChild(imagem);
            link.appendChild(conteudo_container);
            conteudo_container.appendChild(titulo);
            conteudo_container.appendChild(prev_conteudo);

            // Admin Functions

            if (isAdmin && adminView){
                const adminContainer = document.createElement('div');
                adminContainer.className = 'container-btn-admin';

                const btn_editar = document.createElement('a');
                btn_editar.href = `/admin/douglas-blog/posts/editar/${post.id}`;
                btn_editar.className = 'btn-editar';
                btn_editar.textContent = 'Editar';


                const btn_deletar = document.createElement('button');
                btn_deletar.className = 'btn-deletar'
                btn_deletar.textContent = 'Deletar';

                btn_deletar.onclick = async () => {
                    Swal.fire({
                        title: `Deseja deletar o post "${post.titulo}"?`,
                        text: 'Essa ação não poderá ser desfeita.',
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonColor: '#d33',
                        cancelButtonColor: '#3085d6',
                        confirmButtonText: 'Sim, deletar!',
                        cancelButtonText: 'Cancelar.'
                    }).then(async (result) => {
                        if (result.isConfirmed) {
                            const response = await fetch(`/admin/douglas-blog/posts/deletar/${post.id}`, {
                                method: 'DELETE'
                            });

                            if (response.ok) {
                                Swal.fire({
                                    title: 'Sucesso!',
                                    text: 'Post deletado com sucesso.',
                                    icon: 'success',
                                    timer: 1500,
                                    showConfirmButton: false
                                });
                            } else {
                                Swal.fire({
                                    tile: 'Falha ao deletar material.',
                                    text: 'Erro: ' + response.error,
                                    icon: 'error'
                                });
                            }
                        }
                    });
                };

                adminContainer.appendChild(btn_editar);
                adminContainer.appendChild(btn_deletar);
                post_div.appendChild(adminContainer);

            }

            setTimeout(() => post_div.classList.add('fade-in'), 50);
        });
                    
        // Atualiza botões de paginação
        atualizarBotoesDePaginacao();
    }
    catch (error) {
        console.error("Falha ao carregar posts: ", error);
        // Adicionar Swal.fire
    }
    finally {
        const fim_carregamento = performance.now();
        const tempo_carregamento = fim_carregamento - inicio_carregamento;
        const tempo_minimo = 500; //500ms

        const delay = tempo_minimo - tempo_carregamento;

        setTimeout(() => {
            loader_foguete.style.display = 'none';
            carregando = false;
        }, delay > 0 ? delay : 0);
        console.log('Tempo de carregamento: ' + tempo_carregamento);
        console.log('Loader durou por mais: ' + delay);
    }
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

    function atualizarUrlPagina(pagina) {
        const novaUrl = new URL(window.location);
        novaUrl.searchParams.set("page", pagina);
        window.history.pushState({}, '', novaUrl);
    }

    document.getElementById('botao-voltar').addEventListener('click', () => {
        if (pagina_atual > 1){
            pagina_atual--; // Volta uma página
            atualizarUrlPagina(pagina_atual);
            carregarPosts(pagina_atual); // Carrega os posts da página atual
        }
    })

    document.getElementById('botao-avancar').addEventListener('click', () => {
        if (pagina_atual < pagina_total){
            pagina_atual++; // Avança uma página
            atualizarUrlPagina(pagina_atual);
            carregarPosts(pagina_atual); // Carrega posts da página atual
        }
    })

    window.addEventListener('popstate', () => {
        const params = new URLSearchParams(window.location.search);
        const nova_pagina = parseInt(params.get('page')) || 1;
        pagina_atual = nova_pagina;
        carregarPosts(pagina_atual);
    })
//


carregarPosts(pagina_atual);