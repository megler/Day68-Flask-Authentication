# Flask Authentication App

A basic Flask app that creates new users, checks for login and shows custom
pages based on login status. Python Bootcamp Day 68

## Usage

This app is designed to use basic Flask user authentication and password hashing.
Based on the users login status, they will see a different nav menu and home page.

Custom error messages are given at the registration and login screens based on
incorrect email, password or if user already exists in database.

Password hashing with salting is used via [`werkzeug.security.generate_password_hash()`](https://werkzeug.palletsprojects.com/en/1.0.x/utils/#module-werkzeug.security).

This app was not built with the intention of use, but rather as an educational
tool in order to learn login and security.

## License

[MIT](https://choosealicense.com/licenses/mit/)
