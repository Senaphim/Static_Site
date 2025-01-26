import os
import shutil

def cp_static_to_public():
    rm_public()
    path_list = os.listdir("./static")
    for path in path_list:
        recursive_cp(path)

def rm_public():
    remove_list = os.listdir("./public")
    for path in remove_list:
        full_path = os.path.join("./public", path)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
    
def recursive_cp(path):
    static_path = os.path.join("./static", path)
    public_path = os.path.join("./public", path)
    if os.path.isfile(static_path):
        shutil.copy(static_path, public_path)
    else:
        if not os.path.exists(public_path):
            os.mkdir(public_path)
        path_list = os.listdir(static_path)
        for child_path in path_list:
            recursive_cp(os.path.join(path, child_path))

def main():
    cp_static_to_public()

main()

