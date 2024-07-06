class ProgressBar {
    constructor(parent) {
        this.parent = parent
        this.id = "prg_"+Date.now()
        let bar = `<div class="bar"></div>`
        let text = `<p class="text"></p>`
        let block = `<div class="progress-bar" id="${this.id}">${text}${bar}</div>`
        $(parent).prepend(block)
    }
    setText(text) {
        $("#"+this.id+' .text').text(text)
    }
    setProgress(progress) {
        $("#"+this.id+' .bar').css('width',progress+"%")
    }
}

