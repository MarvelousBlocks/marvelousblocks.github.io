# Marvelous Blocks Website

Jekyll-based website for Marvelous Blocks, hosted on GitHub Pages.

## Domain and deployment

- Production URL: `https://marvelous-blocks.com`
- Custom domain is configured via `CNAME`.
- GitHub Actions workflow for build/deploy: `.github/workflows/deploy.yml`

### GitHub repository settings required

1. In `Settings -> Pages`, set `Source` to `GitHub Actions`.
2. Ensure your DNS points to GitHub Pages:
   - Apex `A` records to: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www` CNAME to: `marvelous-blocks.com` (or `<your-user>.github.io`)
3. Enable `Enforce HTTPS` in Pages once DNS is active.

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
