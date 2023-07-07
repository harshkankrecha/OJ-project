
$(document).ready(function() {  
    $('#loading').show();  
    $('#myForm').submit(function(event) {
      event.preventDefault(); // Prevent default form submission    
      var problemId = document.getElementById('problemid').value;  
      console.log(problemId);
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

          $('#submission-result').text("Submission Result: ");
          $('#loading').hide();
          $('#verdict').text(response.verdict).addClass('verdict');
        },
        error: function(xhr, status, error) {
          // Handle errors
          console.log('Error:', error);
        }
      });
    });
  });
  
  