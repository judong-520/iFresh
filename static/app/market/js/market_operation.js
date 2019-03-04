function add_goods_num(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var num = $('#goods_num_' + goods_id).html();
    $.ajax({
        url:'/market/add_num/',
        type: 'post',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': goods_id, 'num': num},
        dataType: 'json',
        success: function(data){
            if(data.code==200){
                $('#goods_num_' + goods_id).html(data.num);
            }
        },
        error: function () {
            alert('请求失败')
        }
        });
}

function sub_goods_num(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var num = $('#goods_num_' + goods_id).html();
    $.ajax({
        url:'/market/sub_num/',
        type: 'post',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': goods_id, 'num': num},
        dataType: 'json',
        success: function (data) {
            if(data.code==200){
                $('#goods_num_' + goods_id).html(data.num);
            }
        },
        error: function () {
            alert('请求失败')
        }
    });
}