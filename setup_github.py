# Quick setup script untuk GitHub
# Run: python setup_github.py

import subprocess
import os

def run_command(cmd, description):
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"⚠️  {description} - Warning")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_github():
    print("=" * 60)
    print("🚀 Setting up GitHub Repository")
    print("=" * 60)
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("\n❌ Git not installed. Please install Git first.")
        return
    
    # Initialize git if not already
    if not os.path.exists('.git'):
        run_command("git init", "Initializing Git repository")
    
    # Add all files
    run_command("git add .", "Adding files to Git")
    
    # Show status
    run_command("git status", "Checking Git status")
    
    print("\n" + "=" * 60)
    print("📝 Next Steps:")
    print("=" * 60)
    print("\n1. Commit your changes:")
    print("   git commit -m \"Initial commit: Mobile Legends Heroes Scraper\"")
    print("\n2. Create GitHub repository:")
    print("   - Go to: https://github.com/new")
    print("   - Repository name: scraping-mlbb")
    print("   - Description: Mobile Legends Heroes Scraper with Web UI")
    print("   - Make it Public/Private")
    print("   - DON'T initialize with README (already have one)")
    print("\n3. Link to remote repository:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/scraping-mlbb.git")
    print("\n4. Push to GitHub:")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n5. (Optional) Add topics/tags on GitHub:")
    print("   mobile-legends, web-scraping, python, flask, playwright")
    print("\n" + "=" * 60)
    
    # Create a commit helper file
    with open('git_commands.txt', 'w') as f:
        f.write("""# Git Commands untuk Push ke GitHub

# 1. Commit changes
git commit -m "Initial commit: Mobile Legends Heroes Scraper"

# 2. Add remote (ganti YOUR_USERNAME dengan username GitHub Anda)
git remote add origin https://github.com/YOUR_USERNAME/scraping-mlbb.git

# 3. Push to GitHub
git branch -M main
git push -u origin main

# Update .gitignore if needed
# Pastikan mlbb.db, *.json, *.html tidak ke-push

# Future updates:
git add .
git commit -m "Your commit message"
git push
""")
    print("\n💡 Commands saved to: git_commands.txt")

if __name__ == '__main__':
    setup_github()
