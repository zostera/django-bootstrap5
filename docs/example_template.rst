.. code:: django

  {# Load the tag library #}
  {% load django_bootstrap5 %}

  {# Load CSS and JavaScript #}
  {% bootstrap_css %}
  {% bootstrap_javascript %}

  {# Display django.contrib.messages as Bootstrap alerts #}
  {% bootstrap_messages %}

  {# Display a form #}
  <form action="/url/to/submit/" method="post" class="form">
    {% csrf_token %}

    {% bootstrap_form form %}

    {% bootstrap_button button_type="submit" content="OK" %}
    {% bootstrap_button button_type="reset" content="Cancel" %}

  </form>

  {# Read the documentation for more information #}
