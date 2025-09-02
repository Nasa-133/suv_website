<h1>TozaSuv - Water Delivery Web Application</h1>

<p>A modern Django web application for water delivery services with interactive UI and responsive design.</p>

<h2>Features</h2>
<ul>
  <li>Responsive design with Bootstrap 5</li>
  <li>Contact form with Telegram notification integration</li>
  <li>Google Maps integration</li>
  <li>FAQ section</li>
  <li>Admin panel for content management</li>
  <li>Localized for Uzbekistan (Uzbek language, Asia/Tashkent timezone)</li>
</ul>

<h2>Installation</h2>
<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/Hazratov/suv-website.git
cd suv-website</code></pre>
  </li>
  <li>Create and activate a virtual environment:
    <pre><code>python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate</code></pre>
  </li>
  <li>Install dependencies:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Fix the missing module error:
    <pre><code># Fix the ModuleNotFoundError: No module named 'bot'
# Either install the missing module:
pip install python-telegram-bot
# Or modify INSTALLED_APPS in settings.py to remove 'bot' if not needed</code></pre>
  </li>
  <li>Configure the timezone in <code>waterConf/settings.py</code>:
    <pre><code>TIME_ZONE = 'Asia/Tashkent'
USE_TZ = True</code></pre>
  </li>
  <li>Run migrations:
    <pre><code>python manage.py migrate</code></pre>
  </li>
  <li>Create a superuser:
    <pre><code>python manage.py createsuperuser</code></pre>
  </li>
  <li>Run the development server:
    <pre><code>python manage.py runserver</code></pre>
  </li>
</ol>

<h2>Project Structure</h2>
<ul>
  <li><code>waterConf/</code> - Main project directory
    <ul>
      <li><code>waterApp/</code> - Main application directory
        <ul>
          <li><code>templates/</code> - HTML templates
            <ul>
              <li><code>contact.html</code> - Contact page with form and Google Maps</li>
              <li><code>base.html</code> - Base template</li>
            </ul>
          </li>
          <li><code>static/</code> - CSS, JS files and media</li>
          <li><code>models.py</code> - Database models</li>
          <li><code>views.py</code> - View functions</li>
        </ul>
      </li>
      <li><code>waterConf/</code> - Project configuration
        <ul>
          <li><code>settings.py</code> - Project settings</li>
          <li><code>urls.py</code> - URL routing</li>
        </ul>
      </li>
    </ul>
  </li>
</ul>

<h2>Contact Page Features</h2>
<ul>
  <li>Contact information cards (address, phone, email)</li>
  <li>Contact form with validation</li>
  <li>Google Maps integration with marker and directions</li>
  <li>FAQ section with accordion interface</li>
</ul>

<h2>SiteConfig Setup</h2>
<p>After running the server, log in to the admin panel and configure:</p>
<ul>
  <li>Company address</li>
  <li>Phone number</li>
  <li>Email address</li>
  <li>Google Maps embed code</li>
  <li>Add FAQ entries for the contact page</li>
</ul>

<h2>Troubleshooting</h2>
<ul>
  <li>If you encounter <code>ModuleNotFoundError: No module named 'bot'</code>:
    <ul>
      <li>Install the telegram bot module: <code>pip install python-telegram-bot</code></li>
      <li>Or check INSTALLED_APPS in settings.py and remove 'bot' if not needed</li>
    </ul>
  </li>
  <li>Time display issues:
    <ul>
      <li>Ensure TIME_ZONE is set to 'Asia/Tashkent' in settings.py</li>
      <li>Make sure USE_TZ = True is set</li>
    </ul>
  </li>
</ul>

<h2>License</h2>
<p>This project is licensed under the MIT License</p>
