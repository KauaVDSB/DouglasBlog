function verificarAula(material_aula, conteudo_container){
    const conteudo_aula = material_aula.replace(`<div class='container-aula'>`, "")
    const container_aula = document.createElement('div');
    container_aula.className = 'container-aula';
    container_aula.textContent = conteudo_aula;
    conteudo_container.appendChild(container_aula);
}
function verificarMapa(material_mapa_mental, conteudo_container){
    const conteudo_mapa_mental = material_mapa_mental.replace(`<div class='container-mapa-mental'>`, "")
    const container_mapa_mental = document.createElement('div');
    container_mapa_mental.className = 'container-aula';
    container_mapa_mental.textContent = conteudo_mapa_mental;
    conteudo_container.appendChild(container_mapa_mental);
}
function verificarLista(material_lista_exercicios, conteudo_container){
    const conteudo_lista_exercicios = material_lista_exercicios.replace(`<div class='container-lista-exercicios'>`, "")
    const container_lista_exercicios = document.createElement('div');
    container_lista_exercicios.className = 'container-aula';
    container_lista_exercicios.textContent = conteudo_lista_exercicios;
    conteudo_container.appendChild(container_lista_exercicios);
}

// Carregamento dos materiais
async function carregarMateriais(destino) {
    const response = await fetch(`/api/get/lista-materiais/${destino}`);
    const data = await response.json(); // retorna materiais e total
    
    if (!Array.isArray(data.materiais)){
        console.error("Erro: materiais não é uma lista.", data.materiais);
        return;
    }
    
    const materiais = data.materiais;
    console.log(materiais);


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
        if (material.aula){
            verificarAula(material.aula, conteudo_container);
        }
        if (material.mapa_mental){
            verificarMapa(material.mapa_mental, conteudo_container);
        }
        if (material.lista_exercicios){
            verificarLista(material.lista_exercicios, conteudo_container);
        }

        material_container.appendChild(material_div);
        material_div.appendChild(titulo);
        material_div.appendChild(conteudo_container);
    });
}

carregarMateriais(destino);