function render_gird(json_data) {
    $('#table_div').datagrid({
        data:json_data.data,
        checkOnSelect: false,
        singleSelect:true,
        columns:[[
            {field:'bom_id',title:'ID',width:40},
            {field:'factory_code',title:'工厂编码',width:60},
            {field:'bom_code',title:'物料编码',width:120},
            {field:'bom_name',title:'物料名称',width:180},
            {field:'bom_cost',title:'成本合计',width:100}
        ]], // end of columns:[[
        toolbar: '#toolbar_div',
        onSelect: function (index,row) {
            var panel_title = "当前物料[" + change_color(row.bom_name, 'red') + "],物料编码["
                 + change_color(row.bom_code, 'blue') + "],工厂[" + change_color(row.factory_code, 'purple') + "]";
            $('#p').panel({title: panel_title});
            $("#bom_code_g").val(row.bom_code);
            composite_refresh_page(default_page_number, default_page_size);
        }
    }); // end of $('#dg_my_job_id').datagrid({
}; // end of function render_gird(json_data) {
function change_color(str, color){
    return '<font color="' + color + '">' + str + '</font>';
}
function calculate_cost_function(){
    // 获取选中数据行的ID，作为参数传递到后台
    var row = $('#table_div').datagrid("getSelected");
    var params = {};
    var msg = "";
    if(!row){
        msg = "未选定产品将重算所有成本,请确认!"
    }else{
        var panel_title = "当前物料[" + change_color(row.bom_name, 'red') + "],物料编码["
                 + change_color(row.bom_code, 'blue') + "],工厂[" + change_color(row.factory_code, 'purple') + "]";
        msg = "确定重算" + panel_title + "的成本么?"
        params["bom_code"] = row.bom_code
    }
    $.messager.confirm('操作提示', msg ,function(r){
        if (r){
            $.get(
                urls.calculate_cost,
                params,
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
        title: '<center>添加产出物料</center>',
        width: 380,
        height: 300,
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
        title: '编辑产出物料',
        width: 380,
        height: 300,
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