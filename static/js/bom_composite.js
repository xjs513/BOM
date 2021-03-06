function composite_render_gird(json_data) {
    $('#composite_table_div').datagrid({
        data:json_data.data,
        checkOnSelect: false,
        singleSelect:true,
        columns:[[
            {field:'id',title:'ID',width:40},
            {field:'factory_code',title:'工厂',width:40},
            {field:'bom_code',title:'物料编码',width:100},
            {field:'bom_name',title:'物料名称',width:200},
            {field:'com_code',title:'组件',width:100},
            {field:'com_name',title:'对象描述',width:100},
            {field:'com_rate',title:'层次',width:40},
            {field:'com_cnt',title:'组件数量',width:60},
            {field:'com_unit',title:'组件单位',width:60},
            {field:'com_unit_price',title:'组件单价',width:60}
        ]], // end of columns:[[
        toolbar: '#composite_toolbar_div'
    }); // end of $('#composite_table_div').datagrid({
}; // end of function composite_render_gird(json_data) {
function composite_del_function(){
    // 获取选中数据行的ID，作为参数传递到后台
    var row = $('#composite_table_div').datagrid("getSelected");
    if(!row){
        $.messager.alert("操作提示", "请选择要删除的数据","error");
        return;
    }
    $.messager.confirm('操作提示','确认删除数据?',function(r){
        if (r){
            $.get(
                urls.composite_delete,
                {"composite_id":row.id},
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
                        composite_refresh_page($('#composite_pager_div').pagination("options").pageNumber, $('#composite_pager_div').pagination("options").pageSize);
                    }
                } // end of  function(res, status) {
            ) // end of $.get(
        }// end of if (r){
    });// $.messager.confirm('操作提示','确认删除数据?',function(r){
};
function composite_add_function(){
    var bom_code = $("#bom_code_g").val();
    $('#composite_operate_div').dialog({
        title: '<center>为物料添加组件</center>',
        width: 400,
        height: 500,
        left:100,
        top:100,
        closed: false,
        cache: false,
        href: urls.composite_pre_add,
        queryParams:{"bom_code":bom_code},
        modal: true,
        buttons:[{
            text:'确定',
            handler:function(){
                $('#composite_add_form').form('submit', {
                    url:urls.composite_add,
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
                            composite_refresh_page($('#composite_pager_div').pagination("options").pageNumber, $('#composite_pager_div').pagination("options").pageSize);
                        }
                    }
                });// end of $('#ff').form('submit', {
            } // end of handler:function(){
        },{
            text:'重置',
            handler:function(){
               $('#composite_add_form').form('reset');
            }
        },{
            text:'关闭',
            handler:function(){
                $("#composite_operate_div").dialog('close');
            }
        }]
    });// end of $('#add_div').dialog({
};
function composite_update_function(){
    var row = $('#composite_table_div').datagrid("getSelected");
    if(!row){
        $.messager.alert("操作提示", "请选择要更新的数据","error");
        return;
    }
    $('#composite_operate_div').dialog({
        title: '编辑物料组成',
        width: 400,
        height: 500,
        left:100,
        top:100,
        closed: false,
        cache: false,
        href: urls.composite_pre_update + "?composite_id=" + row.id,
        modal: true,
        buttons:[{
            text:'确定',
            handler:function(){
                $('#composite_update_form').form('submit', {
                    url:urls.composite_update,
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
                            composite_refresh_page($('#composite_pager_div').pagination("options").pageNumber, $('#composite_pager_div').pagination("options").pageSize);
                        }
                    }
                });// end of $('#update_form').form('submit', {
            } // end of handler:function(){
        },{
            text:'重置',
            handler:function(){
               $('#composite_update_form').form('reset');
            }
        },{
            text:'关闭',
            handler:function(){
                $("#composite_operate_div").dialog('close');
            }
        }]
    });// end of $('#add_div').dialog({
};
function composite_render_pager(total, pageSize) {
    $('#composite_pager_div').pagination({
        total:total,
        pageList: [default_page_size],
        displayMsg:"显示 {from} - {to} 条信息/总计 {total}条信息。",
        pageSize:pageSize,
        onSelectPage:function(pageNumber, pageSize){
            composite_refresh_page(pageNumber, pageSize);
        }
    }); // end of $('#pp_my_job_id').pagination({
}; // end of function render_pager(total, pageSize) {
function composite_refresh_page(pageNumber, pageSize){
    var com_name = $('#com_name').val();
    var com_code = $("#com_code").val();
    var bom_code = $("#bom_code_g").val();
    //注意它的类型是Array
    var dic = {};
    dic["bom_code"] = bom_code;
    dic["com_name"] = com_name;
    dic["com_code"] = com_code;
    dic["pageNumber"] = pageNumber;
    dic["pageSize"] = pageSize;
    $.ajax({ // Ajax调用处理
       type: "POST",
       url: urls.composite_get_page,
       data: dic,
       dataType: "json",
       success: function(json_data){
           composite_render_gird(json_data);
           composite_render_pager(json_data.total, json_data.pageSize)
       } // end of success: function(data){
    }); // end of $.ajax({
}; // end of function get_page_json_data(pageNumber, pageSize, options){