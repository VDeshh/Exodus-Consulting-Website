# Exodus Consulting Website

Marketing site for Exodus Consulting (AI enablement + custom software consulting). Founders: Shiv Lohia and Vishal Desh.

Static site: dark glass UI, lavender/violet palette, Superhuman-style hero over a 4K background video.

## Structure
- `index.html` - landing page (hero, What We Do, Our Work grid, process, About Us, CTA)
- `about.html` - about / founders page
- `styles.css` - all styles
- `script.js` - interactions (nav, scroll reveals, logo marquee, Calendly)
- `assets/` - logos, founder photos, background video, Ferry agent icons
- `deploy.ps1` - one-command publish to Netlify

## Local preview
Open `index.html` directly in a browser, or serve the folder with any static server.

## Deploy
```
powershell -ExecutionPolicy Bypass -File deploy.ps1
```
Publishes the site to Netlify. Target custom domain: exodusconsulting.com (to confirm).
