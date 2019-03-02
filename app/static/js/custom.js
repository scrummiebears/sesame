$(document).ready(function(){
    $('.sidenav').sidenav();
    
    M.AutoInit();

    var today = new Date();
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
      });

    
})
