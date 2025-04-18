function construirAula(material_aula, conteudo_container){
    const conteudo_aula = material_aula.trim();

    const container_aula = document.createElement('div');
    container_aula.className = 'aula';
    conteudo_container.appendChild(container_aula);
    
    const link_aula = document.createElement('a');
    if (!conteudo_aula.startsWith('http://') && (!conteudo_aula.startsWith('https://'))){
        link_aula.href = `https://${conteudo_aula}`;
    }
    else{
        link_aula.href = conteudo_aula;
    }
    link_aula.target = 'blank';
    link_aula.innerHTML =
    `<i class="bi bi-youtube"></i>
    <div>
        <h3>Aula</h3> <p>Assista a aula sobre o assunto.</p>
    </div>`;
    container_aula.appendChild(link_aula);

}
function construirResumo(material_resumo, conteudo_container, material_titulo){
    const conteudo_resumo = material_resumo.trim();

    const container_resumo = document.createElement('div');
    container_resumo.className = 'resumo';
    conteudo_container.appendChild(container_resumo);

    const download_resumo = document.createElement('a');
    download_resumo.href = conteudo_resumo;
    download_resumo.download = conteudo_resumo;
    download_resumo.target = 'blank';
    download_resumo.innerHTML =
    `<i class="bi bi-download"></i>
    <div>
        <h3>Resumo</h3>
        <p> Baixe o PDF com resumo sobre a aula. </p>
    </div>`;

    container_resumo.appendChild(download_resumo);
}
function construirLista(material_lista_exercicios, conteudo_container){
    const conteudo_lista_exercicios = material_lista_exercicios.trim();
    
    const container_lista_exercicios = document.createElement('div');
    container_lista_exercicios.className = 'lista-exercicios';
    conteudo_container.appendChild(container_lista_exercicios);
    
    
    const download_lista_exercicios = document.createElement('a');
    download_lista_exercicios.href = conteudo_lista_exercicios;
    download_lista_exercicios.download = conteudo_lista_exercicios;
    download_lista_exercicios.target = 'blank';
    download_lista_exercicios.innerHTML =
    `<i class="bi bi-download"></i>
    <div>
        <h3>Lista de Exercícios</h3>
        <p> Baixe o PDF de exercícios da aula. </p>
    </div>`;

    container_lista_exercicios.appendChild(download_lista_exercicios);
}


function temCaminho(caminho){
    if (caminho !== '' && caminho !== null){
        console.log('valido');
        return true;
    }
    else {
        console.log('invalido');
    }
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


    // Cria container dos posts
    const material_container = document.getElementById(`material-container`);

    materiais.forEach(material => {

        const material_div = document.createElement('div');
        material_div.className = 'material-div';
        
        const titulo = document.createElement('h2');
        titulo.textContent = material.titulo;
        
        const conteudo_container = document.createElement('div');
        conteudo_container.className = 'conteudo-container';
        console.log(material.aula);
        console.log(material.resumo);
        console.log(material.lista_exercicios);
        console.log('------------');
        if (material.aula){
            construirAula(material.aula, conteudo_container);
        }
        if (temCaminho(material.resumo)){
            construirResumo(material.resumo, conteudo_container, material.titulo.replaceAll(" ", "-"));
        }
        if (temCaminho(material.lista_exercicios)){
            construirLista(material.lista_exercicios, conteudo_container, material.titulo.replaceAll(" ", "-"));
        }

        material_container.appendChild(material_div);
        material_div.appendChild(titulo);
        material_div.appendChild(conteudo_container);
    });
}

carregarMateriais(destino);