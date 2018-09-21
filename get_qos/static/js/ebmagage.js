    $(function () {
        $('#tian').click(function () {
            var tipcon =
                '<div class="hang">'+
            '<sapn>'+
               ' &nbsp&nbsp服务类型：<select name="types">'+
                    '<option value="天气" selected>天气</option>'+
                    '<option value="新闻">新闻</option>'+
                    '<option value="菜谱">菜谱</option>'+
                    '<option value="企业查询">企业查询</option>'+
                    '<option value="身份核验">身份核验</option>'+
                    '<option value="交通查询">交通查询</option>'+
                '</select>'+
           ' </sapn>'+
            '<span>'+
                '&nbsp&nbsp网速：<input type="text" name="bandwidth" class="inputwidth">Mb/s'+
            '</span>'+
            '<span>'+
              '&nbsp&nbsp任务量：<input type="text" name="workload"  class="inputwidth">Kb'+
           ' </span>'+
           ' <span>'+
               '&nbsp&nbsp响应时间：<input type="text" name="qos"  class="inputwidth">ms'+
           ' </span>'+
        '</div>';
            $('.man').append(tipcon);
        });
    });


