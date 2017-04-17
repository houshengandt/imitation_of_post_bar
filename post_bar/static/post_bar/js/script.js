/**
 * Created by czy on 17-4-14.
 */

// 样式

function getHeight() {
	if ($(".user-info").height()>=$(".post-content").height()){
		$(".post-content").height($(".user-info").height());
	}
	else{
		$(".user-info").height($(".post-content").height());
	}
}

function getNotifications() {
    $.getJSON('/get_notification/', function (result) {
        var q = 0;
        var notifications = '<button id="id_mark_as_read" class="btn btn-primary">全部标记为已读</button>';
        if($.isEmptyObject(result)) {
            $('#id_notification').attr("data-content", "没有未读通知").attr("title", '');
            $('.badge').text('');
        } else {
            $.each(result, function (i, item) {
                notifications += "<li class='list-group-item'>" + item.trigger + " 回复了你：" + item.action_content + "</li>";
                q++;
            });
            $('#id_notification').attr("data-content", notifications);
            $('.badge').text(q);
        }
    })

}

$(document).ready(function () {
	$(function () {
    	$('[data-toggle="popover"]').popover()
	});
    getHeight();
    getNotifications();
    $('body').on('click', '#id_mark_as_read', function () {
        $.get('/mark_all_as_read/');
        getNotifications();
    });
    setInterval(getNotifications, 10000);

});