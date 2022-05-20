# RDD-TheProphecy Maintenance Guide

The web portal is deployed onto a Platform as a Service (PaaS) cloud platform with a clould database PostgreSQL. To made any changes on the web portal development, the future team should utilize Heroku & PgAdmin for the hosting and database side.

____________________________________________________
## Overview
**1. Heroku**

    Action 1: Deployment of Code onto Heroku
    Action 2: Add Buildpacks
    Action 3: Configure SSL
    Action 4: Add Private Domain Name

**2. PgAdmin**

    Action 1: View all information in selected table
    Action 2: Manage procedure set at PgAdmin
    
____________________________________________________

## Accounts details used for Heroku and Gmail

**Email    : RDDTheProphecy@gmail.com**

**Password : RDD_TheProphecy1**
____________________________________________________

## Part 1: Heroku

2 applications are deployed at Heroku: **rdd-theprophecy** & **rdd-theprophecy-predict**

**Action 1: Deployment of Code onto Heroku**

The method of App connected to GitHub has some confliction after the Heroku start its maintenance, thus, the preferable way for now is:
- Deploy using Heroku Git (the reference cac be found in Heroku as shown in screenshot)
![image](https://user-images.githubusercontent.com/34600547/168775595-e82aa80f-fd98-4b95-a407-82f658f2ccc9.png)

**Action 2: Add Buildpacks**

The current buildpacks is heroku/php. New buildback can be added under the setting section.
![image](https://user-images.githubusercontent.com/34600547/168776033-386e23f1-3b40-4347-b891-76b9fe43ced3.png)

**Action 3: Configure SSL**

SSL Certificates is one of the category under setting. The Heroku free plan need to upgrade to a paid plan to utilize the build in SSL certification. Cloudflare is able to host domain with free SSL Certificates but it has limited upload size of 100MB that is not enough for this web portal to upload machine learning model.
![image](https://user-images.githubusercontent.com/34600547/168777568-7de1336a-cf65-4353-9bff-7ab08f6576a6.png)

**Action 4: Add Private Domain Name**

The web portal is using the default domain provided by heroku. A specific domain name can be added by configuring it through the Add domain button.
![image](https://user-images.githubusercontent.com/34600547/168778170-5dbb1460-27a8-4ea3-8ed0-5f5962cf89ae.png)
____________________________________________________

## Part 2: PgAdmin

PgAdmin is the platform to manage the postgreSQL database. 

**Some useful links when using pgAdmin:**
* Connect using XAMPP @ https://softtechs.org/2020/10/01/how-to-connect-postgresql-with-xampp/
* Create table @ https://www.guru99.com/create-drop-table-postgresql.html
* Connect Database in PgAdmin @ https://stackoverflow.com/questions/11769860/connect-to-a-heroku-database-with-pgadmin
* Preference Dialog Error @ https://stackoverflow.com/questions/69544583/please-configure-the-postgresql-binary-path-in-the-preferences-dialog
* Set AutoIncrememnt @ https://stackoverflow.com/questions/48446399/sql-auto-increment-pgadmin-4

**Information required when establish the database connected:**
* host=ec2-3-216-221-31.compute-1.amazonaws.com
* dbname=ddji904cha3set
* user=frzxfyklyoytbw
* port=5432
* sslmode=require
* password=6be1eb7f38291fdde5be4fc7707a108f3db8f11542897ff6716b80cf9fe93c64

**Action 1: View all information in selected table**

E.g. view information of RDD user.
1. Right click 'user' at the sidebar.
2. Select 'View/Edit Data'.
3. Select 'All Rows'

![image](https://user-images.githubusercontent.com/34600547/169373619-468541a5-ceb3-4e41-8940-a49bbf7a6796.png)

4. All information displayed

![image](https://user-images.githubusercontent.com/34600547/169374306-d1bae7d9-98d1-4ad4-8ef0-730b0eb83a3d.png)


**Action 2: Manage procedure set at PgAdmin**

Procedure is unique in postgreSQL. It is the custom function that can be reuse in the applications as part of different database workflows. 


Use the code below to check all functions available at the database, select query tool to open the query editor:
```
select n.nspname as function_schema,
       p.proname as function_name,
       l.lanname as function_language,
       case when l.lanname = 'internal' then p.prosrc
            else pg_get_functiondef(p.oid)
            end as definition,
       pg_get_function_arguments(p.oid) as function_arguments,
       t.typname as return_type
from pg_proc p
left join pg_namespace n on p.pronamespace = n.oid
left join pg_language l on p.prolang = l.oid
left join pg_type t on t.oid = p.prorettype 
where n.nspname not in ('pg_catalog', 'information_schema')
order by function_schema,
             function_name;
```
Double click on the row under definition column can get full text of function / procedure created:
![image](https://user-images.githubusercontent.com/34600547/169373181-b2c371a0-8785-4691-8f48-bd28cc3295ed.png)
To update the function / procedure, copy the text under definition, paste the text in query editor, make changes on the text and run the query.
____________________________________________________
End of Document
____________________________________________________
