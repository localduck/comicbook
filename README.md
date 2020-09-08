# comicbook
Tiny web comicbook reader


<hr>
<strong>About:</strong>

A tiny project on a bunch of <code>Python + Django</code>, which is a Web Comic Reader. Development perspective: web comics aggregator.


<hr>
<strong>Python requirements:</strong>

<code>pip freeze</code>
<ul>
<li>python==3.8.3</li>
<li>Django==3.0.8</li>
<li>django-braces==1.14.0</li>
<li>django-cleanup==5.0.0 #will be removed afte rewrite some functions</li>
<li>django-crispy-forms==1.9.2</li>
<li>social-auth-app-django==4.0.0</li>
</ul>

<hr>
<strong>Local run:</strong>

<p style="color: red;">github doesn't work with empty folders, so:</p>
<code>
mkdir media &&
cd media &&
mkdir comic &&
mkdir title
</code>
<br>
<code>python manage.py runserver --settings=comicbook.settings.base</code>


<hr>
<strong>Server run:</strong>

At folder comicbook-->settings create file  production.py with:

<p>DEBUG = ...</p>
<p>SECRET_KEY = ...</p>
<p>ALLOWED_HOSTS = ...</p>
<p>CACHES = ...</p>
<p>STATIC_URL = '/static/'</p>
<p>STATIC_ROOT = ...</p>
<p>MEDIA_URL = '/media/'</p>
<p>MEDIA_ROOT = ...</p>

-- And other important stuffs that u needed


<hr>
<strong>LICENSE:</strong>

This work is licensed under a <a href="http://creativecommons.org/licenses/by/4.0/" rel="nofollow">Creative Commons Attribution 4.0 International License</a>.
