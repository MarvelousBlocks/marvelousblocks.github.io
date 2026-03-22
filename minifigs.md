---
layout: default
title: Minifigs
description: Full Marvelous Blocks list of Iron Man armor related LEGO minifigs and current hunt status.
---

{% assign total = site.data.minifigs | size %}
{% assign owned = site.data.minifigs | where: "status", "owned" | size %}
{% assign missing = site.data.minifigs | where: "status", "missing" | size %}
{% assign unknown = site.data.minifigs | where: "status", "unknown" | size %}

# Iron Man Minifig Hunt List

Track every armor-related minifig and follow what is already collected.

<section class="stats" aria-label="Collection progress">
  <p><strong>Total:</strong> <span data-count-all>{{ total }}</span></p>
  <p><strong>Owned:</strong> <span data-count-owned>{{ owned }}</span></p>
  <p><strong>Missing:</strong> <span data-count-missing>{{ missing }}</span></p>
  <p><strong>Unknown:</strong> <span data-count-unknown>{{ unknown }}</span></p>
</section>

<section class="filters" aria-label="Filter minifigs by status">
  <button class="filter-chip is-active" data-filter="all" type="button">All</button>
  <button class="filter-chip" data-filter="missing" type="button">Missing</button>
  <button class="filter-chip" data-filter="owned" type="button">Owned</button>
  <button class="filter-chip" data-filter="unknown" type="button">Unknown</button>
</section>

<section class="minifig-grid" aria-label="Minifig list">
  {% for minifig in site.data.minifigs %}
    <article class="minifig-card" data-minifig data-status="{{ minifig.status }}">
      <img src="{{ minifig.image }}" alt="{{ minifig.name }}" loading="lazy" width="80" height="80">
      <div>
        <p class="minifig-id">{{ minifig.bricklink_id }}</p>
        <h2>{{ minifig.name }}</h2>
        <p class="status status-{{ minifig.status }}">{{ minifig.status }}</p>
        <p><a href="{{ minifig.bricklink_url }}" target="_blank" rel="noopener noreferrer">Open on BrickLink</a></p>
      </div>
    </article>
  {% endfor %}
</section>
