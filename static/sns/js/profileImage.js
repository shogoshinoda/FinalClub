$(document).ready(function(){
    viewportWidth = 420 //クロッピングするサイズ（横幅 ピクセル表記）
    viewportHeight = 560 //クロッピングするサイズ（縦幅 ピクセル表記）
    boundaryWidth = 700 //クロッピング元画像のサイズ（横幅 ピクセル表記）
    boundaryHeight = 700 //クロッピング元画像のサイズ（縦幅 ピクセル表記）

    // croppieの初期設定
    $image_crop = $('#profileImage_croppie').croppie({
        enableExif: true,
        viewport: {
            width: viewportWidth,
            height: viewportHeight,
            type:'square' //円形にクロッピングしたい際はここをcircleとする
        },
        boundary: {
            width: boundaryWidth,
            height: boundaryHeight
        }
    });
});
$(document).ready(function(){
    $('#upload_image').on('change', function(){
        var reader = new FileReader();
        reader.onload = function (event) {
            $image_crop.croppie('bind', {
                url: event.target.result
            }).then(function(){
                // console.log('Bind complete');
            });
        }
        $('#profileImage_croppie').css('display','block');
        reader.readAsDataURL(this.files[0]);
    });
});