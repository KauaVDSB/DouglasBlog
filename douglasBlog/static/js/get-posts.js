// Requisição dos dados da db
fetch('/get-posts/')
.then(response => response.json())
.then(posts => {
    const container_posts = document.getElementById('resultado');
    posts.forEach(post => {
        // Renderiza no html
        const conteudoPost = document.createElement('div');
        container_posts.innerHTML = container_posts.innerHTML + `
        <h2> ${post.titulo} </h2>
        <h4> ${post.autor} </h4>

        ${post.conteudo}
        <hr>
        `;
        
        // Adiciona ao container
        container_posts.appendChild(conteudoPost);
    });
})
.catch(error => console.error("Erro ao exibir postagens: ", error));