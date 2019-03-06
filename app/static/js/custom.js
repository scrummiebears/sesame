$(document).ready(function(){
    $('.sidenav').sidenav();
    
    M.AutoInit();

    var today = new Date();
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
      });

      var chip = {
        tag: 'chip content',
        image: '', //optional
    };

    $(".chips-custom").chips(
        {onChipDelete : formUpdate
        , onChipAdd: formUpdate,
        autocompleteOptions: {
          data: autoComplete_data
      }, placeholder: "Reveiwers",
    secondaryPlaceholder: " "}
      );

    
})
