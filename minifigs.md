---
layout: default
title: Minifigs
description: The Marvelous Blocks minifig collection, with a dedicated page for every minifig.
permalink: /minifigs/
---

# Minifigs

My LEGO minifig collection.

{% assign minifigs = site.minifigs | where_exp: "minifig", "minifig.images.size > 0" | sort: "bricklink_id" %}

{% if minifigs.size == 0 %}
  <p class="minifig-empty">No minifigs published yet. Check back soon.</p>
{% else %}
  <section class="minifig-grid" aria-label="Minifig collection">
    {% for minifig in minifigs %}
      <article class="minifig-card">
        <a href="{{ minifig.url | relative_url }}">
          <img src="{{ minifig.images.first | relative_url }}" alt="{{ minifig.title }}" loading="lazy" width="80" height="80">
          <div>
            <p class="minifig-id">{{ minifig.bricklink_id }}</p>
            <h2>{{ minifig.title }}</h2>
          </div>
        </a>
      </article>
    {% endfor %}
  </section>
{% endif %}
