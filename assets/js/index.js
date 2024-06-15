$(document).ready(function () {

    let progress_bar = null

    $("#images_folder_modal").submit(function (e) {

        e.preventDefault();
        var images_folder = $('#images_folder').val();

        $('#images_folder_modal_submit').css('display', 'none')

        if (!progress_bar)
            progress_bar = new ProgressBar('#images_folder_modal')

        progress_bar.setProgress(0)
        progress_bar.setText("Preparing(" + 0 + "%)")

        $.post('/images_folder', { images_folder: images_folder })
            .done(function (data) {
                if (data.status == "success") {
                    localStorage.setItem('images_folder', images_folder);
                    checkFolderProgress();
                } else {
                    console.error("Unexpected response:", data);
                    alert("Failed to process the request. Please try again.");
                }
            })
            .fail(function (jqXHR, textStatus, errorThrown) {
                $('#images_folder_modal_submit').css('display', 'block')
                alert("Error: Unable to process the request. Please try again.");
            })

    })

    function checkFolderProgress() {
        if (!progress_bar)
            progress_bar = new ProgressBar('#images_folder_modal')
        var interval = setInterval(function () {
            $.get('/images_folder', function (data) {
                if (data.progress == 100) {
                    clearInterval(interval)
                    findDuplicates()
                }
                progress_bar.setProgress(data.progress)
                progress_bar.setText("Preparing(" + data.progress + "%)")
            })
        }, 200)
    }

    function findDuplicates() {
        let images_folder = localStorage.getItem('images_folder')
        $.post('/find_duplicates', { images_folder: images_folder }, function (data) {
            if (data.status == "success") {
                checkFindDuplicatesProgress()
            }
        })
    }

    function checkFindDuplicatesProgress() {
        if (!progress_bar)
            progress_bar = new ProgressBar('#images_folder_modal')
        var interval = setInterval(function () {
            $.get('/find_duplicates', function (data) {
                if (data.progress == 100) {
                    clearInterval(interval)
                    let images_folder = localStorage.getItem('images_folder')
                    window.location.href = "/result?images_folder=" + images_folder
                }
                progress_bar.setProgress(data.progress)
                progress_bar.setText("Finding duplicates(" + data.progress + "%)")
            })
        }, 1000)
    }


});

function setProgress(text, value) {
    $('#progress').css('width', value + "%");
    $('#progress-text').text(text);
}

function setdProgress(text, value) {
    $('#dprogress').css('width', value + "%");
    $('#dprogress-text').text(text);
}

function checkProgress() {
    $('#tskButton').prop('disabled', true)
    setProgress("Preparing files...", 1)
    var interval = setInterval(function () {
        $.get('/progress', function (data) {
            if (data.progress !== undefined) {
                if (data.progress == 100) {
                    clearInterval(interval);
                    $('#tskButton').prop('disabled', false)
                    setProgress("Preparation done.", data.progress)
                    $('#dupForm').css('display', 'flex')
                }
            } else {
                setProgress("Error Occured", 0)
                $('#tskButton').prop('disabled', false)
                clearInterval(interval);
            }
        });
    }, 1000);
}

function checkDupProgress() {
    $('#dupButton').prop('disabled', true)
    setdProgress("Finding duplicates...", 1)
    var interval = setInterval(function () {
        $.get('/dupprogress', function (data) {
            if (data.progress !== undefined) {
                setdProgress("Finding duplicates...", data.progress)
                if (data.progress == 100) {
                    clearInterval(interval);
                    $('#dupButton').prop('disabled', false)
                    setdProgress("Finding duplicates done.", data.progress)
                    $('#resForm').css('display', 'flex')
                }
            } else {
                setdProgress("Error Occured", 0)
                $('#dupButton').prop('disabled', false)
                clearInterval(interval);
            }
        });
    }, 1000);
}

function handlePaste(event) {
    var clipboardData, pastedText;
    clipboardData = event.clipboardData || window.clipboardData;
    pastedText = clipboardData.getData('Text');
    pastedText = pastedText.replace(/["']/g, '');
    localStorage.setItem('source_dir', pastedText)
    setTimeout(() => {
        $('#folderPath').val(pastedText);
    }, 100);
}