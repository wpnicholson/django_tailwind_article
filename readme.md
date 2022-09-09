# Readme

## Setup

1. Install Django with `pip install django`.
2. Start a new Django project, with `django-admin startproject myproject`.
3. Change directories into your project folder: `cd myproject` where the file `manage.py` is located.
4. Double check that a Python interpreter has been selected in VS Code, with _Ctrl_ + _Shift_ + _p_.
5. Configure Django with Tailwind by following the instructions at [Django-Tailwind](https://django-tailwind.readthedocs.io/en/latest/installation.html).
   1. Install the Django-Tailwind package with `python -m pip install django-tailwind`.
   2. Add `'tailwind'` to `INSTALLED_APPS` in `settings.py`:

      ```python
      INSTALLED_APPS = [
          # other Django apps
          'tailwind',
      ]
      ```

   3. Create a Tailwind CSS compatible Django app. Since this is for the benefit of Tailwind, i.e. css styling, it usually makes sense to call it `theme`. So, change directories into the `new_project` folder (where `manage.py` is situated) and run the command `python manage.py tailwind init` and at the prompt enter the name `theme`. Upon doing this you will see a new folder appear within your existing Django project. This folder will contain the `theme` Django app.
   4. Thus now we need to register this new `theme` Django app by adding it to `INSTALLED_APPS` in `settings.py`:

       ```python
       INSTALLED_APPS = [
           # other Django apps
           'tailwind',
           'theme'
       ]
       ```

   5. Register the generated `theme` app by adding the following line to `settings.py` file (right at the bottom of the `settings.py` file): `TAILWIND_APP_NAME = 'theme'`.
   6. Make sure that the `INTERNAL_IPS` list is present in the `settings.py` file and contains the `127.0.0.1 ip` address. Again, place this at the bottom of the `settings.py` file:

      ```python
      INTERNAL_IPS = [
          "127.0.0.1",
      ]
      ```

6. Configure the path to the `npm` executable. On `Windows` use the command prompt and type `where npm` and then copy the full path to the `npm.cmd` executable. Then, place that full path into the `settings.py` file, again right at the bottom: `NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"`.
7. Add and configure `django_browser_reload`, which takes care of automatic page and css refreshes in the development mode. Add it to `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
       # other Django apps
       'tailwind',
       'theme',
       'django_browser_reload',
   ]

8. Add the middleware to the `MIDDLEWARE` section of the `settings.py` file:

   ```python
   MIDDLEWARE = [
       # ...
       "django_browser_reload.middleware.BrowserReloadMiddleware",
       # ...
   ]
   ```

   The middleware should be listed after any that encode the response, such as Django’s GZipMiddleware. The middleware automatically inserts the required script tag on HTML responses before `</body>` when `DEBUG` is `True`.

9. Include `django_browser_reload` URL in your root `url.py` - also here, don't forget to import the `include` function:

   ```python
   from django.urls import include, path
   urlpatterns = [
       ...,
       path("__reload__/", include("django_browser_reload.urls")),
   ]
   ```

10. Install Tailwind CSS dependencies, by running the following command: `python manage.py tailwind install`. Behind the scenes this will run the `npm` command.
11. And at last you should be able to use Tailwind CSS classes in your Django HTML templates. Thus, start the development server by running the following command in your terminal: `python manage.py tailwind start`.

## Development Servers

* There will be two servers that you need to run to make your life easier during further development of your Django project:
  1. The Tailwind server that will watch behind the scenes and update everytime changes are made to your CSS styling as you develop. This server is started in item 11 above: `python manage.py tailwind start`.
  2. The Django development server: `python manage.py runserver`.

## Create a new Django App

* We can now begin developing our Django project in exactly the same way as we would normally. Start by creating a new Django app with `python manage.py startapp myapp`.
* Add the name of your new app (e.g. `myapp` in this case) to your `settings.py` file of the parent project folder:

  ```python
  INSTALLED_APPS = [
      ...

      'tailwind',
      'theme',
      'django_browser_reload',

      'myapp',
  ]
  ```

* Also, add the routing to your root URLconf in `myproject/urls.py`:

  ```python
  from django.urls import include, path

  urlpatterns = [
      path('admin/', admin.site.urls),

      path("__reload__/", include("django_browser_reload.urls")),

      path('', include('myapp.urls')),
  ]
  ```

* For templating, create a new folder called `templates` inside of `myapp` folder. And then, inside of `templates` create another new folder named `myapp`. Finally create an empty file named `index.html` inside `templates/myapp`.
* Now, inside `myapp/views.py` we'll add the view for the above `index.html` file.

  ```python
  def index(request):
      text = 'Hello World!'
      context = {
          'context_text': text,
      }
      return render(request, 'myapp/index.html', context)
  ```

* Back inside the `myapp` folder, create a `urls.py` to store your URLconf. Inside there we define the following:

  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
      path('', views.index, name='index'),
  ]
  ```

* Finally we add some html to our `index.html`:

  ```html
  {% load tailwind_tags %}
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Django Tailwind Example</title>
      {% tailwind_css %}
    </head>
    <body>
      <h1 class="text-2xl bg-slate-200 hover:bg-yellow-400">{{ context_text }}</h1>
    </body>
  </html>
  ```

* Notice here we have added two new Tailwind specific tags to our html template, namely `{% load tailwind_tags %}` at the top of the template and `{% tailwind_css %}` inside the `<head>` tag.
* Now simply start the second server, i.e. the Django development server, with `python manage.py runserver` and visit the page.
