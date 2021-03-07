$(document).ready(function() {
    judge(0,$('.caseclass').length);
});

function judge(n,max){
  $.ajax({
                  'type': 'get',
                  'url': '/judgecode',
                  'data': {
                      'initnumber':$("#initnumber").text(),
                      'casenumber': n,
                      'submissionid':$("#submissionid").text(),
                      'problemid':$("#problemid").text(),
                      'language':$("#language").text()
                  },
                  'success': function(data){
                    const obj = JSON.parse(data);
                    $('#casestatus'+(n+1)).text(obj.result);
                    $('#timeusage'+(n+1)).text(obj.timeusage+'ms');
                    $('#memoryusage'+(n+1)).text(obj.memoryusage+'KB');
                    if(obj.result=='AC'){
                      $('#casestatus'+(n+1)).css('color','green');
                      if(obj.ac == "true"){
                          $('#finalstatus').text('Status: AC');
                          $('#finalstatus').css('color','green');
                      }
                    }else{
                      $('#casestatus'+(n+1)).css('color','red');
                      if($('#finalstatus').text()=='Status:WJ...'&&obj.result=='TLE'){
                        $('#finalstatus').text('Status:TLE');
                        $('#finalstatus').css('color','red');
                      }else if(obj.result!='AC'){
                        $('#finalstatus').text('Status:'+obj.result);
                        $('#finalstatus').css('color','red');
                      }

                    }
                    if(n+1<max){
                      judge(n+1,max);
                    }
                  }
              });
}
