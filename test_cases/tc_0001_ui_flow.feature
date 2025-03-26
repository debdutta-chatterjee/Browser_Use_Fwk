Feature: E2E Ui Flow

GIVEN I am UI automation tester validating the tasks
WHEN Go to the webpage 'https://rahulshettyacademy.com/loginpagePractise/'
AND Login with username and password, Login details available in the same page
AND Get attribute and url of the page
AND After login, select first 2 products and them to cart
AND Then checkout and store the total value you see on the screen
AND Increase the quantity of any product and check if total value is updated accordingly
AND checkout and select country, agree terms
AND click on purchase button
THEN verify thank you message is displayed
