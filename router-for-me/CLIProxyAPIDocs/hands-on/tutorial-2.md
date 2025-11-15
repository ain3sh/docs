# Two: Gemini CLI + Codex Hands-on

In the previous article, we successfully converted Qwen Code into an API and called it in Cherry Studio through a simple configuration on CLIProxyAPI. I believe that by reading this, you have a preliminary understanding of the powerful functions and convenience of this tool.

In this tutorial, we will continue to explore and integrate Codex and Gemini CLI.

It should be noted that the configuration file used in this operation is the same as the one in the previous Qwen tutorial.

```yaml
port: 8317

# Please fill in the folder location according to your actual situation
auth-dir: "Z:\\CLIProxyAPI\\auths"

request-retry: 3

quota-exceeded:
  switch-project: true
  switch-preview-model: true

api-keys:
# Please set the Key yourself, used for client access to the proxy
- "ABC-123456"
```

### Configure Codex

First, let's configure Codex. The OAuth authorization process for Codex is very similar to the previous Qwen. Enter `cli-proxy-api --codex-login` in the terminal command line, and the system will automatically open the ChatGPT authorization page. Please log in with your ChatGPT account.

![](https://img.072899.xyz/2025/09/8d78b93fcfb3e111a93f6437f9a6acfa.png)

If it is a ChatGPT Team account, you need to select the corresponding workspace. The page for successful authorization is as follows:

![](https://img.072899.xyz/2025/09/86518a31294a769281c7c5ef8946550e.png)

Back in the terminal command line, you can see that the authentication file has been successfully generated and saved.

![](https://img.072899.xyz/2025/09/c4c9613c9b086a9d8af70d0cf31d75f9.png)

If you have multiple ChatGPT accounts, just repeat the same operation a few times.

It should be noted that currently Codex can only be used by paid ChatGPT members, and free users do not have permission.

### Configure Gemini CLI

Next, let's add Gemini CLI. Gemini CLI is completely free, but some users may encounter problems during the configuration process. Therefore, here I will take you through the entire authorization and authentication process step by step, starting from creating a Google Cloud project.

First, please log in to https://console.cloud.google.com/ with your Google account. After successful login, click the position shown in the figure:

![](https://img.072899.xyz/2025/09/75416d68babdacc8ddd9bfd652a49b38.png)

Click "New Project".

![](https://img.072899.xyz/2025/09/566e57546c8bcd73d7ce41e56581b4a5.png)

After naming the project, click "Create".

![](https://img.072899.xyz/2025/09/9e90a699265fc1dcfb7755f7c1858b73.png)

According to the position in the first step, select the project you just created.

![](https://img.072899.xyz/2025/09/a84803f955e057f34723227bdf55b145.png)

First, copy the project ID in the red box for later use, and then click the position indicated by the arrow in the upper left corner.

![](https://img.072899.xyz/2025/09/c1d1617812ecea50c3a63dfb76eb5c04.png)

Click "APIs & Services" -> "Enabled APIs & services" in order.

![](https://img.072899.xyz/2025/09/782d8096de6276f24fc8ca444ee2910d.png)

Click "ENABLE APIS AND SERVICES".

![](https://img.072899.xyz/2025/09/1c0e48d7434bc76d37ef769d86684595.png)

Enter `cloudaicompanion.googleapis.com` in the search box shown in the figure, and then click the searched "Gemini for Google Cloud".

![](https://img.072899.xyz/2025/09/a52b17b80635df9e46b8d5b49957e3d6.png)

Click "Enable".

![](https://img.072899.xyz/2025/09/58afcf1004138c4c1d63474030d49dff.png)

So far, all the preliminary preparations for Google Cloud have been completed. Now, let's go back to the directory where the CLIProxyAPI program is located, open the terminal command line, and enter `cli-proxy-api --login --project_id [your project ID]`. For example, in this case, it is `cli-proxy-api --login --project_id mimetic-planet-473413-v7`.

Then the authorization page will pop up. Please log in with the Google account that you just used for preparation.

![](https://img.072899.xyz/2025/09/51ca74eb061751336d110b3421c43548.png)

The page for successful verification is as follows:

![](https://img.072899.xyz/2025/09/346f6add9a943f0c324afbad856cc3bf.png)

Back in the terminal command line, you can see that the authentication file has been successfully saved.

![](https://img.072899.xyz/2025/09/8682dc8a08bffd34d7900819e1073960.png)

Some readers may be curious why the command line information after successful verification of Codex and Gemini CLI is different from that of Qwen. The answer is that when verifying Codex and Gemini CLI, CLIProxyAPI will listen to a specific port locally to receive callbacks, so the verification is always successful at one time. When verifying Qwen, CLIProxyAPI will directly obtain authorization information from Qwen's verification server, so there will be up to 60 attempts.

### Verify the model

Let's verify the Codex and Gemini CLI we just added through OAuth. Add the model in Cherry Studio as shown below:

![](https://img.072899.xyz/2025/09/db8e65c9548213303da43cc214ee5000.png)

Try Gemini-2.5-Pro:

![](https://img.072899.xyz/2025/09/a2fc6ce45adcf334a2908984a8db428d.png)

Let's ask GPT-5-Codex again:

![](https://img.072899.xyz/2025/09/c07a3dbd57f728186ad835fa5afdde6d.png)

So far, all models have been successfully integrated. Have you learned it?