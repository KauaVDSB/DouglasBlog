const parametro = window.location.pathname.split('%23');
const section = parametro[parametro.length -1];

if (section){
    const alvo = document.getElementById(section);
    if (alvo){
        window.scrollTo({
            top: alvo.offsetTop,
            behavior: 'smooth',
        });
    }
}