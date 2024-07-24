$(document).ready(function () {

    let progress_bar = null;
    let instance_id = Date.now()

    $('#images_folder_modal_stop').css('display', 'none')
    $('#images_folder_modal_stop').on('click', stopAndReload)

    $('#images_folder').on('change', function () {
        var value = $('#images_folder').val();
        if (value.includes('"')) {
            value = value.replace(/"/g, '');
            $('#images_folder').val(value).focus();
        }
    });

    $('#esimilarity_threshold').on('input', function () {
        $('#esimilarity_value').text($(this).val());
    });

    $('#csimilarity_threshold').on('input', function () {
        $('#csimilarity_value').text($(this).val());
    });

    $("#images_folder_modal").submit(function (e) {

        e.preventDefault();
        var images_folder = $('#images_folder').val();
        $('#images_folder_modal_submit').css('display', 'none');

        if (!progress_bar)
            progress_bar = new ProgressBar('#images_folder_modal');

        progress_bar.setProgress(0);
        progress_bar.setText("Preparing(" + 0 + "%)");

        $.post(`/images_folder?instance_id=${instance_id}`, { images_folder: images_folder })
            .done(function (data) {
                if (data.status == "success") {
                    checkFolderProgress();
                } else {
                    console.error("Unexpected response:", data);
                    alert("Failed to process the request. Please try again.");
                }
            })
            .fail(function (jqXHR, textStatus, errorThrown) {
                $('#images_folder_modal_submit').css('display', 'block');
                alert("Error: Unable to process the request. Please try again.");
            });

    });

    function checkFolderProgress() {
        if (!progress_bar)
            progress_bar = new ProgressBar('#images_folder_modal');
        var interval = setInterval(function () {
            $.get(`/images_folder?instance_id=${instance_id}`, function (data) {
                if (data.progress == 100) {
                    clearInterval(interval);
                    findDuplicates();
                }
                progress_bar.setProgress(data.progress);
                progress_bar.setText("Preparing(" + data.progress + "%)");
            });
        }, 200);
    }

    function findDuplicates() {

        var images_folder = $('#images_folder').val();
        var esimilarity_threshold = $('#esimilarity_threshold').val();
        var csimilarity_threshold = $('#csimilarity_threshold').val();

        $('#images_folder_modal_stop').css('display', 'initial')

        $.post(`/find_duplicates?instance_id=${instance_id}`, {
            images_folder: images_folder,
            esimilarity_threshold: esimilarity_threshold,
            csimilarity_threshold: csimilarity_threshold
        }, function (data) {
            if (data.status == "success") {
                checkFindDuplicatesProgress();
            }
        });
    }

    function stopAndReload() {
        $.post(`/stop_duplicates?instance_id=${instance_id}`, {}, function (data) {
            if (data.status == "success") {
                window.location.reload()
            }
        });
    }

    function checkFindDuplicatesProgress() {
        if (!progress_bar)
            progress_bar = new ProgressBar('#images_folder_modal');
        var interval = setInterval(function () {
            $.get(`/find_duplicates?instance_id=${instance_id}`, function (data) {
                if (data.progress == 100) {
                    clearInterval(interval);
                    window.location.href = `/result?instance_id=${instance_id}`;
                }
                progress_bar.setProgress(data.progress);
                progress_bar.setText("Finding duplicates(" + data.text + ")");
            });
        }, 1000);
    }

});
