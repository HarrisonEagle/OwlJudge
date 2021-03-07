$(document).ready(function() {
    $('#submit_form').submit(function() {
        $('#res').text('Processing...');
        $('#res').css('color','black');
        $.ajax({
            'url':$('form#submit_form').attr('action'),
            'type':'POST',
            'data':$('form#submit_form').serialize(),
            'dataType':'json',
            'success':function(response){
                if(response.result.includes('error')||response.result.includes('Error')||response.result.includes('Time Limit Exceed!')){
                    $('#res').css('color','red');
                }else{
                    $('#res').css('color','green');
                }
                $('#res').html(response.result.replace(/\r?\n/g, '<br>'));
                $('#time').text("Time:"+response.timeusage+"ms");
                $('#memory').text("MemoryUsage:"+response.memoryusage+"KB");
            },
        });
        return false;
    });
});
