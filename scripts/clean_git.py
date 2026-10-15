import os
import glob
import subprocess
import sys

def find_git_exe():
    # Common location for GitHub Desktop Git on Windows
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if not local_app_data:
        # Fallback if env var missing
        user_profile = os.environ.get("USERPROFILE", "C:\\Users\\kobe2")
        local_app_data = os.path.join(user_profile, "AppData", "Local")
        
    search_pattern = os.path.join(local_app_data, "GitHubDesktop", "app-*", "resources", "app", "git", "cmd", "git.exe")
    git_paths = glob.glob(search_pattern)
    
    if git_paths:
        return git_paths[0]
        
    # Check standard git in Path just in case
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return "git"
    except Exception:
        pass
        
    return None

def run_git_clean():
    git_exe = find_git_exe()
    if not git_exe:
        print("Error: Could not find git.exe in system path or GitHub Desktop installation.")
        sys.exit(1)
        
    print(f"Using Git executable: {git_exe}")
    
    # 腳本位於 scripts/，專案根目錄為其上一層
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(repo_dir)
    print(f"Working directory: {repo_dir}")
    
    # Git commands to remove untracked stuff from cache (keeps local files intact)
    commands = [
        [git_exe, "rm", "-r", "--cached", "node_modules"],
        [git_exe, "rm", "-r", "--cached", "thomas-backend/.gradle"],
        [git_exe, "rm", "-r", "--cached", "thomas-backend/build"],
        [git_exe, "rm", "-r", "--cached", "thomas-backend/bin"],
        [git_exe, "rm", "-r", "--cached", "dist"],
        [git_exe, "rm", "--cached", "Pitch Deck.pdf"],
        [git_exe, "add", ".gitignore"],
        [git_exe, "commit", "-m", "chore: remove node_modules and ignore build files to fix Vercel deploy"],
        [git_exe, "push", "origin", "main"]
    ]
    
    for cmd in commands:
        cmd_str = " ".join(cmd)
        print(f"\nRunning: {cmd_str}")
        try:
            # We ignore errors on rm if files are not in index
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"Stderr/Warning: {result.stderr}")
        except Exception as e:
            print(f"Command failed: {str(e)}")
            
    print("\nGit cleanup complete!")

if __name__ == "__main__":
    run_git_clean()
