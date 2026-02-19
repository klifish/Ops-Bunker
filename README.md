# Ops-Bunker

A privacy-focused research blog and operational bunker powered by Hugo and GitHub Pages.

## 🚀 Live Site

The site is automatically deployed to GitHub Pages at: **https://klifish.github.io/Ops-Bunker/**

## 📝 About

This repository contains the source code for L K's Nexus - a digital record dedicated to Blockchain Privacy, Zero-Knowledge Proofs (ZKP), and digital sovereignty research.

## 🏗️ Structure

```
.
├── docs/               # Hugo site source
│   ├── content/       # Markdown content
│   ├── themes/        # Hugo themes
│   └── hugo.toml      # Hugo configuration
└── .github/
    └── workflows/
        ├── hugo.yml   # GitHub Pages deployment workflow
        └── wake-up.yml # Heartbeat monitoring
```

## 🔧 GitHub Pages Setup

This repository uses GitHub Actions to automatically build and deploy the Hugo site to GitHub Pages.

### Prerequisites

1. Go to repository **Settings** → **Pages**
2. Under **Build and deployment**, set:
   - **Source**: GitHub Actions
3. The workflow will automatically deploy on pushes to the `main` branch

### Manual Deployment

You can manually trigger a deployment:
1. Go to **Actions** tab
2. Select **Deploy Hugo site to Pages**
3. Click **Run workflow**

## 💻 Local Development

To run the site locally:

```bash
cd docs
hugo server -D
```

Visit `http://localhost:1313` to preview the site.

## 📚 Adding Content

Create a new post:

```bash
cd docs
hugo new posts/my-post.md
```

Edit the generated file in `content/posts/my-post.md`.

## 🤖 Automated Systems

- **GitHub Pages**: Automatic deployment on push to `main`
- **Wake-Up System**: Hourly heartbeat monitoring via Telegram

## 📄 License

See repository for license details.
