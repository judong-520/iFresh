from fdfs_client.client import Fdfs_client


client = Fdfs_client('F:/Projects/django_env/client.conf')
ret = client.upload_by_filename('htpy.mp4')
print(ret)



