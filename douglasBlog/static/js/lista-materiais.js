const parametro = window.location.pathname.split('/');
const destino = parametro[parametro.length - 2];


function verificarAula(conteudo_material, conteudo_container){
    let inicio = conteudo_material.indexOf(`<div class='container-aula'>`);
    let fim = conteudo_material.indexOf(`<div class='container-mapa-mental'>`);
    console.log(conteudo_material.slice(inicio + `<div class='container-aula'>`.length, fim));
    conteudo_material = conteudo_material.slice(0, inicio) + conteudo_material.slice(inicio + `<div class='container-aula'>`.length, fim);
    const container_aula = document.createElement('div');
    container_aula.className = 'container-aula';
    container_aula.textContent = conteudo_material;
    conteudo_container.appendChild(container_aula);
    console.log("essa foi a aula");
}
function verificarMapa(conteudo_material, conteudo_container){
    let inicio = conteudo_material.indexOf(`<div class='container-mapa-mental'>`);
    let fim = conteudo_material.indexOf(`<div class='container-lista-exercicios'>`);
    console.log(conteudo_material.slice(inicio + `<div class='container-mapa-mental'>`.length, fim));
    conteudo_material = conteudo_material.slice(inicio + `<div class='container-mapa-mental'>`.length, fim);
    const container_mapa_mental = document.createElement('div');
    container_mapa_mental.className = 'container-mapa-mental';
    container_mapa_mental.textContent = conteudo_material;
    conteudo_container.appendChild(container_mapa_mental);
    console.log("esse foi o mapa");
}
function verificarLista(conteudo_material, conteudo_container){
    let inicio = conteudo_material.indexOf(`<div class='container-lista-exercicios'>`);
    console.log(conteudo_material.slice(inicio + `<div class='container-lista-exercicios'>`.length));
    conteudo_material = conteudo_material.slice(inicio + `<div class='container-lista-exercicios'>`.length);
    const container_lista_exercicios = document.createElement('div');
    container_lista_exercicios.className = 'container-lista-exercicios';
    container_lista_exercicios.textContent = conteudo_material;
    conteudo_container.appendChild(container_lista_exercicios);
    console.log("essa foi a lista");
}

// Carregamento dos materiais
async function carregarMateriais(destino) {
    const response = await fetch(`/api/get/lista-materiais/${destino}`);
    const materiais = await response.json();


    // Cria container dos posts
    const material_container = document.getElementById(`material-container`);
    materiais.forEach(material => {
        
        
        const material_div = document.createElement('div');
        material_div.className = 'material-div col-4';
        material_div.style = 'border-bottom: 1px solid; overflow:hidden;';
        
        const titulo = document.createElement('h2');
        titulo.textContent = material.titulo;
        
        // Criar split dos materiais para verificar quais são existentes.
        const conteudo_container = document.createElement('div');
        conteudo_container.className = 'conteudo-container';
        let conteudo_material = material.materiais;
        if (conteudo_material.includes(`<div class='container-aula'>`)){
            verificarAula(conteudo_material, conteudo_container);
        }
        if (conteudo_material.includes(`<div class='container-mapa-mental'>`)){
            verificarMapa(conteudo_material, conteudo_container);
        }
        if (conteudo_material.includes(`<div class='container-lista-exercicios'>`)){
            verificarLista(conteudo_material, conteudo_container);
        }

        material_container.appendChild(material_div);
        material_div.appendChild(titulo);
        material_div.appendChild(conteudo_container);
    });
}

carregarMateriais(destino);