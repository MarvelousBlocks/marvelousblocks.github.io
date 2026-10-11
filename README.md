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
- Minifig pages are collection files in `_minifigs/` and render at `/minifigs/<bricklink-id>/`.

### Adding a Minifig

Each minifig is one markdown file in `_minifigs/` and renders at `/minifigs/<bricklink-id>/`.
The `Minifigs` overview page at `/minifigs/` lists all minifigs that provide at least one
image, ordered by BrickLink ID.

1. Copy `_templates/minifig.md` into `_minifigs/` (create the directory on first use) and
   rename it to the BrickLink ID, for example `_minifigs/sh0015.md`.
2. Fill in the front matter fields: `title`, `bricklink_id` (must match the file name), and
   `images`. The image list is required: a minifig without an image is not displayed on the
   overview. Optionally add `youtube_url`, `brickset_url`, and `brickeconomy_url`.
3. Store the minifig's photos under `assets/images/minifigs/<bricklink-id>/` and reference
   them in the `images` list, for example `/assets/images/minifigs/sh0015/sh0015_1.jpg`.
4. Write the description below the front matter. The page layout, the `All Minifigs` back
   link, the image gallery, and the BrickLink link are added automatically.
5. Preview locally with `bundle exec jekyll serve`, then commit.

`_templates/minifig.md` is never published; only files in `_minifigs/` become minifig pages.

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
