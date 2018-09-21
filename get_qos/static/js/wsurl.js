    $(function () {
        $('#tianjia').click(function () {
            var tipcon =
                '<div class="tip">'+
                '<div class="tip-input">'+
                '<input type="text" class="biaoqian" placeholder="标签" name="tag">'+
                '</div>'+
                '<div class="tip-input">' +
                '<input type="url" class="house-tip" placeholder="接口地址" required pattern="http(s)?://([\\w-]+\\.)+[\\w-]+(/[\\w- ./?%&=]*)?" name="address">' +
                '<span class="del"></span>' +
                '</div>'+
            '</div>';
            $('.tip_div').append(tipcon);
            // 删除
            $('.del').click(function () {
                $(this).parent().parent().remove();
            });
        });
    });


