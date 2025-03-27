const parametro = window.location.pathname.split('/');
const destino = parametro[parametro.length - 2];

// Carregamento dos materiais
async function carregarMateriais(destino) {
    const response = await fetch(`/api/get/lista-materiais/${destino}`);
    const materiais = await response.json();
    console.log(materiais)


    // Cria container dos posts
    const material_container = document.getElementById(`material-container`);
    materiais.forEach(material => {
        const material_div = document.createElement('div');
        material_div.className = 'material-div col-4';

        const titulo = document.createElement('h2');
        titulo.textContent = material.titulo;

        material_container.appendChild(material_div);
        material_div.appendChild(titulo);
    });
}

carregarMateriais(destino);