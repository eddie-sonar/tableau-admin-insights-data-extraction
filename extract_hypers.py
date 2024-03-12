import tableauserverclient as TSC
import os
import zipfile

token_name = os.environ.get("TOKEN_NAME")
token_value = os.environ.get("TOKEN_VALUE")
site_name = os.environ.get("SITENAME")
server_url = os.environ.get("SERVER_URL")

tableau_auth = TSC.PersonalAccessTokenAuth(token_name, token_value, site_name)
server = TSC.Server(server_url, use_server_version=True)
server.add_http_options({'verify': False})
server.auth.sign_in(tableau_auth)

all_project_items, _ = server.projects.get()
admin_insights = [x for x in all_project_items if x.name == 'Admin Insights'][0]
admin_insights_id = admin_insights.id

all_datasource_items, _ = server.datasources.get()
admin_insights_ds = [x for x in all_datasource_items if x.project_id == admin_insights_id]

tdsx_location = "./tdsx"
if not os.path.exists(tdsx_location):
    os.makedirs(tdsx_location)

hyper_location = "./hyper"
if not os.path.exists(hyper_location):
    os.makedirs(hyper_location)

print("\n----- Extracting Admin Insights hyper files from Tableau -----\n")
# download tdsx files
for ds in admin_insights_ds:
    server.datasources.download(ds.id, "./tdsx")

# convert to hyper
for tdsx in os.listdir(tdsx_location):
    table_name = tdsx.removesuffix(".tdsx")
    with zipfile.ZipFile(f"{tdsx_location}/{tdsx}", "r") as zip_ref:
        zipinfos = zip_ref.infolist()
        hyper_file = [x for x in zipinfos if x.filename.endswith(".hyper")][0]
        hyper_file.filename = f"{hyper_location}/{table_name}.hyper"
        print(f"Creating {hyper_file.filename}")
        zip_ref.extract(hyper_file)

