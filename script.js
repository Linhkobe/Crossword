document.getElementById('upload-button').addEventListener('click', function() {
    var inputFile = document.getElementById('crossword-image-input');
    if(inputFile.files.length > 0) {
        var file = inputFile.files[0];
        handleFileUpload(file);
    } else {
        alert("Veuillez sélectionner une image.");
    }
});

function handleFileUpload(file) {
    // Ici, vous devez implémenter le code pour envoyer l'image au serveur
    // et recevoir la résolution du puzzle de mots croisés.
    console.log("Image envoyée :", file.name);
    // Simuler une réponse
    setTimeout(() => {
        document.getElementById('crossword-result').textContent = "Résolution simulée du puzzle...";
    }, 1500);
}