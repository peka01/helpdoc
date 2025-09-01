# Test Translation Workflow

This file is used to test the automated translation system with pull request workflow.

## Test Content

This is a simple test to verify that:
1. The translation system works correctly
2. Pull requests are created properly
3. The workflow integrates with Git hooks

## Features to Test

- **DeepL Integration**: Verify API key works
- **File Mapping**: Check that files are mapped correctly
- **Branch Creation**: Ensure new branches are created
- **PR Creation**: Test pull request generation
- **Format Preservation**: Verify markdown structure is maintained

## Expected Results

When this file is committed:
1. A new branch will be created: `auto-translate-YYYYMMDD-HHMMSS`
2. This file will be translated to Swedish
3. A pull request will be created for review
4. The PR will contain the translated file for review

## Next Steps

After the PR is created:
1. Review the translated content
2. Check formatting and links
3. Approve and merge the PR
4. Verify the translation is integrated

This test demonstrates the complete workflow from translation to review to merge.
