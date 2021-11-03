# RDD-TheProphecy
Final year project

Collaborators notes: use the list below to access and modify the repository through command line interface. Apply branches during project development.

____________________________________________________
Github Reference Sheet 
____________________________________________________

**git config --global user.name "YOUR NAME"**

Configure the username

**git config --global user.email "YOUR EMAIL ADDRESS"**
  
Configure the user email address that registered in Github
  
**git clone https://github.com/ChinJingJie/RDD-TheProphecy.git**

Download online repository as an offline local working file through HTTPS clone url

**cd**
  
Navigate the directory
  
**git checkout -b build-login-ui**

Create new branches with name build-login-ui

**git status**

Check the status of the file whether it is align or untrack with the repository
 
**git diff**

Print the changes/lines that has been amended

**git add .**

Add everything onto the repository
  
**git commit -m "message to describe commitment"**

Save the changes with a message as declace the action done

**git push -u origin build-login-ui**

Update the changes onto the server, origin is used to define the branch for the first time of push only

**git checkout main**

Change the server into main (not other branch)

**git merge build-login-ui**  

Merge build-login-ui branch into master/main branch

**git push**

Update the changes onto the server
  
**git pull**

Update local file so it is aligned with the repository on the server
