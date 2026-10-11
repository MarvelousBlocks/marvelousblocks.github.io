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

- Main pages are markdown files (`index.md`, `minifigs.md`, `mocs.md`, `impressum.md`, `privacy.md`).
- Social links are defined once in `_config.yml` under `social.links`.
- Minifig entries are stored in `_data/minifigs.json`.

### Adding a MOC

Each MOC is one markdown file in `_mocs/` and renders at `/mocs/<file-name>/`.
The `MOCs` overview page at `/mocs/` lists all MOCs automatically, ordered by
the `order` field.

1. Copy `_templates/moc.md` into `_mocs/` and rename it, for example
   `_mocs/my-awesome-build.md`.
2. Fill in the front matter fields: `title`, `description`, `image`, `order`.
3. Store the MOC's images under `assets/images/mocs/` and reference them in the
   markdown, for example `![Section 1](/assets/images/mocs/section-1.jpg)`.
4. Write the build documentation below the front matter. Use a `##` heading per
   build section and add text and images freely. The page layout, the `All MOCs`
   back link, and the overview card are added automatically.
5. Preview locally with `bundle exec jekyll serve`, then commit.

`_templates/moc.md` is never published; only files in `_mocs/` become MOC pages.
