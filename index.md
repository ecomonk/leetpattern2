---
layout: default
title: Home
---

<div class="hero">

<h1>My Notes</h1>

<p class="hero-description">
A collection of notes, algorithms, ideas and documentation.
</p>

</div>

<div class="home-grid">

{% assign notes = site.pages | sort: "path" %}

{% for note in notes %}

{% assign path = note.path %}

{% if path contains ".md" %}
{% unless path == "index.md" %}

{% assign name = note.name | remove: ".md" %}
{% assign title = name | replace: "-", " " | replace: "_", " " %}

<a class="note-card" href="{{ note.url | relative_url }}">

<div class="note-card-title">
{{ title | capitalize }}
</div>

<div class="note-card-path">
{{ note.path }}
</div>

</a>

{% endunless %}
{% endif %}

{% endfor %}

</div>
