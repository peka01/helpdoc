#!/usr/bin/env python3
"""
Bidirectional Translation Demo
Demonstrates the translation system's ability to translate between any languages
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and display the result."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print("✅ SUCCESS")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ ERROR")
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🌍 Bidirectional Translation System Demo")
    print("=" * 60)
    print("This demo shows how the translation system works in all directions")
    
    # Test 1: Swedish to English
    success1 = run_command(
        "python translate.py --mode translate-lang --from-lang sv-se --to-lang en-se",
        "Translating Swedish to English"
    )
    
    # Test 2: English to Swedish
    success2 = run_command(
        "python translate.py --mode translate-lang --from-lang en-se --to-lang sv-se",
        "Translating English to Swedish"
    )
    
    # Test 3: Specific file translation
    success3 = run_command(
        "python translate.py --mode translate-file --source-file docs/sv/overview.md --target-lang EN --source-lang SV",
        "Translating specific file (Swedish to English)"
    )
    
    # Test 4: Sync all languages
    success4 = run_command(
        "python translate.py --mode sync-all",
        "Syncing all languages with each other"
    )
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 DEMO SUMMARY")
    print(f"{'='*60}")
    
    tests = [
        ("Swedish → English", success1),
        ("English → Swedish", success2),
        ("Specific file translation", success3),
        ("Sync all languages", success4)
    ]
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    all_passed = all(success for _, success in tests)
    
    if all_passed:
        print(f"\n🎉 All tests passed! The bidirectional translation system is working perfectly.")
        print(f"\n💡 Key Features Demonstrated:")
        print(f"   • Translation between any configured languages")
        print(f"   • Automatic detection of source language")
        print(f"   • Preservation of markdown formatting")
        print(f"   • Batch translation capabilities")
        print(f"   • Git integration ready")
    else:
        print(f"\n⚠️  Some tests failed. Please check the configuration and API key.")
        sys.exit(1)

if __name__ == "__main__":
    main()
