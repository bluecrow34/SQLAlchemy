### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?
  An open source database management system

- What is the difference between SQL and PostgreSQL?
  PostgreSQL stores and process data while SQL enables the building of powerful applications

- In `psql`, how do you connect to a database?
  \c
- What is the difference between `HAVING` and `WHERE`?
  A HAVING clause is like a WHERE clause, but applies only to groups as a whole (that is, to the rows in the result set representing groups), whereas the WHERE clause applies to individual rows

- What is the difference between an `INNER` and `OUTER` join?
    inner join will keep only the information from both tables that's related to each other (in the resulting table). An Outer Join, on the other hand, will also keep information that is not related to the other table in the resulting table

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?
    eft outer join contains all records of the "left" table even if it has no matches in the "right" table specified in the join. A right outer join contains all records in the "right" able even if it has no matches in the "left" table. 

- What is an ORM? What do they do?
  Object Relational Mapping is a technique that lets you query and manipulate data from a daatabase using OOP

- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?
  requests are made to a web server and after they are processed the server returns the updated output in a new page load. In an Ajax request, this sequence of actions happens behind the scenes, asynchronously, so that the user is not interrupted.

- What is CSRF? What is the purpose of the CSRF token?
    Criss Site Request Forgery is a secure randomw token that is used to prevent CSRF attacks

- What is the purpose of `form.hidden_tag()`?
    template argument generates a hidden field that includes a token that is used to protect the form against CSRF attacks