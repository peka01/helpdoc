# GitHub Actions Setup for Automatic Deployment

This guide explains how to set up automatic deployment of your MkDocs documentation to GitHub Pages using GitHub Actions.

## Prerequisites

1. Your repository must be public, or you must have GitHub Pro/Enterprise for private repository GitHub Pages
2. You must have admin access to the repository

## Step 1: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select **GitHub Actions**
5. Click **Save**

## Step 2: Configure GitHub Pages Settings

1. In the **Pages** section, ensure the following settings:
   - **Source**: GitHub Actions
   - **Branch**: Leave as default (GitHub Actions will handle this)
   - **Custom domain** (optional): If you have a custom domain, add it here

## Step 3: Push the Workflow File

The `.github/workflows/deploy.yml` file has been created in the root of your repository. Simply push this to your repository:

```bash
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions workflow for automatic deployment"
git push origin main
```

## Step 4: Verify Deployment

1. After pushing, go to the **Actions** tab in your repository
2. You should see the "Deploy to GitHub Pages" workflow running
3. Once completed, your documentation will be available at:
   - `https://[username].github.io/[repository-name]/`
   - Or your custom domain if configured

## How It Works

The workflow automatically:

1. **Triggers** on every push to `main` or `master` branch
2. **Builds** your MkDocs documentation using Python 3.9
3. **Installs** dependencies from `requirements.txt`
4. **Builds** the site using `mkdocs build`
5. **Deploys** to GitHub Pages

## Troubleshooting

### Common Issues

1. **Build fails**: Check the Actions tab for error messages
2. **Dependencies missing**: Ensure all required packages are in `requirements.txt`
3. **Permission errors**: Verify the workflow has the correct permissions

### Manual Trigger

You can manually trigger the workflow:
1. Go to **Actions** tab
2. Click on **Deploy to GitHub Pages**
3. Click **Run workflow**
4. Select the branch and click **Run workflow**

## Customization

### Branch Protection

Consider protecting your main branch:
1. Go to **Settings** → **Branches**
2. Add rule for `main` branch
3. Enable **Require pull request reviews before merging**
4. Enable **Require status checks to pass before merging**

### Environment Variables

If you need custom environment variables:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add repository secrets as needed
3. Reference them in the workflow using `${{ secrets.SECRET_NAME }}`

## Support

If you encounter issues:
1. Check the GitHub Actions logs in the **Actions** tab
2. Verify your `mkdocs.yml` configuration
3. Ensure all dependencies are properly specified in `requirements.txt`
