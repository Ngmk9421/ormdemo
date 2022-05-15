const IP_PORT = 'http://100.100.6.186'

let flag1 = false
var csrf = $("input[name='csrfmiddlewaretoken']").val()
var article_id = $("input[name='article_id']").val()
$('.like').click(() => {
    if (flag1) {
        $.post( IP_PORT + '/article/like_article', {
            like: 0,
            'csrfmiddlewaretoken': csrf,
            id: article_id
        }, function (data) {
            $('.like_num').text(data.like_num)
        })
        $('.like').css('backgroundColor', 'rgba(171, 213, 248, .6)')
    } else {
        $.post(IP_PORT + '/article/like_article', {
            like: 1,
            'csrfmiddlewaretoken': csrf,
            id: article_id
        }, function (data) {
            $('.like_num').text(data.like_num)
        })
        $('.like').css('backgroundColor', 'rgba(125, 196, 255)')
    }
    flag1 = !flag1
})


$('.del').click(function () {
    if (confirm('确定要删除吗？')) {
        $.get('http://100.100.6.186/article/del_article', {id: article_id}, function (data) {
            history.go(-1)
        })
    }
})

