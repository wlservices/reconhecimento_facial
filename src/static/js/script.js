function closeModal() {
    modal.style.display = 'none';
    photoInput.value = ""; 
};

function showTab(index) {
    const panels = document.querySelectorAll('.tab-panel');
    const buttons = document.querySelectorAll('.tab-btn');

        panels.forEach((panel, i) => {
            panel.classList.toggle('active', i === index);
            buttons[i].classList.toggle('active', i === index);
        });
};

function toggleDetails(id) {
    const elemento = document.getElementById(id);
    elemento.classList.toggle('expandido');
}

function confirmarExclusao(id) {
    if (confirm("Tem certeza que deseja excluir este usuário?")) {
        window.location.href = "/excluir-usuario/" + id;
    }
}

function atualizarRelogio() {
    const agora = new Date();
    const formato = agora.toLocaleDateString('pt-BR') + ' ' + agora.toLocaleTimeString('pt-BR');
    
    // Supondo que você crie um elemento com id="relogio" no seu _header.html
    const elementoRelogio = document.getElementById('relogio');
    if (elementoRelogio) {
        elementoRelogio.innerText = formato;
    }
}

// Atualiza a cada 1 segundo
setInterval(atualizarRelogio, 1000);

function obterLocalizacao() {
    const displayLocal = document.getElementById('local-texto');

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            // Usando a API gratuita do Nominatim (OpenStreetMap)
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
                .then(response => response.json())
                .then(data => {
                    const cidade = data.address.city || data.address.town || data.address.village;
                    const estado = data.address.state;
                    
                    if (displayLocal) {
                        // Exibe "Rio de Janeiro, Rio de Janeiro" ou similar
                        displayLocal.innerText = `${cidade}`;
                    }
                })
                .catch(error => {
                    if (displayLocal) displayLocal.innerText = `Lat: ${lat.toFixed(2)}, Lon: ${lon.toFixed(2)}`;
                    console.error("Erro na geocodificação:", error);
                });

        }, function(error) {
            if (displayLocal) displayLocal.innerText = "Localização indisponível";
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {

    obterLocalizacao()

    let cropper;
    const photoInput = document.getElementById('photo-input');
    const imageToCrop = document.getElementById('image-to-crop');
    const modal = document.getElementById('cropper-modal');
    const croppedInput = document.getElementById('cropped_image');
    const imageContainer = document.getElementById('image-container');

    // Ao selecionar um arquivo
    photoInput.addEventListener('change', function(e) {
        const files = e.target.files;
        if (files && files.length > 0) {
            const reader = new FileReader();
            reader.onload = function(event) {
                imageToCrop.src = event.target.result;
                modal.style.display = 'block';
                
                if (cropper) cropper.destroy();
                
                cropper = new Cropper(imageToCrop, {
                    aspectRatio: 1, // Quadrado para o círculo
                    viewMode: 1,
                    dragMode: 'move',
                    background: false
                });
            };
            reader.readAsDataURL(files[0]);
        }
    });

    // Ao confirmar o recorte no Modal
    document.getElementById('btn-confirm-crop').addEventListener('click', function() {
        const canvas = cropper.getCroppedCanvas({
            width: 400,
            height: 400
        });

        const dataURL = canvas.toDataURL('image/jpeg');
        
        // Atualiza a imagem de preview na tela principal
        imageContainer.innerHTML = `<img src="${dataURL}" class="preview-photo" id="image-preview">`;
        
        // Coloca o Base64 no input hidden para enviar ao Flask
        croppedInput.value = dataURL;
        
        closeModal();
    });
})