#!/usr/bin/env python3
"""
Validation script for graph_theory_animation.py

This script validates the structure and syntax of the graph theory animation
without requiring a full Manim installation.
"""

import ast
import sys
import os

def validate_animation_file():
    """Validate the graph theory animation file"""
    animation_file = "graph_theory_animation.py"
    
    if not os.path.exists(animation_file):
        print(f"❌ Error: {animation_file} not found")
        return False
    
    try:
        # Check syntax by parsing the AST
        with open(animation_file, 'r') as f:
            content = f.read()
        
        ast.parse(content)
        print(f"✅ Syntax validation passed for {animation_file}")
        
        # Check for required classes and methods
        tree = ast.parse(content)
        
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        class_names = [cls.name for cls in classes]
        
        required_classes = ['GraphTheoryEducation']
        
        for req_class in required_classes:
            if req_class in class_names:
                print(f"✅ Found required class: {req_class}")
            else:
                print(f"❌ Missing required class: {req_class}")
                return False
        
        # Check for required methods in GraphTheoryEducation
        graph_theory_class = None
        for cls in classes:
            if cls.name == 'GraphTheoryEducation':
                graph_theory_class = cls
                break
        
        if graph_theory_class:
            methods = [node.name for node in ast.walk(graph_theory_class) 
                      if isinstance(node, ast.FunctionDef)]
            
            required_methods = [
                'construct', 'introduce_graph_theory', 'show_basic_definitions',
                'show_graph_types', 'show_traversal_algorithms', 
                'show_graph_properties', 'show_special_graphs', 'show_conclusion'
            ]
            
            for method in required_methods:
                if method in methods:
                    print(f"✅ Found required method: {method}")
                else:
                    print(f"❌ Missing required method: {method}")
                    return False
        
        # Check for imports
        imports = [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        import_names = [imp.module for imp in imports if imp.module]
        
        if 'manimlib' in import_names:
            print("✅ Found manimlib import")
        else:
            print("❌ Missing manimlib import")
            return False
        
        print(f"\n✅ All validation checks passed for {animation_file}")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in {animation_file}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error validating {animation_file}: {e}")
        return False

def check_file_structure():
    """Check if all required files are present"""
    required_files = [
        "graph_theory_animation.py",
        "graph_theory_demo.py", 
        "README_GRAPH_THEORY.md"
    ]
    
    print("📁 Checking file structure...")
    all_present = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            all_present = False
    
    return all_present

def estimate_animation_duration():
    """Estimate the total duration of the animation"""
    sections = [
        ("Introduction", 3),
        ("Basic Definitions", 4),
        ("Graph Types", 5),
        ("Traversal Algorithms", 8),
        ("Graph Properties", 4),
        ("Special Graphs", 6),
        ("Conclusion", 4)
    ]
    
    total_duration = sum(duration for _, duration in sections)
    
    print(f"\n⏱️  Estimated Animation Duration:")
    for section, duration in sections:
        print(f"   {section}: ~{duration} seconds")
    print(f"   Total: ~{total_duration} seconds ({total_duration/60:.1f} minutes)")
    
    return total_duration

def main():
    """Main validation function"""
    print("🔍 Graph Theory Animation Validation")
    print("=" * 40)
    
    # Check file structure
    if not check_file_structure():
        print("\n❌ File structure validation failed")
        return False
    
    # Validate animation file
    if not validate_animation_file():
        print("\n❌ Animation validation failed")
        return False
    
    # Estimate duration
    estimate_animation_duration()
    
    print("\n🎯 Validation Summary:")
    print("✅ All files present and valid")
    print("✅ Animation structure is correct")
    print("✅ Ready for Manim rendering")
    
    print("\n📋 Next Steps:")
    print("1. Install ManimGL: pip install manimgl")
    print("2. Run demo: python graph_theory_demo.py")
    print("3. Run animation: manimgl graph_theory_animation.py GraphTheoryEducation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)