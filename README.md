

# closet_project

To simply use the website open a web browser and go to `https://ramzinaamane.pythonanywhere.com/register` to register a new user and get started with the website.




# Overview of the code:

1. Install the required packages using the following command:
   ```
   pip install Flask flask_sqlalchemy flask_login
   ```

2. Make sure you have Python installed on your machine.

3. Navigate to the directory where the code is saved.

4. Run the following command to start the server:
   ```
   python <filename>.py
   ```

5. The code sets up a Flask web application with SQLAlchemy for database management and Flask-Login for user authentication.

6. It defines several database models such as Users, Closet, tops, bottoms, shoes, and Images to store user information and items in the closet.

7. The code includes routes for registering, logging in, and logging out users. It also allows adding, viewing, and deleting items (tops, bottoms, shoes) in the closet.

8. Users can upload images for their items and manage their closet through the web interface.

9. The code provides error handling and flashing messages to notify users of their actions.

10. It also includes code to drop and create the database tables when the application runs.

11. Feel free to modify the code to add more features, customize the user interface, or expand the functionality of this code.

