function CustomUploadAdapterPlugin (editor) {
    editor.plugins.get('FileRepository').createUploadAdapter = (loader) => {
        return new UploadAdapterCustom(loader);
    };
}

class UploadAdapterCustom {
    constructor(loader) {
        this.loader = loader;
    }

    upload() {
        return this.loader.file.then(file => new Promise((resolve, reject) => {
            const data = new FormData();
            data.append('upload', file);

            fetch('/api/upload-image-ckeditor', {
                method: 'POST',
                body: data
            })

            .then(response => response.json())
            .then(result => {
                if (result.url) {
                    resolve({default: result.url});
                }
                else {
                    reject(result.error || 'Erro ao fazer Upload.');
                }
            })

            .catch(err => reject(err));
        }));
    }

    abort() {
        // Opcional, explorar mais depois.
    }
}


// Aqui vamos criar o editor de texto com a identificacao de "conteudo"
ClassicEditor.create(document.querySelector('#conteudo'), {
    extraPlugins: [ CustomUploadAdapterPlugin ],
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