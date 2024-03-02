// サブカテゴリ表示
function setSubcategoryArray(category_name, version_array){
    let elm = document.getElementById('subcategory_element');
    let subcategoryElm = document.getElementById('subcategory');

    // 表示する前に一旦非表示にする
    elm.style.display = 'none';

    // subcategory_testプルダウンの内容をクリア
    elm.options.length = 0;

    // カテゴリに対応するサブカテゴリを追加
    for (let i = 0; i < version_array[category_name].length; i++) {
        let op = document.createElement('option');
        op.value = version_array[category_name][i];
        op.textContent = version_array[category_name][i];
        elm.appendChild(op);
    }

    // カテゴリが選択されている場合はsubcategory_testを表示し、subcategoryを非表示にする
    if (category_name) {
        elm.style.display = 'block';
        subcategoryElm.style.display = 'none';
    } else {
        // カテゴリが選択されていない場合はsubcategory_testを非表示にし、subcategoryを表示する
        elm.style.display = 'none';
        subcategoryElm.style.display = 'block';
    }
}
// カテゴリのサブカテゴリが選択されているか確認
function checkFormValidity() {
    var categoryValue = document.getElementById('category_element').value;
    var subcategoryValue = document.getElementById('subcategory_element').value;

    var submitButton = document.getElementById('submitButton');
    var form = document.getElementById('postForm');

    if (categoryValue && subcategoryValue) {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}


// 画像表示
function showImagePreview(input) {
    var file = input.files[0];
    var previewImage = document.getElementById('previewImage');
    var imagePreview = document.getElementById('imagePreview');

    if (file) {
        var reader = new FileReader();

        reader.onload = function (e) {
            previewImage.src = e.target.result;
            imagePreview.style.display = 'block';
        };

        reader.readAsDataURL(file);
    } else {
        previewImage.src = '#';
        imagePreview.style.display = 'none';
    }
}
