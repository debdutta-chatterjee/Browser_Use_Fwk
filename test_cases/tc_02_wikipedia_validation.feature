Feature: Wikipedia E2E Ui Flow

GIVEN Go to url 'https://en.wikipedia.org/'
THEN Click on the desired language 'EN'
AND Enter the search term 'AI' in the search bar
AND Click on the first link in the search results list
AND Click on the 'References' link from the left menu section of the page
THEN Verify the total number of references in the page