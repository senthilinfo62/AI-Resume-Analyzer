# GitHub Actions for AI Resume Analyzer

This directory contains GitHub Actions workflows for the AI Resume Analyzer project.

## Workflows

### Main Workflow (`main.yml`)

This workflow runs on pushes to the main/master branch and on pull requests to these branches.

It consists of the following jobs:

1. **test-backend**: Runs the backend tests using pytest
2. **test-frontend**: Runs the frontend tests using Vitest
3. **build**: Builds Docker images for both frontend and backend
4. **deploy** (commented out): Can be configured for deployment

## Setting Up GitHub Actions

To use these workflows:

1. Push your code to GitHub
2. GitHub will automatically detect the workflow files in the `.github/workflows` directory
3. The workflows will run according to the triggers defined in the workflow files

## Configuring Secrets

If you need to use secrets (e.g., for deployment), you can add them in your GitHub repository:

1. Go to your repository on GitHub
2. Click on "Settings"
3. Click on "Secrets and variables" > "Actions"
4. Click on "New repository secret"
5. Add your secrets (e.g., `DOCKER_USERNAME`, `DOCKER_PASSWORD`, etc.)

## Customizing Workflows

You can customize the workflows by editing the YAML files in this directory. For example:

- Add more jobs
- Change the triggers
- Add deployment steps
- Configure caching

## Troubleshooting

If a workflow fails:

1. Click on the failed workflow run in the "Actions" tab of your repository
2. Examine the logs of the failed job
3. Fix the issues and push your changes
4. The workflow will run again automatically
