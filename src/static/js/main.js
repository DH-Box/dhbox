$( document ).ready(function() {

    $( "#start-demo" ).click(function(e) {
        showModal('Building your Demo DHbox');
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
            var r=confirm("All settings correct?");
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
                    // $('inside-modal').replaceWith('<div>DH Box successfully created.</div>');
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
});