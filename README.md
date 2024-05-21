# Perlego take-home assignment - Python specific
Hello and welcome to the domain specific Perlego developer assessment. Congratulations on passing the initial interview; now we are going to test your skills through a realistic challenge that you could experience on the job.
The role you are applying for will require you to have an understanding of Python so today we are going to focus on testing your ability to create and test a solution using Python.

## The Task
For the challenge, we would like you to determine what countries each of the 4 books in the sample data set can be sold in.

## Requirements:
1. The solution must be able to read Sales Rights information for Book records using the ONIX 3.0 standard.
2. The solution must be able read Sales Rights information for Book records using both the normal tags and also the short tags.
2. The solution must be able to parse the information and store the results in an appropriately designed MYSQL database containing the countries permitted for the books.
3. The solution should gracefully handle errors / missing data and exceptions whilst providing appropriate error information.
4. The solution should have an appropriate automated test mechanism.

## Additional Information:
1. For the challenge, you are able to use pre-existing XML parsers and existing ORM solutions.
2. We do not offer a database for you to record the information in, it is recommended you use an online free service to host your MYSQL instance.
3. ONIX 2.1 is out of scope of this activity. Please do not read, refer or code anything with it in mind, it is significantly different from the 3.0 standard.
4. We are only interested in retrieving the ​countries, ​not the regions or other more specific sales restrictions.

## Document and sample files
You can find the Onix3 documentation in the OnixDocs folder. The documentation is structured in the following way:
- The main documentation sits in the `ONIX_for_Books_Format_Specification_3.0.7.pdf` file. This is a very large document containing information about all the fields which can be supplied in an Onix XML file. 
- Each section of Onix will have a mapping codelist which explains what the values in each composite means.

## The Floor is Yours
There are plenty of options for this assessment, in terms of database design and code design. 

We suggest looking at frameworks and ORM's such as Flask, FastAPI, SQLAlchemy, etc.. to help structure your data, show that you can use these frameworks and understand what they're good for. Options like Django could also work, however we think that's one of the more involved framework which is overkill for the task at hand.

What we're looking for is for you to build a solution which we will be able to setup, run and test on our machines, which are probably running different systems, with different versions of Python or these frameworks. To help with this, we highly recommend making use of virtual environments and/or docker with docker-compose, as it will ensure that the environment against which the code will run is the same.

## Scoring:

- Fault tolerant solutions will score more highly.
- Secure solutions will score more highly than non-secure versions.
- Solutions using appropriate design patterns and database design will score more highly.
- Assessments without automated tests will not pass.
- Creative & over-engineered solutions demonstrating your breadth of skills will score more highly and allow us to understand the breadth and depth of your skills.
- Assessments that we can not get to work locally will score poorly. When working through the assessment, think “What can I do to make my work stand out?”. As opposed to what is just enough to meet the requirements. We are looking to evaluate the breadth and depth of your skillset with this exercise, not the volume of code you can produce.


## Help & Questions
If there is anything in the assessment that you do not understand or would like clarification on feel free to contact your recruitment contact, they will make sure you have the answer fast enough to unblock you.

Good luck!
