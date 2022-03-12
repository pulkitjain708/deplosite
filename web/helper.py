from os import walk , path , remove

def checkStatic(dir="",allowed=[],rootFile=""):
    if dir=="" or len(allowed)==0 or rootFile=="":
        return False,"No specifications provided"
    for index,(root,dir,files) in enumerate(walk(dir)):
        if index==0 and len(dir)==1 and len(files)==0:
            return False,"Try zipping going into root of project,improper zip"
        if index==0 and len(files)!=0:
            if rootFile not in files:
                return False,"Serving File not Found at Root of Project"
            elif len(files)==0:
                return False,"No Files Found to Serve "
        if len(files)!=0:
            for file in files:
                ext=file.rsplit('.',1)[1]
                if ext not in allowed:
                    purepath=path.join(root,file)
                    remove(purepath)
        # print("_________{}______________".format(index))
        # print("DIR : ",dir)
        # print("ROOT : ",root)
        # print("FILES : ",files)
        # print("___________________________")
                    
    return True,"Operation Completed"
