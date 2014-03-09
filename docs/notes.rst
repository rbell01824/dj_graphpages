


# noinspection PyStatementEffect
"""
{% extends "base.html" %}
{% load graphpage %}
{% load crispy_forms_tags %}

{% block content %}
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-6">
                <h3>This is a form page</h3>
                <p>It contains one or more forms, like the one below.</p>
                <p>You can put any explanation text above the form.</p>
            </div>
        </div>

{% form no_countries %}
class GraphForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=80, label='Title')
    number_countries = forms.IntegerField(max_value=50, min_value=5,
                                          label='Number of countries')
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_action = 'graphpages/graphpage3/{{graph_pk}}'
    helper.add_input(Submit('submit', 'Show graph', css_class='btn-primary'))
{% endform no_countries %}

        <div class="row">
            <div class="col-md-6">
               </br>
               <p>Likewise you can put any instructions or whatever after the form.</p>
               <p>Forms support django-crispy-forms and bootstrap3!</p>
            </div>
        </div>
    </div>
{% endblock content %}
"""

# noinspection PyStatementEffect
"""
{% extends "base.html" %}
{% load chartkick %}

{% query %}
title1 = 'Top {{number_countries}} countries by land area'
r = CIA.objects.order_by('-land_area')[:{{number_countries}}]
data1 = [[o.name, o.land_area] for o in r]

title2 = 'Top {{number_countries}} countries by population'
r = CIA.objects.order_by('-population')[:{{number_countries}}]
data2 = [[o.name, o.population] for o in r]
{% endquery %}

{% block content %}
    <div class="container-fluid">
        <div class="jumbotron">
            <h3>Django Graph Pages</h3>
            <p>This template displays two pie charts side by side in a fluid grid.</p>
        </div>
    </div>

    <div class="container-fluid">
        <div class="row">
            <div class="col-md-6">
                <h3>{{ title1 }}</h3>
                {% pie_chart data1 with id='chart-1' %}
                <a class="btn btn-primary" href="javascript:history.back()">Back</a>

            </div>
            <div class="col-md-6">
                <h3>{{ title2 }}</h3>
                {% pie_chart data2 with id='chart-2' %}
                <a class="btn btn-primary" href="javascript:history.back()">Back</a>
            </div>
        </div>
    </div>
{% endblock content %}
"""
