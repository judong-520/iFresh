function add_goods_num(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/cart/add_num/',
        type: 'post',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': goods_id},
        dataType: 'json',
        success: function(data){
            if(data.code==200){
                $('#num_'+ goods_id).html(data.c_num);
                total_prices()
            }else{
                $('#msg_warm_' + goods_id).html(data.msg);
                $('#msg_warm_' + goods_id).show();
            }
        },
        error: function () {
            alert('请求失败')
        }
        });
}

function sub_goods_num(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/cart/sub_num/',
        type: 'post',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': goods_id},
        dataType: 'json',
        success: function (data) {
            if(data.code==200){
                $('#num_' + goods_id).html(data.c_num);
                total_prices()
            }else{
                $('#msg_warm_' + goods_id).html(data.msg);
                $('#msg_warm_' + goods_id).show();
            }
        },
        error: function () {
            alert('请求失败')
        }
    });
}

function change_status(cart_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/cart/change_status/',
        type: 'post',
        headers: {'X-CSRFToken': csrf},
        data: {'cart_id': cart_id},
        dataType: 'json',
        success: function (data) {
            if(data.is_select){
                $('#choose_' + cart_id).html('<span>√</span>');
            }else{
                $('#choose_' + cart_id).html('<span></span>');

            }total_prices()
        },
        error: function () {
            alert('请求失败')
        }
    });
}

function all_select() {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var sign = $('#select_all').html();
    $.ajax({
        url:'/cart/select_all/',
        type: 'post',
        headers: {'X-CSRFToken': csrf},
        data:{'sign': sign},
        dataType: 'json',
        success: function (data) {
            if(data.code==200){
                if(data.sign){
                    $('#is_all').html('<span id="select_all">√</span>');
                    for(var i=0; i < data.ids.length; i += 1){ $('#choose_' + data.ids[i]).html('<span>√</span>')}
                }else{
                    $('#is_all').html('<span id="select_all"></span>');
                    for(var j=0; j < data.ids.length; j += 1){ $('#choose_' + data.ids[j]).html('<span></span>')}

                }total_prices()
            }else{
                alert('参数错误');
            }
        },
        error: function () {
            alert('请求失败')
        }
    })
}


function total_prices(){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/cart/total_price/',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            $('#total_price').html(
                '总价:' + '￥' + data.total
            )
        },
        error: function (msg) {
            alert('总价计算错误')
        }
        });
}

