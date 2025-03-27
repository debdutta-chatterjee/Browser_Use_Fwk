Feature: Wikipedia E2E Ui Flow

GIVEN Go to url 'https://en.wikipedia.org/'
THEN Click on the desired language 'EN'
AND Enter the search term 'AI' in the search bar
AND Click on the first link in the search results list
THEN Verify the page header is 'Artificial intelligence'