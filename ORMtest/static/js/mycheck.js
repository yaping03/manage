    /**
 * Created by yaping on 2017/10/17 0017.
 */
jQuery.fn.extend({
    "check":function (dic) {
        var it = $(this);
        it.find(".btn-success").on("click",function () {
            var tag=true;
            it.find(".form-group").removeClass("has-error");
            it.find("span").text("");
            console.log("123");
            var confirm = it.find(".password");
            if(confirm.eq(0).val()!==confirm.eq(1).val()){
                    confirm.parent().parent().addClass("has-error");
                    confirm.next().text("两次密码必须一致");
                    tag=false;
                    return false
                }
            it.find(".form-control:required").each(function () {
                var my=$(this);
                if(my.val().trim().length===0){
                    my.parent().parent().addClass("has-error");
                    my.next().text(my.attr("id")+" must be not blank");
                    tag=false;
                    return false
            }
                if(my.val().trim().length < dic["user"]["user_length"]){
                    my.parent().parent().addClass("has-error");
                    my.next().text(my.attr("id")+" must be greater than "+dic["user"]["user_length"]);
                    tag=false;
                    return false
            }
        });
            return tag;
    });

    }
});
