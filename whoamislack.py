import argparse, os, re, requests

def validate_args(args: argparse.Namespace) -> argparse.Namespace:
    # Use --token if provided, otherwise use env var, otherwise exit
    args.token = args.token or os.environ.get('SLACK_OAUTH_TOKEN')
    if not args.token:
        print("Slack OAuth Token with team:read scope is required. You can pass this in as an env var named SLACK_OAUTH_TOKEN or via --token on the command line. See the README on how to generate this token.")
        exit(1)

    # Validate webhook URL format
    pattern = r"https://hooks\.slack\.com/services/(T[a-zA-Z0-9]+)/[a-zA-Z0-9]+(/[a-zA-Z0-9]+)?"
    match = re.match(pattern, args.webhook)
    if not match:
        print("Invalid Slack webhook URL format.")
        exit(1)

    # Add match to args for use in get_slack_team_info
    args.webhook_match = match

    return args

def get_slack_team_info(webhook_match: re.Match, token: str) -> dict:
    # Extract Team ID from webhook URL
    team_id = webhook_match.group(1)

    # Send POST request to Slack API team.info endpoint
    api_url = f"https://slack.com/api/team.info?team={team_id}&pretty=1"
    headers = {
        'authority': 'slack.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary2EjSfkUlbGELqAyL',
        'origin': 'https://api.slack.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }
    data = f'''------WebKitFormBoundary2EjSfkUlbGELqAyL\r\nContent-Disposition: form-data; name="content"\r\n\r\nnull\r\n------WebKitFormBoundary2EjSfkUlbGELqAyL\r\nContent-Disposition: form-data; name="token"\r\n\r\n{token}\r\n------WebKitFormBoundary2EjSfkUlbGELqAyL--\r\n'''
    r = requests.post(api_url, headers=headers, data=data)
    
    # Check response and return JSON when successful
    if r.status_code == 200:
        if r.json().get('ok'):
            return r.json()
        
    # On error, print error message and exit
    try:
        print(f"Failed to retrieve Slack Workspace info. Error Message: {r.json().get('error')}")
    except:
        print(f"Failed to retrieve Slack Workspace info.")
    exit(1)

def print_team_info(team_info: dict):
    #Parse JSON response
    id = team_info.get('team').get('id')
    workspace_name = team_info.get('team').get('name')
    domain = team_info.get('team').get('domain')

    # Print team id, workspace name, and domain (if different from workspace name)
    print(f"Team ID: {id}")
    print(f"Workspace Name: {workspace_name}")
    if workspace_name != domain:
        print(f"Domain: {domain}")

if __name__ == "__main__":
    # Parse args and validate
    parser = argparse.ArgumentParser(description="Retrieve Slack Workspace Names from a Slack Webhook URL.")
    parser.add_argument("--token", required=False, help="Slack User OAuth Token with team:read scope (note: a token from any Slack account works). You can pass this in as an env var named SLACK_OAUTH_TOKEN.")
    parser.add_argument("webhook", help="Webhook URL for Slack")
    args = parser.parse_args()
    args = validate_args(args)
    
    # Get Slack Team Info and print
    team_info = get_slack_team_info(args.webhook_match, args.token)
    print_team_info(team_info)

    
