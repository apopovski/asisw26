# Publish Endpoint Setup

This project supports global publishing via `/api/publish`.

## 1) Local env file (for local testing)

Copy `.env.example` to `.env` and fill values:

- `ASISW_EDIT_PASSWORD`
- `GITHUB_TOKEN`
- `GITHUB_OWNER`
- `GITHUB_REPO`
- `GITHUB_BRANCH`
- `GITHUB_CONTENT_PATH` (optional, default `site-content.json`)

## 2) GitHub token permissions

Use a token with **Repository Contents: Read and write** for your target repo.

## 3) Vercel deploy setup

1. Import this GitHub repo into Vercel.
2. Framework preset can remain **Other** (static + serverless API).
3. In Vercel project settings, add environment variables with the same names as above.
4. Deploy.

`vercel.json` is already included and configures:

- Serverless function for `api/publish.js`
- `Cache-Control: no-store` for `/site-content.json`

## 4) How publish works

- User unlocks edit mode in the UI.
- Clicking **Publish** sends payload to `/api/publish` with `X-Edit-Password` header.
- API validates password, then commits updated `site-content.json` to GitHub.
- Updated content becomes globally available after redeploy/refresh (depending on host pipeline).

## 5) Important note

The unlock password entered in the page must exactly match `ASISW_EDIT_PASSWORD` on the server.
