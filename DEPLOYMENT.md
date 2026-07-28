# Deployment guide

## GitHub

The repository is configured to keep `.env`, Streamlit secrets, virtual environments, caches, local SQLite state, and the source MovieLens ZIP out of version control. The extracted MovieLens CSV files are intentionally tracked so offline recommendations work after deployment.

```powershell
git add .
git commit -m "Prepare CineMind AI for deployment"
git remote add origin https://github.com/YOUR-USERNAME/cinemind-ai.git
git push -u origin main
```

## Streamlit Community Cloud

1. Create a new app from the GitHub repository, with `app.py` as the entrypoint.
2. In **Advanced settings → Secrets**, add:

   ```toml
   TMDB_API_KEY = "your_tmdb_api_key"
   ```

3. Deploy. The app runs in offline MovieLens mode when the secret is absent.

Do not upload `.env` or commit credentials. For local development, retain the private `.env` file at the project root.
