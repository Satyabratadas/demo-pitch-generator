import os
import re
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration for Memory Safety
# We define what we care about to prevent reading binary/huge files (like .png, .pt, .mp4)
ALLOWED_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', 
    '.md', '.txt', '.json', '.yml', '.yaml', '.java', 
    '.c', '.cpp', '.h', '.go', '.rs', '.sql', '.sh'
}
# Limit file size to 50KB to prevent memory exhaustion (OOM) on free-tier servers
MAX_FILE_SIZE = 50000 

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()

def is_safe_file(file_name: str, file_size: int) -> bool:
    """Utility to check if a file is safe to process."""
    _, ext = os.path.splitext(file_name)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False
    if file_size > MAX_FILE_SIZE:
        return False
    return True

def parse_github_url(url: str) -> tuple[str, str]:
    """Extracts the owner and repository name from a GitHub URL."""
    clean_url = url.strip().rstrip('/')
    if clean_url.endswith('.git'):
        clean_url = clean_url[:-4]
        
    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, clean_url)
    
    if not match:
        raise ValueError("Invalid GitHub repository URL format.")
        
    return match.group(1), match.group(2)

def fetch_repository_context(url: str) -> str:
    """Fetches the README and top-level directory structure safely."""
    try:
        owner, repo_name = parse_github_url(url)
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        # 1. Fetch README
        try:
            readme_file = repo.get_readme()
            readme_content = readme_file.decoded_content.decode('utf-8')
        except Exception:
            readme_content = "No README.md found."

        # 2. Fetch File Structure (Only if safe)
        try:
            contents = repo.get_contents("")
            file_structure = []
            for content_file in contents:
                if content_file.type == "dir":
                    file_structure.append(f"📁 {content_file.name}/")
                else:
                    # Apply memory safety check here
                    if is_safe_file(content_file.name, content_file.size):
                        file_structure.append(f"📄 {content_file.name}")
                    else:
                        file_structure.append(f"📄 {content_file.name} [SKIPPED - Binary/Large]")
            file_tree_str = "\n".join(file_structure)
        except Exception:
            file_tree_str = "Could not retrieve file structure."

        context = f"""
            REPOSITORY: {owner}/{repo_name}
            =========================================
            TOP-LEVEL FILE STRUCTURE:
            {file_tree_str}
            =========================================
            README CONTENT:
            {readme_content}
            """
        return context

    except Exception as e:
        raise RuntimeError(f"Failed to extract GitHub data: {str(e)}")