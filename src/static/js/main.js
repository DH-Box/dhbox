$( document ).ready(function() {

    $('#appTabs').on('click', function(e) {  
        paneID = $(e.target).attr('href');
        src = $(paneID).attr('data-src');
        windowHeight = $(window).height() - 100; 
        $(paneID+" iframe").attr("height",windowHeight);
        // if the iframe hasn't already been loaded once
        if($(paneID+" iframe").attr("src")=="")
        {
            $(paneID+" iframe").attr("src",src);
    }
    });

    $( "#start-demo" ).click(function(e) {
        showModal('Building your Demo DHbox');
     });

    $( window ).resize(function() {
        $('.app-iframe').each(function() {
            $(this).attr("height",$( window ).height() - 100);
        });
    });

    var errorTemplate = '<div class="help-block"><i class="fa fa-exclamation-circle"></i><i class="fa fa-check"></i></div>';

    $.validator.setDefaults({
        debug: false,
        success: "has-success"
    });
    var form = $( "form" );
    form.validate({
        success: function(label, element) {
            label.text("Looks good!");
        },
        errorPlacement: function (error, element) {
            var errorElement = $(errorTemplate);
            error.appendTo(errorElement);
            errorElement.insertAfter(element);
        }
    });
    $( "#dhbox_form_submit" ).click(function(e) {
        e.preventDefault();
        if (form.valid()){
            var x;
            var r=true
            if (r==true)
              {
                var allUsers = { users: [] };
                $('.userwrapper').each(function () {
                    allUsers.users.push({
                    name: $(this).find('[what=users]').val(),
                    pass: $(this).find('[what=passes]').val(),
                    email: $(this).find('[what=email]').val(),
                    duration: $(this).find('[what=duration]:checked').val()
                    })
                });
                showModal('Building your DHbox');
                allUsers.users = allUsers.users.filter(function(n){ return n != undefined });
                mainUser = allUsers.users[0].name
                allUsers = JSON.stringify(allUsers);
                // console.log(allUsers);
                // console.log(mainUser);
                $.post('/new_dhbox', allUsers, function(data){
                if (data == 'failure'){
                    $('#modal-content').modal('hide');
                    $('#failure-modal').modal({show: true});
                }else
                {
                    setTimeout(function () {
                        alert(data)
                        window.location = '/dhbox/'+mainUser;
                        }, 9000);
                }
                });
              }
            else
              {
              x="!";
              console.log('didnt go through with it');
              }
        }
    });

    function showModal(title) {
        var modal = $('#progress-modal');

        modal.find('.modal-title').text(title);

        modal.modal('show');
    }

    $.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please check your input. No capital letters or spaces."
    );
    $("#admin").rules("add", { regex: "^[a-z][-a-z0-9]*\$" })
    // $("#admin").rules("add", { regex: "^[a-z][-a-z0-9]*\$" })

    // add listener for SSE (progress bars etc)
    var source = new EventSource("{{ url_for('sse.stream') }}");
    alert('heyo!'); 
    console.log('heyo!'); 
    source.addEventListener('greeting', function(event) {
	console.log(event.data) 
        var data = JSON.parse(event.data);
	console.log(data) 
    }, false);

});
