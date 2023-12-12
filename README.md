# WhoAmISlack
Simple Command Line Tool to Enumerate Slack Workspace Names from Slack Webhook URLs.

You need a Slack OAuth User Token with team:read privs to enumerate a workspace name. These are free and easy to create.

**Important: You can use any account's OAuth token to enumerate cross-workspace names. This means you can enumerate a workspace name for any Slack Webhook.**

## Installation & Usage

1. Install the `requests` pypi library.

```
pip install requests
```

2. Run the `getslackworkspace.py` script.

```
python3 getslackworkspace.py --token <TOKEN_VALUE> https://hooks.slack.com/T234DSLKJ/BSDFJWEK23/e9Wi324jlkasdf
```

The script takes one (or two) command line arguments. 
- A Slack User OAuth token with `team:read` privs (see below how to generate it). You can set an env variable named `SLACK_OAUTH_TOKEN` to the token value or pass the token on the command line with the `--token` flag.
- A Slack Webhook URL. This is a required and a positional argument.

## Generate a Slack User OAuth Token

1. Login to any Slack workspace (or create a new one) in the browser and visit [https://api.slack.com/apps](https://api.slack.com/apps).
2. Click `Create New App`. Select `From scratch`. Name it and associate it with a workspace.
3. Click `OAuth and Permissions` under `Features`. 
4. Under `Scopes` > `User Token Scopes`, add the `team:read` permission.
5. Scroll up. Under `OAuth Tokens for Your Workspace`, click `Install to Workspace`.
6. Copy your `User OAuth Token`.
