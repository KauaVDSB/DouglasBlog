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
        console.log('não é menu');
    }
    else{
        console.log('é menu');
    }
});