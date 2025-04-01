const path = window.location.pathname.split('/-');
const section = path[path.length -1];

if (section){
    const alvo = document.getElementById(section);
    if (alvo){
        window.scrollTo({
            top: alvo.offsetTop,
            behavior: 'smooth',
        });
    }
}