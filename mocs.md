---
layout: default
title: MOCs
description: LEGO MOC builds by Marvelous Blocks, documented with images and text for every build section.
permalink: /mocs/
---

# MOCs

My own LEGO builds, documented step by step.

{% assign mocs = site.mocs | sort: "order" %}

{% if mocs.size == 0 %}
  <p class="moc-empty">No MOCs published yet. Check back soon.</p>
{% else %}
  <section class="moc-grid" aria-label="MOC list">
    {% for moc in mocs %}
      <article class="moc-card">
        <a href="{{ moc.url | relative_url }}">
          <img src="{{ moc.image | relative_url }}" alt="{{ moc.title }}" loading="lazy" width="160" height="160">
          <div>
            <h2>{{ moc.title }}</h2>
            <p>{{ moc.description }}</p>
          </div>
        </a>
      </article>
    {% endfor %}
  </section>
{% endif %}
