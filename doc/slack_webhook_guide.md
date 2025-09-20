# How to Get a Slack Webhook URL

This guide will walk you through the process of creating an Incoming Webhook in Slack. This URL will allow the Infoseeker application to send notifications to a channel in your workspace.

### Step 1: Create a New Slack App

1.  Go to the [Slack API website](https://api.slack.com/apps).
2.  Click on the **"Create New App"** button.
3.  In the modal that appears, select **"From scratch"**.
4.  Enter an **App Name** (e.g., "Infoseeker Notifier") and select the **Workspace** you want to send notifications to.
5.  Click **"Create App"**.

### Step 2: Activate Incoming Webhooks

1.  After creating the app, you will be redirected to the app's settings page. In the sidebar, under **"Features"**, click on **"Incoming Webhooks"**.
2.  On the Incoming Webhooks page, toggle the **"Activate Incoming Webhooks"** switch to **On**.

### Step 3: Create a Webhook for a Channel

1.  Now that webhooks are activated, a new section will appear at the bottom of the page called **"Webhook URLs for Your Workspace"**.
2.  Click on the **"Add New Webhook to Workspace"** button.
3.  On the next screen, select the **channel** where you want the notifications to be posted (e.g., `#general` or a dedicated `#papers` channel).
4.  Click **"Allow"**.

### Step 4: Copy the Webhook URL

1.  You will be redirected back to the Incoming Webhooks settings page.
2.  Your new webhook URL will be listed in the **"Webhook URLs for Your Workspace"** section. It will look something like this:
    ```
    https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
    ```
3.  Click the **"Copy"** button to copy the URL.

### Step 5: Add the URL to `config.py`

1.  Open the `config.py` file in the Infoseeker project.
2.  Paste the copied URL as the value for the `SLACK_WEBHOOK_URL` variable.

That's it! Your application is now configured to send notifications to your Slack channel.
