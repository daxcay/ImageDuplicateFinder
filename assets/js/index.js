$(document).ready(function () {

    let progress_bar = null

    $('#images_folder').on('change', function() {
        var value = $('#images_folder').val();
        if (value.includes('"')) {
            value = value.replace(/"/g, '');
            $('#images_folder').val(value).focus();
        }
    });

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
                progress_bar.setText("Finding duplicates(" + data.text + ")")
            })
        }, 1000)
    }


});