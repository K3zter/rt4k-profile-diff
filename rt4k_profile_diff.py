import sys
import zipfile
import shutil
import stat
from os import listdir, makedirs, chmod, remove
from os.path import isdir, isfile
from git import Repo, repo

class UpdateFile():
    def __init__(self, version_num, file_name):
        self.version_num = version_num
        self.file_name = file_name

def sort_version(val):
    return val.version_num

temp_dir = "./temp/"
results_file = "./results.txt"

def rm_dir_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    chmod(path, stat.S_IWRITE)
    func(path)

print("Working...")

if isdir(temp_dir):
   shutil.rmtree(temp_dir, ignore_errors=False, onerror=rm_dir_readonly)

if isfile(results_file):
    remove(results_file)

makedirs(temp_dir)

if(len(sys.argv) != 3):
    print("2 arguments expected")
    exit

file_names = [sys.argv[1].replace('.\\', ''), sys.argv[2].replace('.\\', '')]
files = []

for file in file_names:
    version_num = file[5:8]
    files.append(UpdateFile(version_num, file))

files.sort(key=sort_version)

print("Comparing bundle version " + files[0].version_num + " with version " + files[1].version_num + "...")

with zipfile.ZipFile(files[0].file_name, 'r') as zip_ref:
    for file in zip_ref.namelist():
        if file.startswith('profile/'):
            zip_ref.extract(file, temp_dir)

repo = Repo.init(temp_dir + 'profile')
repo.git.add(all=True)
commit = repo.index.commit(files[0].version_num)

for item in listdir(temp_dir + 'profile'):
    if item != ".git":
        if(isdir(temp_dir + 'profile/' + item)):
            shutil.rmtree(temp_dir + 'profile/' + item, ignore_errors=False, onerror=rm_dir_readonly)
        else:
            remove(temp_dir + 'profile/' + item)

with zipfile.ZipFile(files[1].file_name, 'r') as zip_ref:
    for file in zip_ref.namelist():
        if file.startswith('profile/'):
            zip_ref.extract(file, temp_dir)

repo.git.add(all=True)
repo.index.commit(files[1].version_num)

print("Generating " + results_file)

diff_added = repo.git.diff('HEAD~1..HEAD',name_only=True,diff_filter="A")
diff_modified = repo.git.diff('HEAD~1..HEAD',name_only=True,diff_filter="M")
diff_removed = repo.git.diff('HEAD~1..HEAD',name_only=True,diff_filter="D")
diff_renamed_list = commit.diff("HEAD").iter_change_type("R")
diff_renamed = ""

for diff in diff_renamed_list:
    lines = str(diff).split('\n')
    diff_renamed = diff_renamed + lines[4][19:-1] + " -> " + lines[5][17:-1] + "\n"

f = open(results_file, "x")

if(len(diff_added)):
    f.write("NEW PROFILES\n============\n")
    f.write(diff_added)

if(len(diff_modified)):
    f.write("\n\nMODIFIED PROFILES\n=================\n")
    f.write(diff_modified)

if(len(diff_removed)):
    f.write("\n\nREMOVED PROFILES\n================\n")
    f.write(diff_removed)

if(len(diff_renamed)):
    f.write("\n\nMOVED PROFILES\n==============\n")
    f.write(diff_renamed)
    
repo.close()

if isdir(temp_dir):
   shutil.rmtree(temp_dir, ignore_errors=False, onerror=rm_dir_readonly)

print("Done!")