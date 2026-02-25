
# zye6.github.io

# Hugo + PaperMod + GitHub Pages

This is a beginner-friendly **Hugo** blog using the **PaperMod** theme, deployed with GitHub Actions.

## Why Hugo (for your case)

You asked for a first-time setup and learning path:
- Hugo is fast and simple once scaffolded.
- Markdown-first authoring is clean for blog posts.
- GitHub Pages deployment is reliable through Actions.

When Jekyll may still be better:
- If you want the absolute fewest moving parts in GitHub Pages (native Jekyll support, no build workflow).

## Project structure

```text
.
├── .github/workflows/hugo-gh-pages.yml
├── archetypes/default.md
├── content/
│   ├── _index.md
│   ├── about/index.md
│   └── posts/
│       ├── blog-1.md
├── themes/PaperMod/
└── hugo.toml
```

## Add your local `blog.md` file

Copy content into:
- `content/posts/blog-1.md`

Each file already has Hugo front matter. Edit `title` and `date` as needed.

## Local run

1. Install Hugo ([Hugo docs](https://gohugo.io/installation/)).
2. Start server:

```bash
hugo server -D
```

3. Open `http://localhost:1313`.

## Theme notes

- Active theme is set in [hugo.toml](/Users/tim/Code/github-page/hugo.toml): `theme = "PaperMod"`.
- Theme source is in `themes/PaperMod`.
- If you later initialize git, you can switch this to a git submodule setup.

## Deploy on GitHub Pages (first time)

1. Push this repo to GitHub (branch `main`).
2. In GitHub: `Settings -> Pages`.
3. Under `Build and deployment`, choose `GitHub Actions`.
4. Push again (or run workflow manually) and wait for the `Deploy Hugo site to Pages` workflow.

Your URL will look like:

`https://<your-username>.github.io/<repo-name>/`

## Helpful Hugo commands

Create a new post:

```bash
hugo new content/posts/my-new-post.md
```

Build production output:

```bash
hugo --minify
```

