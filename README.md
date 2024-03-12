# Tableau Admin Insights to Sqlite3

A script to download Tableau Admin Insights data and save it to a local sqlite3 db for analysis using SQL.

## Prereqs

Run

`pip install tableauserverclient`

`arch -x86_64 /usr/bin/python3 -m pip install pantab`

Make a [Personal Access Token on Tableau](https://help.tableau.com/current/server/en-us/security_personal_access_tokens.htm#create-personal-access-tokens) and create a `.env` file, with the following configurations:

```
TOKEN_NAME="<token_name>"
TOKEN_VALUE="<token_value>"
SITENAME="sonarsource"
SERVER_URL="dub01.online.tableau.com"
```

## How to run

Run

`bash get_admin_insights.sh`

Now you can connect to the generated `admin_insights.db` using your SQL IDE and explore the tables.