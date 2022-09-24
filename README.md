# boxInventory
## Getting started:
 - create and activate a python virtual environment (python 3.5 or above)
 - run `git clone https://github.com/AbhigyaShridhar/boxInventory`
 - `cd cuboid`
 - Install all dependencies by running - `pip install -r requirements.txt`
 - create `.env` file in the root directory of the project and put the following text in it:
 ```
 SECRET_KEY = "someRandomKey123"
 ```
 
 Now run:
 ```
 ./manage.py makemigrations backend
 ./manage.py migrate
 ./manage.py runserver
 ```
 
 Now the project can be accessed on `http://127.0.0.1:8000/`
 
## API

 - `users/register`: registers a new user
 ```
 {
    'username': 'user1',
    'password': 'asdf',
    'first_name': 'john',
    'last_name': 'doe',
    'email': 'email@email.com'
 }
 ```
 
  - `users/login`: gives a **token** which needs to be added as authentication bearer for restricted end points
  ```
  {
      'username': 'user1',
      'password': 'asdf'
  }
  ```
  
   - `users/account`: returns all information and inventory for the current user
   
   - `inventory/add`: add a new box to the inventory
   ```
   {
      'length': 1,
      'breadth': 1,
      'height': 1
   }
   ```
   
   - `inventory/update/<id_of_the_box_to_be_updated>`: updates a box if user and new details are validated
   ```
   {
      'length': 1,
      'breadth': 1,
      'height': 1
   }
   ```
   
    - `inventory/delete/<id_of_the_box_to_be_deleted>`: deletes a box if the user performing the action is validated
    
    - `inventory/view`: view list of boxes
    filters can be applied like:
     - `http://127.0.0.1:8000/inventory/view?after=2022-09-24%2018:17:30.514448`: returns list of boxes created after the given timestamp
     - `http://127.0.0.1:8000/inventory/view?before=09-24%2018:17:30.514448`: returns list of boxes created beforeiven timestamp
     - `http://127.0.0.1:8000/inventory/view?volume_more=1`: returns all boxes with volume greater than or equal to one
     
     Other possible filters are: volume_less, area_more, area_less, breadth_more, breadth_less, height_more, height_less, length_more, length_less, creator(give username
 
  - `users/inventory`: returns all the boxes created by the current user, all the filters apply to this route as well
  
  Authentication token from the `login` route has to be put in headers as: `Authentication: Token <token_value>`
  
  **by default, users are not registered as staff users, this can be changed via admin site**
  
  run:
  `./manage.py createsuperuser` to access the admin site
