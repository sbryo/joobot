import dropbox
app_key='4e3oofj6zqcx5dh'
app_secret='vaoz96wg81222c9'
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()
client = dropbox.client.DropboxClient('BH4cEdpiGmAAAAAAAAAAB5P3NEPXB2HO07UZJD56WRC5VfomuHI_Jz6Aa06YUUxl')
f, metadata = client.get_file_and_metadata('/Shaked/History.txt')

lines = f.readlines()
for line in lines:
    S = line.split('=')
    print S[0]
