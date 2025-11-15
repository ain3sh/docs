# Git-backed Configuration and Token Store

The application can be configured to use a Git repository as a backend for storing both the `config.yaml` file and the authentication tokens from the `auth-dir`. This allows for centralized management and versioning of your configuration.

To enable this feature, set the `GITSTORE_GIT_URL` environment variable to the URL of your Git repository.

**Environment Variables**

| Variable                | Required | Default                   | Description                                                                                             |
|-------------------------|----------|---------------------------|---------------------------------------------------------------------------------------------------------|
| `MANAGEMENT_PASSWORD`   | Yes      |                           | The password for management webui.                                                                      |
| `GITSTORE_GIT_URL`      | Yes      |                           | The HTTPS URL of the Git repository to use.                                                             |
| `GITSTORE_LOCAL_PATH`   | No       | Current working directory | The local path where the Git repository will be cloned. Inside Docker, this defaults to `/CLIProxyAPI`. |
| `GITSTORE_GIT_USERNAME` | No       |                           | The username for Git authentication.                                                                    |
| `GITSTORE_GIT_TOKEN`    | No       |                           | The personal access token (or password) for Git authentication.                                         |

**How it Works**

1.  **Cloning:** On startup, the application clones the remote Git repository to the `GITSTORE_LOCAL_PATH`.
2.  **Configuration:** It then looks for a `config.yaml` inside a `config` directory within the cloned repository.
3.  **Bootstrapping:** If `config/config.yaml` does not exist in the repository, the application will copy the local `config.example.yaml` to that location, commit, and push it to the remote repository as an initial configuration. You must have `config.example.yaml` available.
4.  **Token Sync:** The `auth-dir` is also managed within this repository. Any changes to authentication tokens (e.g., through a new login) are automatically committed and pushed to the remote Git repository.
