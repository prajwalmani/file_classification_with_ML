if (window.File && window.FileReader && window.FileList && window.Blob) {
    function showFile() {
       var preview = document.getElementById('show-text');
       var file = document.querySelector('input[type=file]').files[0];
       var reader = new FileReader()

       var textFile = /text.*/;

       if (file.mimetype.match(textFile )) {
          reader.onload = function (event) {
             preview.innerHTML = event.target.result;
          }
       } else {
          preview.innerHTML = "<span class='error'>Not a Text File</span>";
       }
       reader.readAsText(file);
    }
 } else {
    alert("ERROR : Cuz no file option avialble");
 }