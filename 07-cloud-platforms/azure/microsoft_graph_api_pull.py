"""
Scenario: Pull data from Microsoft Graph API (e.g., Users, SharePoint lists, Teams messages,
Outlook calendar/emails) using OAuth2 client-credentials flow (app-only, no user login needed —
ideal for unattended data pipelines).

pip install msal requests pandas

Setup (one-time, in Azure AD / Entra ID):
1. Register an app in Azure AD (App Registrations).
2. Add API permissions (Application type, not Delegated) e.g. User.Read.All, Sites.Read.All.
3. Grant admin consent.
4. Create a client secret.
"""

import msal
import requests
import pandas as pd

TENANT_ID = "your-tenant-id"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]  # .default uses app's granted permissions
GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def get_access_token() -> str:
    """Client-credentials flow — no user interaction, perfect for scheduled pipelines."""
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" not in result:
        raise Exception(f"Auth failed: {result.get('error_description')}")
    return result["access_token"]


def fetch_all_pages(url: str, headers: dict) -> list[dict]:
    """Microsoft Graph paginates via '@odata.nextLink' — loop until exhausted."""
    results = []
    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        payload = resp.json()
        results.extend(payload.get("value", []))
        url = payload.get("@odata.nextLink")  # None when no more pages
    return results


def pull_all_users() -> pd.DataFrame:
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    users = fetch_all_pages(f"{GRAPH_BASE}/users?$select=id,displayName,mail,jobTitle,department", headers)
    return pd.DataFrame(users)


def pull_sharepoint_list_items(site_id: str, list_id: str) -> pd.DataFrame:
    """Common DE scenario: pull SharePoint list used as a business data source."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{GRAPH_BASE}/sites/{site_id}/lists/{list_id}/items?expand=fields"
    items = fetch_all_pages(url, headers)
    rows = [item["fields"] for item in items]
    return pd.DataFrame(rows)


def pull_teams_channel_messages(team_id: str, channel_id: str) -> pd.DataFrame:
    """Pull chat messages for analytics (e.g., engagement dashboards)."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{GRAPH_BASE}/teams/{team_id}/channels/{channel_id}/messages"
    messages = fetch_all_pages(url, headers)
    return pd.DataFrame(messages)


if __name__ == "__main__":
    users_df = pull_all_users()
    print(users_df.head())
    users_df.to_csv("aad_users_export.csv", index=False)
    # Next step in pipeline: load this into a warehouse table (see 03-python/api-to-db)
