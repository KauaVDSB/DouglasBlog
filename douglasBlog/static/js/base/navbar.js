// SEGURANÇA
const params = new URLSearchParams(window.location.search);
const ACESSO_LOGIN = document.getElementById('menu-navbar').dataset.acesso;
if (params.get('acesso') === ACESSO_LOGIN) {
    params.delete('acesso');
    const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    window.history.replaceState({}, '', newUrl);
}

async function carregar_views_totais() {
    let views_totais;
    const contador_views_totais = document.getElementById('contador-views-totais');
    
    try{
        const response = await fetch(`/api/analytics/total`);
        views_totais = await response.json();
        contador_views_totais.innerText = views_totais.total;
    }
    catch(error){
        console.error("Falha ao carregar número de visualizações.", error);
    }
}

carregar_views_totais();
// MOBILE
// Script para ativar e desativar menu lateral em dispositivos pequenos.

const openButton = document.querySelector('.menu-toggle.open');
const closeButton = document.querySelector('.menu-toggle.close');
const menu = document.querySelector('.menu');



// Torna menu lateral visível
openButton.addEventListener('click', () => {
    menu.classList.add('active');
});

// Esconde menu lateral
closeButton.addEventListener('click', () => {
    menu.classList.remove('active');
});

// Fecha o menu lateral em outras ocasiões
document.addEventListener('click', (event) => {
    if (event.target !== menu && event.target !== openButton)
    {
        menu.classList.remove('active');
    }
});
