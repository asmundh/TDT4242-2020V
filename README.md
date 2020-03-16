# Aggrelance Project
Åsmund Haugse & Odd Gunnar Aspaas

1. [Introduction](#1-introduction)  
  1.1 [Problem description](#11-problem-description)
2. [Standards](#2-standards)  
  2.1 [Whitebox testing approach](#21-whitebox-testing-approach)  
  2.2 [Blackbox testing approach](#22-blackbox-testing-approach)  
  2.3 [Django testing approach](#23-django-testing-approach)  
  2.4 [CI/CD configuration](#24-cicd-configuration)  
  2.5 [Design standards](#25-design-standards)
3. [Test Driven Development Methodology](#3-test-driven-development-methodology)  
  3.1 [Overview](#31-overview)  
  3.2 [Approach](#32-approach)  
4. [Implementations](#4-implementations)  
   4.1 [Boundary value tests](#41-boundry-value-tests)  
      4.1.1 [Give project offers](#411-give-project-offers)  
      4.1.2 [Sign-up page](#412-sign-up-page)  
5. [New features](#5-new-features)    
    5.1 [Use case 1](#51-use-case-1)  
      5.1.1 [Design](#511-design)  
      5.1.2 [Tests](#512-tests)  
    5.2 [Use case 2](#52-use-case-2)  
      5.2.1 [Design](#521-design)  
      5.2.2 [Tests](#522-tests)  
    5.3 [Use case 3](#53-use-case-3)  
      5.3.1 [Design](#531-design)  
      5.3.2 [Tests](#532-tests)  

<h2>1. Introduction</h2>
During this exercise we will practice software development in the DevOps 
environment and white-box and black-box testing approach. 

<h3>1.1. Problem Description</h3>
From exercise 1, we got the [requirements](#5-new-features) of some new features from our peer 
group. In this exercise, we will enhance the existing web application by adding 
new features. In addition, we are going to practice the 
[testing approached](#3-test-driven-development-methodology) learned from the lectures to find bugs of the 
existing web application and to ensure the quality of the new features you add. 

<h2>2. Standards</h2>  
<h3>2.1 Whitebox testing approach</h3> 
<h3>2.2 Blackbox testing approach</h3> 
In short terms, blackbox testing is the act of testing the functionality of a system. For instance, we could test that for a given input, the component being tested will reyturn the correct output. This means that we do not worry about the internal processes or structure of the component. Blackbox testing also includes non-functional testing, such as performance or usability. 

When we are testing functionality through blackbox testing we are interested in finding errors in the system, for example missing or incorrect functions or initialization and terminator errors. With tests in place, discovering new errors as a  result of changes to the code can be made easier. If a previously passing test now fails, this could indicate unwanted errors in the code.

Blackbox testing holds the advantage of it not being dependent on knowledge of the internal structure and composition of the system. This means that the tests can be made once the requirement specifications of the system have been defined. Furthermore, the tests can be created by a third party not involved in the development of the system.  

These strength can also pose as weaknesses. If the requirements specifications are not properly developed, writing tests for the sytem can prove hard or even impossible. In the real world, requirements specifications are seldom perfect, thus designing and writing the test cases often prove difficult.

<h3>2.3 Django testing approach</h3> 
<h3>2.4 CI/CD configuration</h3> 
<h3>2.5 Design standards</h3> 
We will stride to keep the existing feel of Agreelance by inspecting the pages 
and draw inspiration from their layout and style. We will use the design tool 
[Figma](https://www.figma.com/) during our design phase of implementing the 
new features.

Font style:  `"Roboto","Lucida Grande","DejaVu Sans","Bitstream Vera Sans",Verdana,Arial,sans-serif;`

<h2>3. Test Driven Development Methodology</h2>
<h3>3.1 Overview</h3>
<h3>3.2 Approach</h3>

<h2>4. Implementations</h2>
<h3>4.1 Boundary value tests</h3>
<h4>4.1.1 Give project offers</h4>
<h4>4.1.2 Sign-up page</h4>

<h2>5. New features</h2>
<h3>5.1 Use case 1</h3>
User Profile with description

| ID and Name       | FR3 - Creating user profiles                                                                                                                                                                                                                                                                                                            |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Created By:       | Odd Gunnar, Åsmund Date Created: 03.02.2020                                                                                                                                                                                                                                                                                             |
| Primary Actor     | Entrepreneur                                                                                                                                                                                                                                                                                                                            |
| Secondary Actor   | Customer, Database, Server                                                                                                                                                                                                                                                                                                              |
| Description       | All users should have a profile. This profile should have a field where the person can choose to write about themself and their skills.                                                                                                                                                                                                 |
| Definitions       | Account: The entity a user needs to have to be able to maneuver and interact with Agreelance. <br/>Profile: Information about an account.                                                                                                                                                                                               |
| Trigger           | The user signs up to Agreelance or pushes the edit profile button in settings.                                                                                                                                                                                                                                                          |
| Preconditions     | PRE-1: A user must have an account. <br/> PRE-2: The user must be authenticated. <br/> PRE-3: Database is online.                                                                                                                                                                                                                       |
| Postconditions    | POST-1: New description about a person is stored in database.<br/> POST-2: New description is visible to other users of the system.                                                                                                                                                                                                     |
| Normal flow       | **3.0 Creating a profile description for existing account** <br/> 1. The user navigates to their profile page. <br/> 2. The user presses the “Edit profile” button to enter edit mode. <br/> 3. The user changes their profile description. <br/> 4. The user confirms the change. <br/> 5. The change is stored in the database. <br/> |
| Alternative flows | **3.1 Creating a profile description when signing up** <br/> 1. The user prompts to sign up for Agreelance. <br/> 2. The user fills in a description about themself. <br/> 3. The user sends their sign-up information. <br/> The description is stored in the database alongside other information about the user.                     |
| Exceptions:       | **2.0.E1 Customer does not write a description** <br/> 1.System displays a banner message: “Your profile has no description. Please add one now!”. <br/>2. The user clicks on the banner to start normal flow. <br/> a) The user clicks on the banner to start normal flow. <br/>b) The user clicks “x” to close the banner.            |  |
| Priority          | Medium                                                                                                                                                                                                                                                                                                                                  |
| Frequency of Use  | Not necessarily used. Can be used repeatedly if the user wants to update their description.    |

<h4>5.1.1 Design</h4>
![User_page_1](/uploads/5d198d5b221b8e10959d9c0a7b6791a6/User_page_1.png)
<h4>5.1.2 Tests</h4>

<h3>5.2 Use case 2</h3>
<h4>5.2.1 Design</h4>
<h4>5.2.2 Tests</h4>

<h3>5.3 Use case 3</h3>
<h4>5.3.1 Design</h4>
<h4>5.3.2 Tests</h4>

  