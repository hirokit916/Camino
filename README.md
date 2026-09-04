# Camino — Website

Bilingual (日本語 / English) one-page site for **Camino**, a one-on-one online
tutoring service for international school students.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The entire site — HTML, CSS, and JS in one file. |
| `logo.png` | Camino logo mark (header + footer). **Required.** |
| `tutor.jpg` | Tutor photo (home card + About tab). **Required.** |
| `og-image.jpg` | Social/link-preview image (1200x630). |
| `robots.txt`, `sitemap.xml` | Search-engine crawling directives. |
| `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png` | Browser tab / bookmark icons. |

All files go in the **same folder** (the repository root). `logo.png` and
`tutor.jpg` were moved out of the HTML to cut the page weight roughly in half —
if they are missing, the logo and photo will not appear.

There is no build step and no external JavaScript. Fonts load
asynchronously from Google Fonts, so they never block the first paint. There is no build step and no
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

## Link preview image

`og-image.jpg` (1200x630) is what shows when the link is pasted into iMessage,
LINE, Slack, X, or Facebook. The `og:` tags in `index.html` already point at the
absolute URL `https://caminotutor.com/og-image.jpg`, so previews work as soon as
the site is live. If the domain ever changes, update `og:url`, `og:image`,
`twitter:image`, `<link rel="canonical">`, `robots.txt` and `sitemap.xml`.

## Search / performance notes

- Fonts load asynchronously (`media="print"` + `onload`), so they never block
  first paint. Only the weights actually used are requested.
- `robots.txt` and `sitemap.xml` are included; submit the sitemap in
  Google Search Console after deploying.
- Tab links are real `<a href="#...">` anchors so Google can crawl them, and
  deep links like `caminotutor.com/#fees` open that tab directly.
- Security headers (CSP, HSTS, COOP, X-Frame-Options) cannot be set on GitHub
  Pages. Putting the site behind Cloudflare (free) lets you add them.
