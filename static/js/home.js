$(function(){
    // 初始化 accordion
    $("#RightAccordion").accordion({
        fillSpace:true,
        fit:true,
        border:false,
        animate:false
    });
    // 初始化 tabs
    $('#main_div').tabs({
        border:false,
        onSelect:function(title){

        }
    });
    // 异步请求后台数据
    $.ajax({
        type: "POST",
        url: urls.menu_get_tree,
        data: {},
        dataType: "json",
        success: function(data){
            $(data).each(function(i, e){
                $('#RightAccordion').accordion('add', {
                    title: e.text,
                    content: "<ul id='tree" + e.id + "'></ul>",
                    selected: true,
                    iconCls: e.icon_path
                });
                $("#tree" + e.id).tree({
                    data: e.children,
                    onClick : function(node){
                        if(node.url === "#"){
                            return;
                        }
                        var tabTitle = node.text;
                        var url =  node.url;
                        var icon = node.iconCls;
                        addTab(tabTitle, url, icon);
                   }
                });// end of $("#tree" + e.id).tree({
            });// end of $(data).each(function(i, e){
            // 展开第一个 Accordion
            $("#RightAccordion").accordion("select", 0);
            // 点击第一个有内容的子节点
            var  first_node = $($(".tree")[0]).tree('getRoot');
            addTab(first_node.text, first_node.url, first_node.iconCls);
        }// end of success: function(data){
    });// end of $.ajax({


    /**
     * 在iFrame中打开一个新tab
     * @param title
     * @param href
     */
    function addTab(title,href, icon){
        var iframe_height = $("#main_div").outerHeight() - $("#main_div").children("div.tabs-header").outerHeight() - 3 ;
        var e = $('#main_div').tabs('exists',title);
        if(e){
            $("#main_div").tabs('select',title);
            var tab = $("#main_div").tabs('getSelected');
            $('#main_div').tabs('update',{
                tab:tab,
                options:{
                    title:title,
                    content:"<iframe src='" + href + "' style='width:100%;height:" + iframe_height + "px;overflow-x:hidden; overflow-y:hidden;border: 0px;'></iframe>",
                    closable:true,
                    selected:true
                }
            });
        }else{
            $('#main_div').tabs('add',{
                title:title,
                content:"<iframe src='" + href + "' style='width:100%;height:" + iframe_height + "px;overflow-x:hidden; overflow-y:hidden;border: 0px;'></iframe>",
                iconCls:'',
                closable:true
            });
        }
    }
    // 注销函数
    $(".loginOut").click(function () {
         // 异步请求后台数据
        $.ajax({
            type: "POST",
            url: urls.user_logout,
            data: {},
            dataType: "json",
            success: function(data){
                window.location.href = '/';

            }// end of success: function(data){
        });// end of $.ajax({
    });
    // 修改密码
    $(".changepwd").click(function () {
        $('#operate_div').dialog({
            title: '修改密码',
            width: 380,
            height: 250,
            closed: false,
            cache: false,
            href: urls.pre_change_password,
            modal: true,
            buttons:[{
                text:'确定',
                handler:function(){
                    var user_id = $("#user_id").val();
                    var old_password = $("#old_password").val();
                    var new_password = $("#new_password").val();
                    var new_password_repeat = $("#new_password_repeat").val();
                    if(old_password.trim() === ""){
                        $.messager.alert("操作提示", "原来密码为空!","error");
                        return;
                    }
                    if(new_password.trim() === ""){
                        $.messager.alert("操作提示", "新设密码为空!","error");
                        return;
                    }
                    if(new_password.length < 6){
                        $.messager.alert("操作提示", "新设密码最少六位!","error");
                        return;
                    }
                    if(new_password != new_password_repeat){
                        $.messager.alert("操作提示", "两次新设密码不一致!","error");
                        return;
                    }
                    $.messager.confirm('操作提示',"确认修改密码?",function(r){
                        if (r){
                            // 异步请求后台数据
                            $.ajax({
                                type: "POST",
                                url: urls.change_password,
                                data: {"user_id": user_id, "old_password":old_password, "new_password":new_password},
                                dataType: "json",
                                success: function(res){
                                    $.messager.show({
                                        title:'操作提示',
                                        msg:res.msg,
                                        timeout:2000,
                                        showType:'slide'
                                    });
                                }// end of success: function(data){
                            });// end of $.ajax({
                        }// end of if (r){
                    });// $.messager.confirm('操作提示',message,function(r){
                } // end of handler:function(){
            },{
                text:'关闭',
                handler:function(){
                    $("#operate_div").dialog('close');
                }
            }]
        });// end of $('#operate_div').dialog({
    });
});// end of $(function(){