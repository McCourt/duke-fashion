# duke-fashion

Please refer to the sqltest folder for how to generate the “production” dataset and load it into your database. 

How to set up the server and deploy the application: 
```{bash}
./manage.py runserver
```

Project description:
The process goes as follows: To be able to sell or buy clothes, students must register for an account and log in. Once a seller posts a clothes item online, this item has an open-for-bidding time frame of 7 days, within which any buyer who is interested in the item can bid a higher price than the selling price, or the last highest bid. If no one bids for the item during the time period, the item will expire automatically. After the user bids an item of interest, if someone else bids the same item with a higher price, the user will receive an email notification and can bid an even higher price if he or she wants.
In addition to functions described above, our web application provides other beneficial and user-friendly features for both sellers and users: to begin with, every visitor to our webpage can view clothes details, and conveniently filter items to display according to customized criteria. Every registered user also has access to his own profile page, which clearly lists clothes items he has put for sale and bidded. Besides, sellers only need to fill out a simple form to post a clothes item, which is particularly useful for those who have multiple items to sell.

File description:
models.py: data models
urls.py: redirect
views.py: functions and queries
forms.py: user input