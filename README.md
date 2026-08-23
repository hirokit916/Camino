# Camino — Website

Bilingual (日本語 / English) one-page site for **Camino**, a one-on-one online
tutoring service for international school students.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The entire site — HTML, CSS, and JS in one self-contained file. |
| `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png` | Browser tab / bookmark icons. |

The page is fully self-contained: all photos are embedded directly in
`index.html`, and fonts load from Google Fonts. There is no build step and no
external JavaScript — just open `index.html`.

## Editing

Everything lives in `index.html`.

- **Colors and fonts** are defined once as CSS variables in the `:root { … }`
  block near the top of the `<style>` section (e.g. `--sun` is the amber
  accent, `--leaf` the sage green, `--serif` the English display font).
  Change a value there and it updates everywhere.
- **Text** is bilingual. Each phrase appears twice inside
  `<span data-inl class="ja">…</span><span data-inl class="en">…</span>`.
  Edit the matching language span.

## Deploying with GitHub Pages

1. Create a new repository on GitHub and upload these files (keep them at the
   repository root, or in a `/docs` folder).
2. In the repository, go to **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Select the `main` branch and the `/ (root)` folder (or `/docs` if you put the
   files there), then **Save**.
5. After a minute or two, your site is live at
   `https://<your-username>.github.io/<repo-name>/`.

Because everything is static, any static host (Netlify, Cloudflare Pages,
Vercel, etc.) works the same way — point it at this folder.

## Custom domain (optional)

To use your own domain, add a file named `CNAME` (no extension) containing just
your domain, e.g. `www.camino.example`, then configure the DNS records your host
specifies.
