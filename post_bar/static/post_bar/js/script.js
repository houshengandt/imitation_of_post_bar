/**
 * Created by czy on 17-4-14.
 */

// 样式

function getHeight() {
	if ($(".user-info").height()>=$(".post-content").height()){
		$(".post-content").height($(".user-info").height());
		console.log($(".user-info").height())
	}
	else{
		$(".user-info").height($(".post-content").height());
		console.log($(".user-info").height())
	}
}


$(document).ready(function () {
   getHeight();
});