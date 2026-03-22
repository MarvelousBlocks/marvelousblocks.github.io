# Marvelous Blocks Website

Jekyll-based website for Marvelous Blocks, hosted on GitHub Pages.

## Local development

1. Install Ruby and Bundler.
2. Install dependencies:

```bash
bundle install
```

3. Start local server:

```bash
bundle exec jekyll serve
```

4. Open http://127.0.0.1:4000

## Content editing

- Main pages are markdown files (`index.md`, `minifigs.md`, `impressum.md`, `privacy.md`).
- Social links are defined once in `_config.yml` under `social.links`.
- Minifig entries are stored in `_data/minifigs.json`.
