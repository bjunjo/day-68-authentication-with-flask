# day-68-authentication-with-flask
## Problem: Make a simple signup page using Flask
## Solution:

1. Using the database (accessing the data). e.g. `User.query.filter_by(email=request.form.get('email')).first()`

```
# Check if the user already exists in the database

# Solution 1: My solution using the 'for' loop
for user in user_list:
  if request.form.get("email") == user.email:
      flash("Looks like you've already registered. Please login.", "info")
      return redirect(url_for('login'))

# Solution 2: Angela's solution using 'filter_by'--fewer and simpler codes
if User.query.filter_by(email=request.form.get('email')).first():
    # User already exists
    flash("You've already signed up with that email, log in instead!")
    return redirect(url_for('login'))
```

2.Use if statement to show a different navbar once a user login

```
# Make sure to pass the "logged_in" in each return statement
# In main.py
....
return render_template("login.html", logged_in=current_user.is_authenticated)

# base.html
<li class="nav-item">
  <!-- Show 'Log Out' only if a user logged in  -->
      {% if logged_in: %}
      <a class="nav-link" href="{{ url_for('logout') }}">Log Out</a>
      {% endif %}
</li>
```

## Lessons
1. If you're working with a wrong model, you're going to get wrong results all the time. 
E.g. I was confused with logging in the user data vs getting the user from the database

2. Authentication isn't hard, just build on top of the basic programming logic, such as "if-statement"
