

function getURLParameter(sUrl, sParam) {
        let sPageURL = sUrl.substring(sUrl.indexOf('?') + 1);
        let sURLVariables = sPageURL.split('&');
        for (let i = 0; i < sURLVariables.length; i++) {
            let sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == sParam) {
                return sParameterName[1];
            }
        }
}



$(document).ready(function(){

$(document).on('click', '[data-action="paginate"]', function(){
        var href = $(this).data('href')
        var page = getURLParameter(href, 'page')
        load_product(page)


})

       function load_product(page) {
                var querystring = getFormData($('#filter-form'))
                querystring['page'] = page
                console.log(querystring)
                $.ajax({
                        url: '/api/products/',
                        method: 'GET',
                        data: querystring,
                        success: function(json) {
                                $('#list-products').html(json['html'])
                                var path = window.location.pathname + '?page=' + page
                                window.history.pushState({route: path}, "", path)
                        },
                        error: function(data) {
                            console.log('Invalid')
                        },
                 })
             }

var start = getURLParameter(window.location.href, 'page')


if (start){
    load_product(start)
 }


$('#filter-form-submit').on('click', function() {
    load_product('1')

})


function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });
    console.log($('#category').val(),$('#name').val() , $('#brand').val())
    indexed_array['category'] = $('#category').val()
    indexed_array['name'] = $('#name').val()
    indexed_array['brand'] = $('#brand').val()

    return indexed_array;
}



$('#name').keyup(function(e){
    if(e.keyCode == 13) {
       load_product('1')
    }
});

$('#category').change(function(e){
        load_product('1')
});


$('#brand').change(function(e){
       load_product('1')

})


})