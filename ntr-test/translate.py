#!/usr/bin/env python3
"""
Automated Translation Script for NTR Documentation
Handles translation between English and Swedish using DeepL API
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
from datetime import datetime
import logging
import tempfile
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('translation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TranslationManager:
    def __init__(self, config_path: str = "help-config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.deepl_api_key = os.getenv('DEEPL_API_KEY')
        self.deepl_api_url = "https://api-free.deepl.com/v2/translate"
        
        if not self.deepl_api_key:
            logger.warning("DEEPL_API_KEY environment variable not set. Translation will be skipped.")
    
    def load_config(self) -> Dict:
        """Load the help configuration file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {self.config_path} not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {self.config_path}")
            sys.exit(1)
    
    def get_language_configs(self) -> Dict:
        """Get language configurations from the config file."""
        app_config = self.config.get('apps', {}).get('ntr-app', {})
        return app_config.get('locales', {})
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = "EN") -> str:
        """Translate text using DeepL API."""
        try:
            response = requests.post(
                self.deepl_api_url,
                headers={
                    'Authorization': f'DeepL-Auth-Key {self.deepl_api_key}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data={
                    'text': text,
                    'source_lang': source_lang,
                    'target_lang': target_lang,
                    'preserve_formatting': '1'
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['translations'][0]['text']
            else:
                logger.error(f"DeepL API error: {response.status_code} - {response.text}")
                return text
                
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text
    
    def extract_markdown_content(self, file_path: str) -> Tuple[str, Dict]:
        """Extract content and metadata from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split frontmatter and content
            lines = content.split('\n')
            metadata = {}
            content_lines = []
            in_frontmatter = False
            
            for line in lines:
                if line.strip() == '---':
                    if not in_frontmatter:
                        in_frontmatter = True
                    else:
                        in_frontmatter = False
                    continue
                
                if in_frontmatter:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
                else:
                    content_lines.append(line)
            
            return '\n'.join(content_lines), metadata
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return "", {}
    
    def translate_markdown_file(self, source_file: str, target_file: str, 
                              source_lang: str, target_lang: str) -> bool:
        """Translate a markdown file while preserving structure."""
        logger.info(f"Translating {source_file} to {target_file}")
        
        # Check if source file exists
        if not os.path.exists(source_file):
            logger.error(f"Source file {source_file} does not exist. Skipping translation.")
            return False
        
        # Check if DeepL API key is available
        if not self.deepl_api_key:
            logger.warning("DeepL API key not available. Skipping translation to avoid overwriting content.")
            return False
        
        # Extract content and metadata
        content, metadata = self.extract_markdown_content(source_file)
        
        # Check if content was successfully extracted
        if not content:
            logger.error(f"Could not extract content from {source_file}. Skipping translation.")
            return False
        
        # Translate content
        translated_content = self.translate_text(content, target_lang, source_lang)
        
        # Check if translation actually happened (content should be different)
        if translated_content == content:
            logger.warning("Translation returned original content. Skipping to avoid overwriting.")
            return False
        
        # Reconstruct file with metadata
        output_lines = []
        if metadata:
            output_lines.append('---')
            for key, value in metadata.items():
                output_lines.append(f"{key}: {value}")
            output_lines.append('---')
            output_lines.append('')
        
        output_lines.append(translated_content)
        
        # Ensure target directory exists
        target_dir = os.path.dirname(target_file)
        os.makedirs(target_dir, exist_ok=True)
        
        # Write translated file
        try:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))
            logger.info(f"Successfully translated to {target_file}")
            return True
        except Exception as e:
            logger.error(f"Error writing translated file {target_file}: {e}")
            return False
    
    def get_changed_files(self) -> List[str]:
        """Get list of changed files from git."""
        try:
            # Check if we're in GitHub Actions environment
            if os.getenv('GITHUB_ACTIONS'):
                            # In GitHub Actions, compare with the previous commit
            result = subprocess.run(
                ['git', 'diff', '--name-status', 'HEAD~1', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            changed_files_raw = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            # Parse status and filename, only include added/modified files
            changed_files = []
            for line in changed_files_raw:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        status, filename = parts[0], parts[1]
                        # Only include files that were added or modified (not deleted)
                        if status in ['A', 'M']:
                            changed_files.append(filename)
            else:
                # For local development, get staged and unstaged changes
                # First try to get staged changes
                result = subprocess.run(
                    ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                    capture_output=True, text=True, check=True
                )
                staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
                
                # Also get unstaged changes
                result = subprocess.run(
                    ['git', 'diff', '--name-only', '--diff-filter=ACM'],
                    capture_output=True, text=True, check=True
                )
                unstaged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
                
                # Combine and deduplicate
                changed_files = list(set(staged_files + unstaged_files))
            
            # Filter for markdown files only
            markdown_files = [f for f in changed_files if f.endswith('.md')]
            
            logger.info(f"Found {len(markdown_files)} changed markdown files: {markdown_files}")
            return markdown_files
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Could not get changed files from git: {e}")
            return []
    
    def find_corresponding_files(self, changed_file: str) -> List[Tuple[str, str, str, str]]:
        """Find corresponding files in other languages for translation."""
        language_configs = self.get_language_configs()
        translations = []
        
        # Determine which language the changed file belongs to
        source_lang = None
        source_section = None
        
        # First try exact match
        for lang_code, lang_config in language_configs.items():
            for section, file_path in lang_config.get('file_paths', {}).items():
                if file_path == changed_file:
                    source_lang = lang_code
                    source_section = section
                    break
            if source_lang:
                break
        
        # If no exact match, try to infer from file path structure
        if not source_lang:
            # Extract language from path (e.g., ntr-test/docs/sv/vouchers.md -> sv)
            path_parts = changed_file.split('/')
            if len(path_parts) >= 3 and path_parts[-2] in ['sv', 'en']:
                detected_lang = path_parts[-2]
                # Map detected language to config language codes
                if detected_lang == 'sv':
                    source_lang = 'sv-se'
                elif detected_lang == 'en':
                    source_lang = 'en-se'
                
                # Try to find the section by matching the filename
                filename = path_parts[-1]
                for lang_code, lang_config in language_configs.items():
                    if lang_code == source_lang:
                        for section, file_path in lang_config.get('file_paths', {}).items():
                            if file_path.endswith(filename):
                                source_section = section
                                break
                        break
        
        if not source_lang or not source_section:
            logger.warning(f"Could not determine language for {changed_file}")
            return []
        
        logger.info(f"Detected source language: {source_lang}, section: {source_section}")
        
        # Find corresponding files in ALL other languages (bidirectional translation)
        for lang_code, lang_config in language_configs.items():
            if lang_code != source_lang:
                target_file = lang_config.get('file_paths', {}).get(source_section)
                if target_file:
                    source_lang_code = language_configs[source_lang]['code'].upper()
                    target_lang_code = lang_config['code'].upper()
                    translations.append((
                        changed_file, target_file, source_lang_code, target_lang_code
                    ))
        
        return translations
    
    def translate_changed_files(self) -> bool:
        """Translate all changed files to other languages and create pull request."""
        changed_files = self.get_changed_files()
        if not changed_files:
            logger.info("No changed files detected")
            return True
        
        logger.info(f"Found {len(changed_files)} changed files")
        
        # Create a new branch for translations
        branch_name = f"auto-translate-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        if not self.create_translation_branch(branch_name):
            logger.error("Failed to create translation branch")
            return False
        
        success = True
        translated_files = []
        
        for changed_file in changed_files:
            if not changed_file.endswith('.md'):
                continue
                
            translations = self.find_corresponding_files(changed_file)
            for source_file, target_file, source_lang, target_lang in translations:
                if self.translate_markdown_file(source_file, target_file, source_lang, target_lang):
                    translated_files.append(target_file)
                else:
                    success = False
        
        if translated_files and success:
            # Commit translated files
            if self.commit_translations(translated_files, branch_name):
                # Create pull request
                if self.create_pull_request(branch_name, translated_files):
                    logger.info(f"Pull request created for branch: {branch_name}")
                else:
                    logger.error("Failed to create pull request")
                    success = False
            else:
                logger.error("Failed to commit translations")
                success = False
        
        return success
    
    def translate_specific_file(self, source_file: str, target_lang: str, 
                              source_lang: str = "EN") -> bool:
        """Translate a specific file to a target language."""
        if not os.path.exists(source_file):
            logger.error(f"Source file {source_file} not found")
            return False
        
        # Generate target filename
        source_path = Path(source_file)
        target_file = str(source_path.parent / f"{source_path.stem}_{target_lang.lower()}{source_path.suffix}")
        
        return self.translate_markdown_file(source_file, target_file, source_lang, target_lang)
    
    def translate_between_languages(self, source_lang: str, target_lang: str) -> bool:
        """Translate all files from one language to another."""
        language_configs = self.get_language_configs()
        
        source_config = language_configs.get(source_lang)
        target_config = language_configs.get(target_lang)
        
        if not source_config or not target_config:
            logger.error(f"Language configuration not found for {source_lang} or {target_lang}")
            return False
        
        success = True
        translated_files = []
        
        for section, source_file in source_config.get('file_paths', {}).items():
            if not os.path.exists(source_file):
                logger.warning(f"Source file {source_file} not found, skipping")
                continue
            
            target_file = target_config.get('file_paths', {}).get(section)
            if target_file:
                source_code = source_config['code'].upper()
                target_code = target_config['code'].upper()
                
                if self.translate_markdown_file(source_file, target_file, source_code, target_code):
                    translated_files.append(target_file)
                else:
                    success = False
        
        if translated_files:
            logger.info(f"Successfully translated {len(translated_files)} files from {source_lang} to {target_lang}")
        
        return success
    
    def sync_all_files(self) -> bool:
        """Sync all files between all languages (bidirectional)."""
        language_configs = self.get_language_configs()
        success = True
        
        # Get all language codes
        lang_codes = list(language_configs.keys())
        
        # For each language, sync to all other languages
        for source_lang_code in lang_codes:
            source_config = language_configs.get(source_lang_code)
            if not source_config:
                logger.warning(f"Source language configuration not found for {source_lang_code}")
                continue
            
            logger.info(f"Syncing files from {source_lang_code} to other languages...")
            
            for section, source_file in source_config.get('file_paths', {}).items():
                if not os.path.exists(source_file):
                    logger.warning(f"Source file {source_file} not found, skipping")
                    continue
                
                # Find translations to all other languages
                for target_lang_code in lang_codes:
                    if target_lang_code != source_lang_code:
                        target_config = language_configs.get(target_lang_code)
                        if target_config:
                            target_file = target_config.get('file_paths', {}).get(section)
                            if target_file:
                                source_code = source_config['code'].upper()
                                target_code = target_config['code'].upper()
                                if not self.translate_markdown_file(source_file, target_file, source_code, target_code):
                                    success = False
        
        return success
        
    def run_github_actions_workflow(self) -> bool:
        """Run the translation workflow specifically for GitHub Actions."""
        logger.info("Running GitHub Actions translation workflow")
        
        # Get changed files from the last commit
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            markdown_files = [f for f in changed_files if f.endswith('.md')]
            
            logger.info(f"Changed markdown files in last commit: {markdown_files}")
            
            if not markdown_files:
                logger.info("No markdown files changed in the last commit")
                return True
                
        except subprocess.CalledProcessError:
            logger.warning("Could not get changed files from last commit")
            return False
        
        # Run bidirectional translation for all languages
        success = self.sync_all_files()
        
        if success:
            logger.info("GitHub Actions translation workflow completed successfully")
        else:
            logger.error("GitHub Actions translation workflow failed")
            
        return success
        
    def translate_only_changed_files(self) -> bool:
        """Translate only the files that were changed in the last commit."""
        logger.info("Running smart translation for changed files only")
        
        # Get changed files from the last commit - try multiple approaches
        markdown_files = []
        
        # Method 1: Try to get changes from the last commit
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-status', 'HEAD~1', 'HEAD'],
                capture_output=True, text=True, check=True
            )
            changed_files_raw = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            # Parse status and filename
            markdown_files = []
            for line in changed_files_raw:
                if line.strip() and line.endswith('.md'):
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        status, filename = parts[0], parts[1]
                        # Only include files that were added or modified (not deleted)
                        if status in ['A', 'M']:
                            markdown_files.append(filename)
                        else:
                            logger.info(f"Skipping {filename} (status: {status})")
            
            logger.info(f"Method 1 - Changed markdown files from last commit: {markdown_files}")
        except subprocess.CalledProcessError:
            logger.warning("Method 1 failed - could not get changes from last commit")
        
        # Method 2: If no files found, try to get all staged/unstaged changes
        if not markdown_files:
            try:
                # Get staged changes
                result = subprocess.run(
                    ['git', 'diff', '--cached', '--name-only'],
                    capture_output=True, text=True, check=True
                )
                staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
                
                # Get unstaged changes
                result = subprocess.run(
                    ['git', 'diff', '--name-only'],
                    capture_output=True, text=True, check=True
                )
                unstaged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
                
                # Combine and filter
                all_files = list(set(staged_files + unstaged_files))
                markdown_files = [f for f in all_files if f.endswith('.md')]
                logger.info(f"Method 2 - Found markdown files with changes: {markdown_files}")
            except subprocess.CalledProcessError:
                logger.warning("Method 2 failed - could not get staged/unstaged changes")
        
        # Method 3: If still no files, try to get files from the push event
        if not markdown_files:
            try:
                # Look for files in the docs directory that might have been changed
                result = subprocess.run(
                    ['find', 'ntr-test/docs', '-name', '*.md', '-type', 'f'],
                    capture_output=True, text=True, check=True
                )
                all_md_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
                # For now, just pick the first few files as a fallback
                markdown_files = all_md_files[:3]  # Limit to 3 files
                logger.info(f"Method 3 - Using fallback files: {markdown_files}")
            except subprocess.CalledProcessError:
                logger.warning("Method 3 failed - could not find markdown files")
        
        if not markdown_files:
            logger.info("No markdown files found to translate")
            return True
        
        # Get language configurations
        language_configs = self.get_language_configs()
        success = True
        translated_files = []
        
        # For each changed file, find its counterpart and translate
        for changed_file in markdown_files:
            # Determine which language this file belongs to
            source_lang = None
            source_section = None
            
            # First try exact match
            for lang_code, lang_config in language_configs.items():
                for section, file_path in lang_config.get('file_paths', {}).items():
                    if file_path == changed_file:
                        source_lang = lang_code
                        source_section = section
                        break
                if source_lang:
                    break
            
            # If no exact match, try to infer from file path structure
            if not source_lang:
                # Extract language from path (e.g., ntr-test/docs/sv/vouchers.md -> sv)
                path_parts = changed_file.split('/')
                if len(path_parts) >= 3 and path_parts[-2] in ['sv', 'en']:
                    detected_lang = path_parts[-2]
                    # Map detected language to config language codes
                    if detected_lang == 'sv':
                        source_lang = 'sv-se'
                    elif detected_lang == 'en':
                        source_lang = 'en-se'
                    
                    # Try to find the section by matching the filename
                    filename = path_parts[-1]
                    for lang_code, lang_config in language_configs.items():
                        if lang_code == source_lang:
                            for section, file_path in lang_config.get('file_paths', {}).items():
                                if file_path.endswith(filename):
                                    source_section = section
                                    break
                            break
            
            if not source_lang or not source_section:
                logger.warning(f"Could not determine language for {changed_file}")
                continue
            
            logger.info(f"Processing changed file: {changed_file} (language: {source_lang}, section: {source_section})")
            
            # Check if the changed file actually exists
            if not os.path.exists(changed_file):
                logger.warning(f"Changed file {changed_file} does not exist in filesystem. Skipping translation.")
                continue
            
            # Find the corresponding file in the OTHER language
            for target_lang_code, target_config in language_configs.items():
                if target_lang_code != source_lang:  # Only translate to OTHER language
                    target_file = target_config.get('file_paths', {}).get(source_section)
                    if target_file:
                        source_code = language_configs[source_lang]['code'].upper()
                        target_code = target_config['code'].upper()
                        
                        logger.info(f"Translating {changed_file} ({source_code}) → {target_file} ({target_code})")
                        
                        if self.translate_markdown_file(changed_file, target_file, source_code, target_code):
                            translated_files.append(target_file)
                        else:
                            success = False
        
        if translated_files and success:
            # Create a new branch for translations
            branch_name = f"auto-translate-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            if not self.create_translation_branch(branch_name):
                logger.error("Failed to create translation branch")
                return False
            
            # Commit translated files
            if self.commit_translations(translated_files, branch_name):
                # Create pull request
                if self.create_pull_request(branch_name, translated_files):
                    logger.info(f"Pull request created for branch: {branch_name}")
                else:
                    logger.error("Failed to create pull request")
                    success = False
            else:
                logger.error("Failed to commit translations")
                success = False
        else:
            logger.info("No files were actually translated, skipping PR creation")
        
        if success:
            logger.info("Smart translation completed successfully")
        else:
            logger.error("Smart translation failed")
            
        return success
    
    def create_translation_branch(self, branch_name: str) -> bool:
        """Create a new branch for translations."""
        try:
            # Configure git user for GitHub Actions
            if os.getenv('GITHUB_ACTIONS'):
                subprocess.run(['git', 'config', '--local', 'user.email', 'action@github.com'], check=True)
                subprocess.run(['git', 'config', '--local', 'user.name', 'GitHub Action'], check=True)
            
            # Get current branch
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, check=True)
            current_branch = result.stdout.strip()
            
            # Create and checkout new branch
            subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
            logger.info(f"Created and switched to branch: {branch_name}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create branch {branch_name}: {e}")
            return False
    
    def commit_translations(self, translated_files: List[str], branch_name: str) -> bool:
        """Commit translated files to the current branch."""
        try:
            # Add all translated files
            for file_path in translated_files:
                subprocess.run(['git', 'add', file_path], check=True)
            
            # Create commit message
            commit_message = f"Auto-translate: Update {len(translated_files)} files\n\n"
            commit_message += "Translated files:\n"
            for file_path in translated_files:
                commit_message += f"- {file_path}\n"
            commit_message += f"\nBranch: {branch_name}"
            
            # Commit
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            logger.info(f"Committed {len(translated_files)} translated files")
            
            # Push the branch to remote repository
            subprocess.run(['git', 'push', 'origin', branch_name], check=True)
            logger.info(f"Pushed branch {branch_name} to remote repository")
            
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to commit translations: {e}")
            return False
    
    def create_pull_request(self, branch_name: str, translated_files: List[str]) -> bool:
        """Create a pull request for the translation changes."""
        try:
            # Get repository info
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True, check=True)
            remote_url = result.stdout.strip()
            
            # Extract owner and repo from remote URL
            if 'github.com' in remote_url:
                # Handle both SSH and HTTPS URLs
                if remote_url.startswith('git@github.com:'):
                    repo_path = remote_url.replace('git@github.com:', '').replace('.git', '')
                else:
                    repo_path = remote_url.replace('https://github.com/', '').replace('.git', '')
                
                owner, repo = repo_path.split('/', 1)
                
                # Create PR title and body
                pr_title = f"Auto-translate: Update {len(translated_files)} documentation files"
                pr_body = f"""## Automated Translation Update

This pull request contains automated translations for the following files:

### Translated Files:
"""
                for file_path in translated_files:
                    pr_body += f"- `{file_path}`\n"
                
                pr_body += f"""
### Details:
- **Branch**: `{branch_name}`
- **Translation Provider**: DeepL API
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Review Instructions:
1. Review the translated content for accuracy
2. Check that formatting and links are preserved
3. Verify that the translations maintain the original meaning
4. Approve and merge if satisfied

### Note:
This PR was automatically generated by the translation system. Please review the changes before merging.
"""
                
                # Try to create PR using GitHub API directly
                github_token = os.getenv('GITHUB_TOKEN')
                if github_token:
                    try:
                        # Create PR using GitHub API
                        api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
                        headers = {
                            'Authorization': f'token {github_token}',
                            'Accept': 'application/vnd.github.v3+json',
                            'Content-Type': 'application/json'
                        }
                        data = {
                            'title': pr_title,
                            'body': pr_body,
                            'head': branch_name,
                            'base': 'main'
                        }
                        
                        response = requests.post(api_url, headers=headers, json=data, timeout=30)
                        if response.status_code == 201:
                            logger.info("Pull request created using GitHub API")
                            return True
                        else:
                            logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                    except Exception as e:
                        logger.error(f"Failed to create PR via GitHub API: {e}")
                
                # Fallback to GitHub CLI if available
                try:
                    subprocess.run(['gh', '--version'], capture_output=True, check=True)
                    # Create PR using GitHub CLI
                    subprocess.run([
                        'gh', 'pr', 'create',
                        '--title', pr_title,
                        '--body', pr_body,
                        '--base', 'main'
                    ], check=True)
                    logger.info("Pull request created using GitHub CLI")
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # GitHub CLI not available, provide manual instructions
                    logger.info("GitHub CLI not available. Please create PR manually:")
                    logger.info(f"Repository: {owner}/{repo}")
                    logger.info(f"Branch: {branch_name}")
                    logger.info(f"Title: {pr_title}")
                    logger.info(f"Body: {pr_body}")
                    
                    # Create a PR template file
                    pr_template = f"""# Pull Request Template

## Title
{pr_title}

## Body
{pr_body}

## Manual Steps
1. Go to: https://github.com/{owner}/{repo}/compare/main...{branch_name}
2. Click "Create pull request"
3. Copy the title and body above
4. Submit the PR

## Files Changed
{chr(10).join(f"- {f}" for f in translated_files)}
"""
                    
                    with open(f"PR_TEMPLATE_{branch_name}.md", 'w', encoding='utf-8') as f:
                        f.write(pr_template)
                    
                    logger.info(f"PR template saved to: PR_TEMPLATE_{branch_name}.md")
                    return True
            else:
                logger.warning("GitHub repository not detected. Please create PR manually.")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create pull request: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Automated Translation for NTR Documentation")
    parser.add_argument('--config', default='help-config.json', help='Configuration file path')
    parser.add_argument('--mode', choices=['git-hook', 'sync-all', 'translate-file', 'translate-lang', 'github-actions', 'smart-translate'], 
                       default='git-hook', help='Translation mode')
    parser.add_argument('--source-file', help='Source file to translate (for translate-file mode)')
    parser.add_argument('--target-lang', help='Target language code (for translate-file/translate-lang modes)')
    parser.add_argument('--source-lang', default='EN', help='Source language code (for translate-file mode)')
    parser.add_argument('--from-lang', help='Source language for translate-lang mode (e.g., en-se, sv-se)')
    parser.add_argument('--to-lang', help='Target language for translate-lang mode (e.g., en-se, sv-se)')
    
    args = parser.parse_args()
    
    manager = TranslationManager(args.config)
    
    if args.mode == 'git-hook':
        success = manager.translate_changed_files()
        if not success:
            sys.exit(1)
    elif args.mode == 'sync-all':
        success = manager.sync_all_files()
        if not success:
            sys.exit(1)
    elif args.mode == 'github-actions':
        success = manager.run_github_actions_workflow()
        if not success:
            sys.exit(1)
    elif args.mode == 'smart-translate':
        success = manager.translate_only_changed_files()
        if not success:
            sys.exit(1)
    elif args.mode == 'translate-file':
        if not args.source_file or not args.target_lang:
            logger.error("--source-file and --target-lang are required for translate-file mode")
            sys.exit(1)
        success = manager.translate_specific_file(args.source_file, args.target_lang, args.source_lang)
        if not success:
            sys.exit(1)
    elif args.mode == 'translate-lang':
        if not args.from_lang or not args.to_lang:
            logger.error("--from-lang and --to-lang are required for translate-lang mode")
            sys.exit(1)
        success = manager.translate_between_languages(args.from_lang, args.to_lang)
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()
