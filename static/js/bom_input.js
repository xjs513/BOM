function render_gird(json_data) {
    $('#table_div').datagrid({
        data:json_data.data,
        checkOnSelect: false,
        singleSelect:true,
        columns:[[
            {field:'bom_id',title:'ID',width:40},
            {field:'bom_name',title:'组件名称',width:100},
            {field:'bom_code',title:'组件编码',width:100},
            {field:'bom_rate',title:'组件层次',width:60},
            {field:'bom_unit',title:'组件单位',width:60},
            {field:'bom_unit_price',title:'组件单价',width:60},
            {field:'is_produce',title:'组件来源',width:60,
                formatter: function(value,row,index){
                    if(value===1){
                        return '<span style="color:green;">自制</span>';
                    }else{
                        return '<span style="color:red;">外购</span>';
                    }
                }}
        ]], // end of columns:[[
        toolbar: '#toolbar_div',
        onSelect: function (index,row) {
            var msg = "当前组件[" + change_color(row.bom_name, 'red') + "],编码["
                 + change_color(row.bom_code, 'blue') + "]--";
            if(row.is_produce == 0){
                $('#p').panel({title: msg + "为外购物资"});
                $("#p").hide();
            }else{
                $('#p').panel({title: msg + "组件组成如下:"});
                $("#p").show();
            }
            $("#bom_code_g").val(row.bom_code);
            rel_refresh_page(default_page_number, default_page_size);
        }
    }); // end of $('#dg_my_job_id').datagrid({
}; // end of function render_gird(json_data) {
function change_color(str, color){
    return '<font color="' + color + '">' + str + '</font>';
}
function del_function(){
    // 获取选中数据行的ID，作为参数传递到后台
    var row = $('#table_div').datagrid("getSelected");
    if(!row){
        $.messager.alert("操作提示", "请选择要删除的数据","error");
        return;
    }
    $.messager.confirm('操作提示','确认删除数据?',function(r){
        if (r){
            $.get(
                urls.delete,
                {"bom_id":row.bom_id},
                function(res, status) {
                    $.messager.show({
                        title:'操作提示',
                        msg:res.msg,
                        timeout:2000,
                        showType:'slide'
                    });
                    if(res.status===0){
                        return;
                    }else{
                        refresh_page($('#pager_div').pagination("options").pageNumber, $('#pager_div').pagination("options").pageSize);
                    }
                } // end of  function(res, status) {
            ) // end of $.get(
        }// end of if (r){
    });// $.messager.confirm('操作提示','确认删除数据?',function(r){
};
function add_function(){
    $('#operate_div').dialog({
        title: '<center>添加[组件-原料]</center>',
        width: 380,
        height: 340,
        left:100,
        top:100,
        closed: false,
        cache: false,
        href: urls.pre_add,
        modal: true,
        buttons:[{
            text:'确定',
            handler:function(){
                $('#add_form').form('submit', {
                    url:urls.add,
                    onSubmit: function(){
                        return $(this).form('validate');
                    },
                    success:function(res){
                        res = JSON.parse(res);
                        $.messager.show({
                            title:'操作提示',
                            msg:res.msg,
                            timeout:2000,
                            showType:'slide'
                        });
                        if(res.status===0){
                            return;
                        }else{
                            refresh_page($('#pager_div').pagination("options").pageNumber, $('#pager_div').pagination("options").pageSize);
                        }
                    }
                });// end of $('#ff').form('submit', {
            } // end of handler:function(){
        },{
            text:'重置',
            handler:function(){
               $('#add_form').form('reset');
            }
        },{
            text:'关闭',
            handler:function(){
                $("#operate_div").dialog('close');
            }
        }]
    });// end of $('#add_div').dialog({
};
function update_function(){
    var row = $('#table_div').datagrid("getSelected");
    if(!row){
        $.messager.alert("操作提示", "请选择要更新的数据","error");
        return;
    }
    $('#operate_div').dialog({
        title: '编辑[组件-原料]',
        width: 380,
        height: 340,
        left:100,
        top:100,
        closed: false,
        cache: false,
        href: urls.pre_update + "?bom_id=" + row.bom_id,
        modal: true,
        buttons:[{
            text:'确定',
            handler:function(){
                $('#update_form').form('submit', {
                    url:urls.update,
                    onSubmit: function(){
                        return $(this).form('validate');
                    },
                    success:function(res){
                        res = JSON.parse(res);
                        $.messager.show({
                            title:'操作提示',
                            msg:res.msg,
                            timeout:2000,
                            showType:'slide'
                        });
                        if(res.status===0){
                            return;
                        }else{
                            refresh_page($('#pager_div').pagination("options").pageNumber, $('#pager_div').pagination("options").pageSize);
                        }
                    }
                });// end of $('#update_form').form('submit', {
            } // end of handler:function(){
        },{
            text:'重置',
            handler:function(){
               $('#update_form').form('reset');
            }
        },{
            text:'关闭',
            handler:function(){
                $("#operate_div").dialog('close');
            }
        }]
    });// end of $('#add_div').dialog({
};
function render_pager(total, pageSize) {
    $('#pager_div').pagination({
        total:total,
        pageList: [default_page_size],
        displayMsg:"显示 {from} - {to} 条信息/总计 {total}条信息。",
        pageSize:pageSize,
        onSelectPage:function(pageNumber, pageSize){
            refresh_page(pageNumber, pageSize);
        }
    }); // end of $('#pp_my_job_id').pagination({
}; // end of function render_pager(total, pageSize) {
function refresh_page(pageNumber, pageSize){
    var bom_name = $('#bom_name').val();
    var bom_code = $('#bom_code').val();
    //注意它的类型是Array
    var dic = {};
    dic["bom_name"] = bom_name;
    dic["bom_code"] = bom_code;
    dic["pageNumber"] = pageNumber;
    dic["pageSize"] = pageSize;
    $.ajax({ // Ajax调用处理
       type: "POST",
       url: urls.get_page,
       data: dic,
       dataType: "json",
       success: function(json_data){
           render_gird(json_data);
           render_pager(json_data.total, json_data.pageSize)
       } // end of success: function(data){
    }); // end of $.ajax({
}; // end of function get_page_json_data(pageNumber, pageSize, options){