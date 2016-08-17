## Synopsis

A URL Shortening service (similar to bit.ly, tinyurl.com) with django.

## Example

A long URL is converted into a micro URL with a custom alias if provided otherwise a random code is good to go. Every submission is associated to a random user. Duplicate URLs and aliases are not entertained.

## Motivation

Micro URLs are readable and beautiful.

## Installation

`# mkdir dev`

`# cd dev`

`/dev# git clone https://github.com/asma-kothari-dev/micro_url.git`

`/dev# virtualenv venv`

> New python executable in venv/bin/python

> Installing setuptools, pip...done.

`/dev# source venv/bin/activate`

`/dev# cd micro_url/micro_url/`

`/dev/micro_url/micro_url# pip install -r requirements.txt`

> Successfully installed django requests django-bootstrap-toolkit coverage

> Cleaning up...

`/dev/micro_url/micro_url# python manage.py syncdb`

> Superuser created successfully.

`/dev/micro_url/micro_url# python manage.py makemigrations`

`/dev/micro_url/micro_url# python manage.py migrate`

`/dev/micro_url/micro_url# python manage.py create_fake_users 100`

> Successfully created 100 random user(s)

`/dev/micro_url/micro_url# sh run.sh`

> System check identified no issues (0 silenced).

> August 17, 2016 - 08:13:00

> Django version 1.8.6, using settings 'micro_url.settings'

> Starting development server at http://127.0.0.1:8000/

> Quit the server with CONTROL-C.

### - Access Home Page

![home-page](https://cloud.githubusercontent.com/assets/6028395/17714451/b5662c26-63b4-11e6-8a8b-2fd431dc3715.png)

### - Create Micro URL

![add-link-and-alias](https://cloud.githubusercontent.com/assets/6028395/17714515/ffeb4290-63b4-11e6-9886-e6649ea3fd30.png)

### - Display Micro URL

![display_micro_url](https://cloud.githubusercontent.com/assets/6028395/17715328/6e83af1e-63b8-11e6-9569-cb819bb406fb.png)

### - Preview Micro URL

![preview-micro-url](https://cloud.githubusercontent.com/assets/6028395/17714546/27c21744-63b5-11e6-876b-8f587070154b.png)

### - Redirect from Micro URL to Original URL

![redirect-from-micro-url-to-original-url](https://cloud.githubusercontent.com/assets/6028395/17714582/3a4b1ba4-63b5-11e6-80ac-1b5606d114dc.png)


## Tests

`/dev/micro_url/micro_url# sh runtests.sh`

```
Name                                              Stmts   Miss  Cover
---------------------------------------------------------------------
shrink/__init__.py                                    1      0   100%
shrink/admin.py                                       6      0   100%
shrink/forms.py                                      27      0   100%
shrink/management/__init__.py                         0      0   100%
shrink/management/commands/__init__.py                0      0   100%
shrink/management/commands/_random_users.py          50     12    76%
shrink/management/commands/create_fake_users.py      33      9    73%
shrink/migrations/0001_initial.py                     7      0   100%
shrink/migrations/__init__.py                         0      0   100%
shrink/models.py                                     62      4    94%
shrink/tests/__init__.py                              0      0   100%
shrink/tests/test_create_micro_url.py                65      0   100%
shrink/tests/test_display_micro_url.py               31      0   100%
shrink/tests/test_home.py                            10      0   100%
shrink/tests/test_preview_micro_url.py               34      0   100%
shrink/tests/test_redirect.py                        41      0   100%
shrink/urls.py                                        3      0   100%
shrink/views.py                                      43      2    95%
---------------------------------------------------------------------
TOTAL                                               413     27    93%
```
