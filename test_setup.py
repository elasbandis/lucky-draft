#!/usr/bin/env python3
"""
Test script to verify the GitHub Actions setup locally
"""

import os
import subprocess
import sys

def test_dependencies():
    """Test if required dependencies are available"""
    print("🔍 Testing dependencies...")
    
    try:
        import pandas
        import numpy
        print("✅ pandas and numpy available")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        return False
    
    return True

def test_data_file():
    """Test if lottery data file exists"""
    print("📊 Testing data file...")
    
    if os.path.exists('lottery_results.csv'):
        print("✅ lottery_results.csv found")
        
        # Check file size
        size = os.path.getsize('lottery_results.csv')
        print(f"📈 Data file size: {size:,} bytes")
        
        # Count lines
        with open('lottery_results.csv', 'r') as f:
            lines = sum(1 for line in f)
        print(f"📊 Total lines: {lines:,} (including header)")
        
        return True
    else:
        print("❌ lottery_results.csv not found")
        print("💡 Run 'php csvGen.php' to generate the data file")
        return False

def test_analyzer():
    """Test the lottery analyzer script"""
    print("🎰 Testing lottery analyzer...")
    
    try:
        result = subprocess.run(['python3', 'lottery_analyzer_simple.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Lottery analyzer runs successfully")
            output_lines = len(result.stdout.split('\n'))
            print(f"📝 Generated {output_lines} lines of output")
            return True
        else:
            print(f"❌ Analyzer failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Analyzer timed out (>30 seconds)")
        return False
    except Exception as e:
        print(f"❌ Error running analyzer: {e}")
        return False

def test_html_generator():
    """Test the HTML report generator"""
    print("🌐 Testing HTML report generator...")
    
    try:
        result = subprocess.run(['python3', 'generate_html_report.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ HTML generator runs successfully")
            
            # Check if HTML file was created
            if os.path.exists('docs/index.html'):
                size = os.path.getsize('docs/index.html')
                print(f"📄 Generated HTML report: {size:,} bytes")
                return True
            else:
                print("❌ HTML file not generated")
                return False
        else:
            print(f"❌ HTML generator failed: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ HTML generator timed out (>60 seconds)")
        return False
    except Exception as e:
        print(f"❌ Error running HTML generator: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing GitHub Actions Setup")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Data File", test_data_file),
        ("Analyzer Script", test_analyzer),
        ("HTML Generator", test_html_generator),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
        
        if not success:
            print(f"⚠️  {test_name} failed - GitHub Action may not work properly")
    
    print("\n" + "=" * 50)
    print("🎯 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GitHub Action should work correctly.")
        print("🚀 Push to main branch to trigger the workflow.")
    else:
        print("⚠️  Some tests failed. Fix issues before pushing to main.")
        
    # Show next steps
    print("\n🔧 NEXT STEPS:")
    print("1. Fix any failing tests above")
    print("2. Commit and push to main branch")
    print("3. Check GitHub Actions tab for workflow status")
    print("4. Enable GitHub Pages in repository settings")
    print("5. View your report at: https://[username].github.io/[repo-name]/")

if __name__ == "__main__":
    main()
