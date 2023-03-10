# The Cafe Beats

### Developer: Dhvani Intwala

![Mockup-screenshot-image](Screenshot/Screenshot-of-the-mockup-image.png)

The Cafe beats website has been developed to provide users the chance to order food for delivery or pick-up via a command line based interface.

[View live website]()


# Table of Contents

1. [Project Goals](#project-goals)
    1. [User Goals](#user-goals)
    2. [Site Owner Goals](#site-owner-goals)
2. [User Experience](#user-experience)
    1. [Target Audience](#target-audience)
    2. [User Requirements and Expectations](#user-requirements-and-expectations)
    3. [User Stories](#user-stories)
    4. [Site Owner Stories](#site-owner-stories)
    5. [User Manual](#user-manual)
3. [Technical Design](#technical-design)
    1. [Structure](#structure)
    2. [Flowchart](#flowchart)
    3. [Data Models](#data-models)
4. [Technologies Used](#technologies-used)
    1. [Coding Languages](#coding-languages)
    2. [Frameworks and Tools](#frameworks-and-tools)
    3. [Libraries](#libraries)
5. [Features](#features)
    1. [Existing Features](#existing-features)
    2. [Future Implementations](#future-implementations)
6. [Python Valiadation](#python-validation)
7. [Testing](#testing)
    1. [Device Testing](#device-testing)
    2. [Browser Compatibility](#browser-compatibility)
    3. [Manual Testing](#manual-testing)
    4. [Automated Testing](#automated-testing)
8. [Bugs](#bugs)
9. [Deployment](#deployment)
10. [Credits](#credits)
11. [Acknowledgements](#acknowledgements)


## Project Goals

### User Goals
- Be able to easily interact with the app to order food for    pick up or home delivery.
- Navigate the app seamlessly.
- Receive clear instructions on their current input options.
- Be able to add and remove items from an order prior to order confirmation.
- Be able to cancel the order.
- The ability to preview their order.
- Be able to quit the app from any page.

### Site Owner Goals

- Provide potential customers an easy-to-use app to order food from the cafe beats.
- To save the user information and order data to a Google Sheets worksheet.

## User Experience

### Target Audience

- People looking to have food ordered for delivery.
- People looking to pick up food from the store.

### User Requirements and Expectations

- The ability to seamlessly navigate through the app.
- To have a well organized menu.
- To have a easy ordering process.
- To have validation that inputs have been successfully entered.

### User stories

-  As a user, I want to be provided with clear instructions throughout the app.
- As a user, I want to be able to choose between order pick up or delivery.
- As a user, I want to be able to view the menu.
- As a user, I want to be able to add items to my order.
- As a user, I want to be able to remove items from my order.
- As a user, I want to be able to preview an order.
- As a user, I want to be able to cancel an unplaced order.
- As a user, I want to be able to place an order.
- As a user, I want to be shown a receipt.
- As a user, I want to be able to exit the app.

### Site Owner Stories

- As a site owner, I would want users to be greeted with a welcome message to give a friendly feel to the app.
- As a site owner, I would want to save the user information and order data to a Google Sheets file.
- As a site owner, I would want users to get feedback based on their input.

### User Manual
<details><summary>Instructions</summary>

#### Overview

The Cafe beats app is for users who wish to place orders for home delivery / pickup.

----

#### Welcome page

Purpose: To greet users

Description: On the Welcome page users are asked if you would like to make an order. userd will be provdied with 2 options. 

- Yes
- No




</details>

## Deployment
This project was deployed to Heroku with following steps:
1. Use the "pip freeze -> requiremnts.txt" command in the terminal to save any libraries that need to be installed in the file.
2. Navigate to https://www.heroku.com/ and login or create an account. 
3. Click the "new" button in the upper right corner and select "create new app".
<details>
<summary>Screenshot</summary>
<img src="Screenshot/new-app.png">
</details>

4. Choose an app name and your region and click "Create app".
<details>
<summary>Screenshot</summary>
<img src="Screenshot/app-name.png">
</details>

5. Under Config Vars store any sensitive data you saved in .json file. Name 'Key' field, copy the .json file and paste it to 'Value' field. Also add a key 'PORT' and value '8000'.
<details>
<summary>Screenshot</summary>
<img src="Screenshot/config-var.png">
</details>

6. Go to the "settings" tab, add the Python build pack and then the node.js build pack (please note they need to be in the correct order of Python above node.js).

<details>
<summary>Screenshot</summary>
<img src="Screenshot/App-information.png">
</details>

<details>
<summary>Screenshot</summary>
<img src="Screenshot/Add-buildpack1.png">
</details

<details>
<summary>Screenshot</summary>
<img src="Screenshot/buildpack.png">
</details>



7. Go to the "deploy" tab and pick GitHub as a deployment method.
<details>
<summary>Screenshot</summary>
<img src="Screenshot/deploy-method.png">
</details>

8. Search for a repository to connect to and select the branch you would like to build the app from.
<details>
<summary>Screenshot</summary>
<img src="Screenshot/manual-deploy.png">
</details>

9. If preferred enable automatic deploys and then deploy branch.
Wait for the app to build and then click on the "View" link which will redirect you to the deployed link.


### Forking the GitHub Repository

We can make a copy of the original repository on our GitHub account to view or make changes too without affecting the original repository, this is known as forking. Forking in GitHub can be done via the following steps:

1. Navigate to www.github.com and log in.
2. Once logged in navigate to the desired [GitHub Repository](https://github.com/jkingportfolio/CI_PP3_Taco_Trailer) that you would like to fork.
3. At the top right corner of the page click on the fork icon.
4. There should now be a copy of your original repository in your GitHub account.

Please note if you are not a member of an organisation on GitHub then you will not be able to fork your own repository.

### Clone a GitHub Repository

You can make a local clone of a repository via the following steps: 

1. Navigate to www.github.com and log in.
2. Once logged in navigate to the desired [GitHub Repository](https://github.com/jkingportfolio/CI_PP3_Taco_Trailer) that you would like to clone.
3. Locate the code button at the top, above the repository file structure.
4. Select the preferred clone method from HTTPS. SSH or GitHub CLI then click the copy button to copy the URL to your clipboard.
5. Open Git Bash
6. Update the current working direction to the location in which you would like the clone directory to be created.
7. Type `git clone` and paste the previously copied URL at Step 4.
8. `$ clone https://github.com/jkingportfolio/CI_PP3_Taco_Trailer`
9. Now press enter and the local clone will be created at the desired local location


## Credits

I used following resources during the project development:

- For Gspreds functions for retrieving and updating the data from and to google sheets [Gspread Documents](https://docs.gspread.org/en/latest/user-guide.html)

- For finding common elements in two lists using sets  
    https://www.geeksforgeeks.org/python-print-common-elements-two-lists

- A tutorial on the use of the tabulate module for displaying table data from pyeng.io was used - [Tabulate](https://pyneng.readthedocs.io/en/latest/book/12_useful_modules/tabulate.html)

## Acknowledgements

I would like to also thank the following:

- My Code Institute mentor Mr Akshat Garg for his guidance through this project.
- My fellow Code Institute students from whom I got the project idea.
- My Brother for his support in debugging.
- Code Institute tutor support who helped me with different issues while doing the project.

[Back to Top](#the-cafe-beats)


