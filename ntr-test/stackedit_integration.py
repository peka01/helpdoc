#!/usr/bin/env python3
"""
StackEdit Integration Script for NTR Help Documentation

This script provides local integration with StackEdit for managing markdown files
in your documentation repository.
"""

import os
import json
import webbrowser
import subprocess
import argparse
from pathlib import Path
from typing import Optional, List
import requests

class StackEditIntegration:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.config_file = Path("stackedit_config.json")
        self.load_config()
    
    def load_config(self):
        """Load StackEdit configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "recent_files": [],
                "favorite_files": [],
                "stackedit_url": "https://stackedit.io/app#",
                "auto_open_browser": True
            }
            self.save_config()
    
    def save_config(self):
        """Save StackEdit configuration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def list_markdown_files(self) -> List[Path]:
        """List all markdown files in the docs directory"""
        markdown_files = []
        for pattern in ["*.md", "**/*.md"]:
            markdown_files.extend(self.docs_dir.glob(pattern))
        return sorted(markdown_files)
    
    def open_in_stackedit(self, file_path: Optional[str] = None):
        """Open StackEdit in browser, optionally with a specific file"""
        if file_path:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"Error: File {file_path} does not exist")
                return
            
            # Convert to relative path from docs directory
            try:
                rel_path = file_path.relative_to(self.docs_dir)
                print(f"Opening {rel_path} in StackEdit...")
                
                # Add to recent files
                if str(rel_path) not in self.config["recent_files"]:
                    self.config["recent_files"].insert(0, str(rel_path))
                    self.config["recent_files"] = self.config["recent_files"][:10]  # Keep only 10 recent
                    self.save_config()
                
            except ValueError:
                print(f"Error: File {file_path} is not in the docs directory")
                return
        
        # Open StackEdit in browser
        if self.config["auto_open_browser"]:
            webbrowser.open(self.config["stackedit_url"])
            print("StackEdit opened in browser")
        else:
            print(f"StackEdit URL: {self.config['stackedit_url']}")
    
    def create_stackedit_page(self, title: str, content: str = "", filename: Optional[str] = None):
        """Create a new markdown file with StackEdit-ready content"""
        if not filename:
            # Generate filename from title
            filename = title.lower().replace(' ', '-').replace('_', '-')
            filename = ''.join(c for c in filename if c.isalnum() or c in '-')
            filename = f"{filename}.md"
        
        file_path = self.docs_dir / filename
        
        # Create content with frontmatter
        markdown_content = f"""# {title}

{content}

---
*Generated with StackEdit Integration Tool*
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Created new file: {file_path}")
        return file_path
    
    def sync_with_github(self, commit_message: str = "Update documentation"):
        """Sync changes with GitHub repository"""
        try:
            # Add all changes
            subprocess.run(["git", "add", "."], check=True)
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            # Push to remote
            subprocess.run(["git", "push"], check=True)
            
            print("Successfully synced with GitHub")
            
        except subprocess.CalledProcessError as e:
            print(f"Error syncing with GitHub: {e}")
        except FileNotFoundError:
            print("Error: Git not found. Make sure Git is installed and in your PATH.")
    
    def show_recent_files(self):
        """Show recently opened files"""
        if not self.config["recent_files"]:
            print("No recent files")
            return
        
        print("Recent files:")
        for i, file_path in enumerate(self.config["recent_files"], 1):
            print(f"  {i}. {file_path}")
    
    def show_favorite_files(self):
        """Show favorite files"""
        if not self.config["favorite_files"]:
            print("No favorite files")
            return
        
        print("Favorite files:")
        for i, file_path in enumerate(self.config["favorite_files"], 1):
            print(f"  {i}. {file_path}")
    
    def add_favorite(self, file_path: str):
        """Add a file to favorites"""
        if file_path not in self.config["favorite_files"]:
            self.config["favorite_files"].append(file_path)
            self.save_config()
            print(f"Added {file_path} to favorites")
        else:
            print(f"{file_path} is already in favorites")
    
    def remove_favorite(self, file_path: str):
        """Remove a file from favorites"""
        if file_path in self.config["favorite_files"]:
            self.config["favorite_files"].remove(file_path)
            self.save_config()
            print(f"Removed {file_path} from favorites")
        else:
            print(f"{file_path} is not in favorites")

def main():
    parser = argparse.ArgumentParser(description="StackEdit Integration Tool")
    parser.add_argument("--docs-dir", default="docs", help="Documentation directory")
    parser.add_argument("--open", help="Open specific file in StackEdit")
    parser.add_argument("--create", help="Create new markdown file")
    parser.add_argument("--content", help="Content for new file")
    parser.add_argument("--list", action="store_true", help="List all markdown files")
    parser.add_argument("--recent", action="store_true", help="Show recent files")
    parser.add_argument("--favorites", action="store_true", help="Show favorite files")
    parser.add_argument("--add-favorite", help="Add file to favorites")
    parser.add_argument("--remove-favorite", help="Remove file from favorites")
    parser.add_argument("--sync", help="Sync with GitHub (optional commit message)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    
    args = parser.parse_args()
    
    # Initialize integration
    integration = StackEditIntegration(args.docs_dir)
    
    if args.no_browser:
        integration.config["auto_open_browser"] = False
        integration.save_config()
    
    if args.open:
        integration.open_in_stackedit(args.open)
    elif args.create:
        integration.create_stackedit_page(args.create, args.content or "")
    elif args.list:
        files = integration.list_markdown_files()
        print("Markdown files in docs directory:")
        for file_path in files:
            print(f"  {file_path.relative_to(integration.docs_dir)}")
    elif args.recent:
        integration.show_recent_files()
    elif args.favorites:
        integration.show_favorite_files()
    elif args.add_favorite:
        integration.add_favorite(args.add_favorite)
    elif args.remove_favorite:
        integration.remove_favorite(args.remove_favorite)
    elif args.sync is not None:
        integration.sync_with_github(args.sync)
    else:
        # Default: open StackEdit
        integration.open_in_stackedit()

if __name__ == "__main__":
    main()
