// Aqui vamos criar o editor de texto com a identificacao de "conteudo"
ClassicEditor.create(document.querySelector('#conteudo'), {
    // ckfinder: {
        // Neste arquivo vamos configurar o PHP que vai fazer o envio da imagem para a pasta "imagens/"
        // uploadUrl: 'upload_imagem.php'
    // },
    mediaEmbed: {
        // Faz com que videos e outras midias aparecam como previa dentro do editor
        previewsInData: true
    }
}).catch(error => {
    // .catch e usado pra capturar qualquer erro que aconteca no codigo
    // "error =>" e a funcao que sera chamada se esse erro acontecer...
    // => significa "RECEBE", ou seja, a funcao vai receber o erro
    console.error(error); // Exibe o erro no console do navegador, se ocorrer algum problema
}); 