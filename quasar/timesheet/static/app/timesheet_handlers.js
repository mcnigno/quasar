
(function($) {
    // lock readonly and change class (no clock) for time fields on page load - in case of validation...
    
    //$('.vTimeField').attr('readonly','readonly');
    //$('.field-from_time').attr('class','simple');
    console.log('span....')
    console.log($('.field-from_time').children().attr('readonly','readonly'));
    console.log($('.field-from_time').children().attr('class','simple'));
    // document.querySelector("#task_set-9 > td.field-from_time > span")
    // on new task document.querySelector("#id_task_set-9-to_time")
    
    $(document).on('formset:added', function(event, $row, formsetName) {
        if (formsetName)  {
            
            // Get Time Now
            
            var today = new Date();
            var time = today.getHours().toString().padStart(2,'0') 
                        + ":" + today.getMinutes().toString().padStart(2,'0')
                        + ":" + today.getSeconds().toString().padStart(2,'0');

            // Update time for the NEW row
            $row.find('.field-from_time').children().val(time);
            $row.find('.field-to_time').children().val(time);
            
            // Set Readonly on every from-time field and remove "now"
            $('.field-from_time').children().attr('readonly','readonly');
            $('.field-from_time').children().children().remove();
            
        }
    });

    $(document).on('formset:removed', function(event, $row, formsetName) {
        // Row removed
    
    });
    
})(django.jQuery);

$("#details").click(function(){
    console.log('detail button pressed');
    $("p").toggle();
  });
