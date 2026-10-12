import os
from dulwich.repo import Repo
from dulwich import porcelain

repo_dir = r"d:\db project\college_club_system"

# Initialize repo
try:
    repo = Repo(repo_dir)
    print("Repo already exists.")
except Exception:
    repo = Repo.init(repo_dir)
    print("Repo initialized.")

# Add all files
# We can stage all non-ignored files
files_to_add = []
for root, dirs, files in os.walk(repo_dir):
    if ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        if f.endswith(".db") or f.endswith(".pyc"):
            continue
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, repo_dir).replace("\\", "/")
        files_to_add.append(rel_path)

porcelain.add(repo, files_to_add)
print(f"Staged {len(files_to_add)} files.")

try:
    commit_sha = porcelain.commit(repo, message=b"Initial commit: College Club Event Management System")
    print(f"Committed: {commit_sha}")
except Exception as e:
    print(f"Commit note: {e}")

# Set remote
config = repo.get_config()
remote_url = b"https://github.com/ramrameshram08-del/college_club_system.git"
config.set((b"remote", b"origin"), b"url", remote_url)
config.set((b"remote", b"origin"), b"fetch", b"+refs/heads/*:refs/remotes/origin/*")
config.write_to_path()
print(f"Remote set to {remote_url.decode()}")
