const parametro = window.location.pathname.split('/');
const destino = parametro[parametro.length - 2];
const lista_destino = ['PRIMEIRO', 'SEGUNDO', 'TERCEIRO', 'OLÍMPIADAS'];

document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById('header');
    const titulo_pagina = document.createElement('h1');
    destino_titulo = lista_destino[destino-1];
    if (destino == 4){
        titulo_pagina.innerHTML = destino_titulo;
    }
    else{
        titulo_pagina.innerHTML = 'MATERIAIS<br>' + destino_titulo + ' ANO';
    }
    header.appendChild(titulo_pagina);
});
