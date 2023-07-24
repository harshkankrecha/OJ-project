$(document).ready(function() {  
  $("#submit-btn").click(function() {
    var loadingDiv = $("#loading");
    document.getElementById('loading').style.display = 'flex';
    //loadingDiv.style.display = 'flex';
    // Show the loading animation
    loadingDiv.show();
      
    $('#myForm').submit(function(event) {
      event.preventDefault(); // Prevent default form submission    
      var questionId = document.getElementById('questionid').value;  
      console.log(questionId);
      var formData = new FormData(this);  
      $.ajax({
        url: 'submit/',
        //url:'/register',        
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          // Handle the response from the server
          loadingDiv.hide();

          $('#submission-result').text("Submission Result: ");
          $("#verdict1").empty();
          if (response.verdict === "Accepted"){
            $("#verdict1").empty();
            $("#verdict2").empty();
            $('#verdict1').text(response.verdict).addClass('verdict');
          }
          else{
            $("#verdict2").empty();
            $("#verdict1").empty();
            $('#verdict2').text(response.verdict).addClass('verdict');
          }
          
        },
        error: function(xhr, status, error) {
          // Handle errors
          console.log('Error:', error);
        }
      });
    });
  });
  });
  