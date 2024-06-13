
NOTES FOR REFFERENCE


1,  To backup data before refreshing the database:

    1 - General backing
        -   python manage.py dumpdata --format json --indent 4 > fixtures/fixtures.json
    2 - Specific backing
        -   python manage.py dumpdata mall --format json --indent 4 > fixtures/mall.json
    3 - More specific backing
        -   python manage.py dumpdata mall.Product --format json --indent 4 > fixtures/products.json


2,  To load data after refreshing the database:

    1 - python manage.py loaddata fixtures/fixtures.json

3,  If static files disturb probably it is because of mimetypes. Paste this on top of route settings.py after imports

        import mimetypes

        mimetypes.add_type("text/css", ".css", True)

        mimetypes.add_type("text/js", ".js", True)

4,  Remember to keep the secret key used in production secret



git init
git add -A    or    git add . /if it is a new repository
git commit -m "your message"
git push -u origin deeporacles:main/to github
git push heroku deeporacles:main/ to heroku

flutter dependency http: ^0.13.4




python -m venv env   /# creating a virtual environment

django-admin startproject deeporacles 

py manage.py startapp deeporacles

pip install -r requirements.txt     /# installing requirements .


TESTS

py manage.py test      /# this is a normal python command to run test

coverage run manage.py test      #/ this is a command using coverage package.  coverage helps to identify areas that need testing.

coverage report      #/ this command helps to identify areas where testing is  needed.

coverage run --omit='*/ajonv/*' manage.py test      #/ this command helps to omit the venv folder we dont need  to test

coverage html            #/   this command creates html reports for you to see where missing tests exist



<!-- easy thumbnail -->

     in settings.py

     THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
}

    {% load thumbnail %}
    <img src="{{ profile.photo|thumbnail_url:'avatar' }}" alt="" />


    Manually specifying size / options

    Template:

    {% load thumbnail %}
    <img src="{% thumbnail profile.photo 50x50 crop %}" alt="" />

    Using in combination with other thumbnailers
    Alternatively, you load the templatetags by {% load easy_thumbnails_tags %} instead of traditional {% load thumbnail %}. It’s especially useful in projects that do make use of multiple thumbnailer libraries that use the same name (thumbnail) for the templatetag module:

    {% load easy_thumbnails_tags %}
    <img src="{% thumbnail profile.photo 50x50 crop %}" alt="" />





    AttributeError: 'NoneType' object has no attribute 'items' #


The Python "AttributeError: 'NoneType' object has no attribute 'items'" occurs when we try to call the items() method on a None value, e.g. assignment from function that doesn't return anything. To solve the error, make sure to only call items() on dict objects.

Here is an example of how the error occurs.

my_dict = None
# ⛔️ AttributeError: 'NoneType' object has no attribute 'items'
result = my_dict.items()
if my_dict is not None:
    print('variable is NOT None')
    print(my_dict.items())
else:
    print('variable is None')

Trying to call the items() method on a None value is what causes the error.

If you print the variable you are calling items() on, it will be None, so you have to track down where the variable gets assigned a None value and correct or remove the assignment.
The most common source of a None value (other than an explicit assignment) is a function that doesn't return anything.

# 👇️ this function returns None
def get_dict():
    print({'name': 'Alice', 'age': 30})
# 👇️ None
my_dict = get_dict()

# ⛔️ AttributeError: 'NoneType' object has no attribute 'items'
print(my_dict.items())
Notice that our get_dict function doesn't explicitly return a value, so it implicitly returns None.

We assigned the result of calling the function to a variable and tried to call items() which caused the error.
The "AttributeError: 'NoneType' object has no attribute 'items'" occurs for multiple reasons:

Having a function that doesn't return anything (returns None implicitly).
Explicitly setting a variable to None.
Assigning a variable to the result of calling a built-in function that doesn't return anything.
Having a function that only returns a value if certain condition is met.
Some built-in methods mutate a data structure in place and don't return a value. In other words, they implicitly return None.
Make sure you aren't assigning the result of calling a method that returns None to a variable.

If a variable might sometimes store a dict and sometimes store None, you can explicitly check if the variable is not None before you call items().

my_dict = {'name': 'Alice', 'age': 30}
if my_dict is not None:
    print('variable is NOT None')
    print(my_dict.items())  # 👉️ dict_items([('name', 'Alice'), ('age', 30)])
else:
    print('variable is None')

The if block will run only if the my_dict variable does not store a None value, otherwise the else block runs.

Another common cause of the error is having a function that returns a value only if a condition is met.

def get_dict(a):
    if len(a) > 1:
        return a
my_dict = get_dict({'name': 'Alice'})

print(my_dict)  # 👉️ None

The if statement in the get_dict function is only ran if the passed in dictionary has a length greater than 1.

In all other cases, the function doesn't return anything and ends up implicitly returning None.
To solve the error in this scenario, you either have to check if the function didn't return None or return a default value if the condition is not met.

def get_dict(a):
    if len(a) > 1:
        return a
    return {}

my_dict = get_dict({'name': 'Alice'})

print(my_dict)  # 👉️ {}
Now the function is guaranteed to return a dict regardless if the condition is met.



'AsgiRequest' object has no attribute 'user' error

Using the request.user for django debug toolbar, please make sure the middleware that uses the request.user attribute is run AFTER the middleware in charge of the authentication (knox, or whatever you use), otherwise there won't be any user at all, and you will hit this.

