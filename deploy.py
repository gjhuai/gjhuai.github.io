import os, pysftp

LOCAL_PATH = os.getcwd()
REMOTE_PATH = "/home/gjh/mynotes"

sftp = pysftp.Connection(host="192.168.31.200", username="gjh", private_key="~\\.ssh\\id_rsa_200_gjh")
if not sftp.exists(REMOTE_PATH):
    sftp.mkdir(REMOTE_PATH)
sftp.chdir(REMOTE_PATH)


for parent,dirs,files in os.walk(LOCAL_PATH):
    if parent.startswith(os.path.join(LOCAL_PATH, '.git')):
        continue
    
    relative_path = parent.replace(LOCAL_PATH, "").replace('\\', '/')
    doc_dir = REMOTE_PATH + '/' + relative_path

    if not sftp.exists(doc_dir):
        sftp.mkdir(doc_dir)
    sftp.chdir(doc_dir)
    print("Upload %s --> %s" % (parent, sftp.pwd))

    for filename in files:
        if sftp.exists(filename):
            attr = sftp.stat(filename)
            # print(attr.st_mtime, attr.st_size)
            localpath = os.path.join(parent,filename)
            size_l = os.path.getsize(localpath)
            
            # 上传 size有变化、最后修改日期大于远程文件的本地文件
            if size_l!=attr.st_size and os.path.getmtime(localpath) > attr.st_mtime:
                print("     file: " + os.path.join(parent,filename))
                sftp.put(os.path.join(parent,filename))
        else:
            print("     file: " + os.path.join(parent,filename))
            sftp.put(os.path.join(parent,filename))


sftp.close()

print("\nSuccessfully uploaded!!!")