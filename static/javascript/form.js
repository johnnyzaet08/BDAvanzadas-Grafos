
window.onload = function() {
    var inputs = document.getElementsByClassName('js-input');

    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('keyup', myfunc)
    };

}

function myfunc() {
    if (this.value) {
        this.classList.add('not-empty');
    } else {
        this.classList.remove('not-empty');
    }
}
