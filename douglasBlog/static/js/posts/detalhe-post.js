const parametro = window.location.pathname.split('/');
const post_id = parametro[parametro.length -2];

// Função async para carregar o post
async function carregarPost(){
    const response = await fetch(`/api/get/ver-post/${post_id}`);
    const post = await response.json();


    const container_conteudo = document.getElementById('container-conteudo');
    container_conteudo.innerHTML = post.conteudo;

    if (window.MathJax) {
        MathJax.typesetPromise()
            .then(() => {
                console.log("Equações renderizadas por MathJax!");
            })
            .catch((err) => console.error("Erro ao renderizar equações", err));
    }
    else {
        console.warn("MathJax ainda não foi carregado");
    }
}

carregarPost()