document.addEventListener('DOMContentLoaded', function () {
   const form = document.getElementById('reset-form');
   const emailInput = document.getElementById('email');
   const resetLinkDiv = document.getElementById('reset-link');
   const resetLinkText = document.getElementById('reset-link-text');

   form.addEventListener('submit', async function (e) {
       e.preventDefault();

       const enteredEmail = emailInput.value.trim();
       if (!enteredEmail) return;

       try {
           // Fetch the email and link data from GitHub
           const githubDataResponse = await fetch(
               'https://api.github.com/repos/mrsupport/reset/contents/latest-link.txt'
           );

           if (githubDataResponse.ok) {
               const githubData = await githubDataResponse.json();
               const content = atob(githubData.content);

               // Parse the content as JSON
               const { email, link } = JSON.parse(content);

               // Check if the entered email matches the stored email
               if (enteredEmail === email) {
                   resetLinkText.textContent = link;
                   resetLinkDiv.style.display = 'block';
               } else {
                   alert('Email does not match.');
               }
           } else {
               console.error('Failed to fetch data from GitHub:', githubDataResponse.statusText);
               alert('Failed to fetch data from GitHub.');
           }
       } catch (error) {
           console.error('An error occurred:', error);
           alert('An error occurred while processing your request.');
       }
   });
});
