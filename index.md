---
layout: home
title: My Notes
---

Welcome to my notes.

{% assign notes = site.static_files | where_exp: "file", "file.path contains '.md'" %}

## Notes

{% for file in notes %}
{% unless file.path contains "index.md" %}
- [{{ file.basename | replace: "-", " " | capitalize }}]({{ file.path | relative_url }})
{% endunless %}
{% endfor %}
