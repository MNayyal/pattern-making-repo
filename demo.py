#!/usr/bin/env python3
"""
Demonstration script for the Advanced Pattern Generation System
Shows various capabilities and use cases
"""

import os
from pattern_generator import PatternGenerator, Measurements, PatternConstants
from pattern_modifications import (
    AdvancedPatternModifier, DesignOptions, 
    create_a_line_dress, create_fitted_dress, create_maxi_dress
)
from pattern_interface import quick_generate, batch_generate

def demo_basic_usage():
    """Demonstrate basic pattern generation"""
    print("=== Basic Pattern Generation Demo ===")
    
    # Generate a basic pattern for size 50
    print("Generating basic pattern for size 50...")
    measurements = Measurements(size=50.0)
    generator = PatternGenerator(measurements)
    generator.generate_pattern()
    generator.plot_pattern("demo_size_50.pdf", show_plot=False)
    print("✓ Generated demo_size_50.pdf")
    
    # Generate with custom measurements
    print("\nGenerating pattern with custom measurements...")
    custom_measurements = Measurements(
        size=44.0,
        waist_circumference=78.0,
        hip_circumference=100.0,
        chest_circumference=95.0,
        jacket_length=90.0
    )
    custom_generator = PatternGenerator(custom_measurements)
    custom_generator.generate_pattern()
    custom_generator.plot_pattern("demo_custom_measurements.pdf", show_plot=False)
    custom_generator.save_measurements("demo_custom_measurements.json")
    print("✓ Generated demo_custom_measurements.pdf and .json")

def demo_adjustments():
    """Demonstrate pattern adjustments"""
    print("\n=== Pattern Adjustments Demo ===")
    
    # Create base pattern
    base_generator = PatternGenerator(Measurements(size=42.0))
    modifier = AdvancedPatternModifier(base_generator)
    
    # Apply various adjustments
    adjustments = {
        'waist_adjustment': -4.0,  # 4cm smaller waist
        'hip_adjustment': 2.0,     # 2cm larger hips
        'chest_adjustment': -1.0,  # 1cm smaller chest
        'length_adjustment': 5.0   # 5cm longer
    }
    
    print("Applying adjustments: waist -4cm, hip +2cm, chest -1cm, length +5cm...")
    modifier.apply_advanced_adjustments(adjustments)
    base_generator.plot_pattern("demo_adjustments.pdf", show_plot=False)
    print("✓ Generated demo_adjustments.pdf")

def demo_design_variations():
    """Demonstrate design variations"""
    print("\n=== Design Variations Demo ===")
    
    # A-line dress
    print("Creating A-line dress...")
    a_line = create_a_line_dress(size=46.0)
    a_line.plot_pattern("demo_a_line.pdf", show_plot=False)
    print("✓ Generated demo_a_line.pdf")
    
    # Fitted dress
    print("Creating fitted dress with 3cm waist reduction...")
    fitted = create_fitted_dress(size=46.0, waist_reduction=3.0)
    fitted.plot_pattern("demo_fitted.pdf", show_plot=False)
    print("✓ Generated demo_fitted.pdf")
    
    # Maxi dress with V-neck
    print("Creating maxi dress with V-neck...")
    maxi = create_maxi_dress(size=46.0, neckline="v_neck")
    maxi.plot_pattern("demo_maxi_vneck.pdf", show_plot=False)
    print("✓ Generated demo_maxi_vneck.pdf")
    
    # Custom design variations
    print("Creating dress with multiple design options...")
    custom_measurements = Measurements(size=48.0)
    custom_generator = PatternGenerator(custom_measurements)
    custom_modifier = AdvancedPatternModifier(custom_generator)
    
    design_options = DesignOptions(
        neckline_type="boat",
        dress_style="straight",
        length_style="knee"
    )
    
    custom_modifier.apply_design_variations(design_options)
    custom_generator.plot_pattern("demo_boat_neck_straight.pdf", show_plot=False)
    print("✓ Generated demo_boat_neck_straight.pdf")

def demo_batch_generation():
    """Demonstrate batch generation for multiple sizes"""
    print("\n=== Batch Generation Demo ===")
    
    sizes = [38, 40, 42, 44, 46, 48, 50]
    print(f"Generating patterns for sizes: {sizes}")
    
    # Create output directory
    os.makedirs("demo_batch_patterns", exist_ok=True)
    
    generators = batch_generate(sizes, "demo_batch_patterns")
    print(f"✓ Generated {len(generators)} patterns in demo_batch_patterns/")

def demo_grading_chart():
    """Demonstrate grading chart creation"""
    print("\n=== Grading Chart Demo ===")
    
    base_measurements = Measurements(size=42.0)
    base_generator = PatternGenerator(base_measurements)
    modifier = AdvancedPatternModifier(base_generator)
    
    size_range = [38, 40, 42, 44, 46, 48]
    print(f"Creating grading chart for sizes: {size_range}")
    
    grading_chart = modifier.create_grading_chart(42.0, size_range)
    
    # Save grading information
    import json
    grading_data = {}
    for size, data in grading_chart.items():
        grading_data[str(size)] = {
            'size': data['measurements'].size,
            'shoulder_width': data['measurements'].shoulder_width,
            'waist_circumference': data['measurements'].waist_circumference,
            'hip_circumference': data['measurements'].hip_circumference,
            'pattern_width': data['calculated_values']['width'],
            'armhole_depth': data['calculated_values']['armhole_depth']
        }
    
    with open("demo_grading_chart.json", "w") as f:
        json.dump(grading_data, f, indent=2)
    
    print("✓ Generated demo_grading_chart.json")

def demo_fabric_layout():
    """Demonstrate fabric layout calculation"""
    print("\n=== Fabric Layout Demo ===")
    
    generator = PatternGenerator(Measurements(size=44.0))
    modifier = AdvancedPatternModifier(generator)
    
    # Calculate layout for different fabric widths
    fabric_widths = [110, 140, 150, 160]
    
    layouts = {}
    for width in fabric_widths:
        layout = modifier.export_cutting_layout(width)
        layouts[width] = layout
        print(f"Fabric width {width}cm: {layout['total_fabric_needed']:.1f}cm needed, "
              f"{layout['layout_efficiency']:.1f}% efficiency")
    
    # Save layout information
    import json
    with open("demo_fabric_layouts.json", "w") as f:
        json.dump(layouts, f, indent=2)
    
    print("✓ Generated demo_fabric_layouts.json")

def demo_quick_functions():
    """Demonstrate quick generation functions"""
    print("\n=== Quick Functions Demo ===")
    
    # Quick generate with adjustments
    print("Quick generating size 45 with waist adjustment...")
    quick_generate(size=45, waist_adj=-2, filename="demo_quick.pdf")
    print("✓ Generated demo_quick.pdf")
    
    # Multiple quick generations
    print("Quick generating multiple variations...")
    quick_generate(size=40, waist_adj=0, hip_adj=3, filename="demo_quick_hip.pdf")
    quick_generate(size=40, chest_adj=-2, filename="demo_quick_chest.pdf")
    print("✓ Generated demo_quick_hip.pdf and demo_quick_chest.pdf")

def demo_measurement_management():
    """Demonstrate measurement saving and loading"""
    print("\n=== Measurement Management Demo ===")
    
    # Create and save custom measurements
    measurements = Measurements(
        size=47.0,
        shoulder_width=47.5,
        waist_circumference=84.0,
        hip_circumference=108.0,
        chest_circumference=98.0,
        jacket_length=88.0,
        waist_from_A=41.0,
        hip_from_waist=20.0
    )
    
    generator = PatternGenerator(measurements)
    generator.generate_pattern()
    generator.save_measurements("demo_custom_profile.json")
    print("✓ Saved custom measurements to demo_custom_profile.json")
    
    # Load and use measurements
    loaded_generator = PatternGenerator.load_measurements("demo_custom_profile.json")
    loaded_generator.plot_pattern("demo_loaded_pattern.pdf", show_plot=False)
    print("✓ Loaded measurements and generated demo_loaded_pattern.pdf")

def create_summary_report():
    """Create a summary report of all demonstrations"""
    print("\n=== Creating Summary Report ===")
    
    report = """
# Pattern Generation System Demonstration Report

This report summarizes the patterns and files generated during the demonstration.

## Generated Files:

### Basic Patterns:
- demo_size_50.pdf - Basic pattern for size 50
- demo_custom_measurements.pdf - Pattern with custom measurements
- demo_custom_measurements.json - Custom measurements data

### Pattern Adjustments:
- demo_adjustments.pdf - Pattern with waist, hip, chest, and length adjustments

### Design Variations:
- demo_a_line.pdf - A-line dress design
- demo_fitted.pdf - Fitted dress with waist reduction
- demo_maxi_vneck.pdf - Maxi dress with V-neckline
- demo_boat_neck_straight.pdf - Boat neck straight dress

### Batch Generation:
- demo_batch_patterns/ - Directory containing patterns for sizes 38-50

### Analysis Files:
- demo_grading_chart.json - Size grading information
- demo_fabric_layouts.json - Fabric layout calculations

### Quick Generation:
- demo_quick.pdf - Quick generated pattern with adjustments
- demo_quick_hip.pdf - Quick pattern with hip adjustment
- demo_quick_chest.pdf - Quick pattern with chest adjustment

### Measurement Management:
- demo_custom_profile.json - Saved custom measurement profile
- demo_loaded_pattern.pdf - Pattern generated from loaded measurements

## Usage Examples:

### Command Line Usage:
```bash
# Interactive mode
python pattern_interface.py --interactive

# Generate specific size
python pattern_interface.py --size 42 --output my_pattern.pdf

# Generate with adjustments
python pattern_interface.py --size 44 --waist-adj -2 --hip-adj 1

# Load from measurements file
python pattern_interface.py --load custom_measurements.json
```

### Programmatic Usage:
```python
from pattern_generator import PatternGenerator, Measurements
from pattern_modifications import create_a_line_dress

# Basic generation
measurements = Measurements(size=42.0)
generator = PatternGenerator(measurements)
generator.generate_pattern()
generator.plot_pattern("my_pattern.pdf")

# Quick A-line dress
a_line = create_a_line_dress(size=44.0)
a_line.plot_pattern("a_line_dress.pdf")
```

## Features Demonstrated:
1. ✓ Basic pattern generation with custom sizes
2. ✓ User input system for measurements
3. ✓ Pattern adjustments (waist, hip, chest, length)
4. ✓ Design variations (A-line, fitted, maxi, different necklines)
5. ✓ Batch generation for multiple sizes
6. ✓ Grading chart creation
7. ✓ Fabric layout calculation
8. ✓ Measurement saving and loading
9. ✓ Command-line interface
10. ✓ Programmatic API

All formulas from the original script have been preserved and enhanced
with dynamic size calculations and adjustment capabilities.
"""
    
    with open("DEMO_REPORT.md", "w") as f:
        f.write(report)
    
    print("✓ Generated DEMO_REPORT.md")

def main():
    """Run all demonstrations"""
    print("🎨 Advanced Pattern Generation System - Full Demonstration")
    print("=" * 60)
    
    try:
        demo_basic_usage()
        demo_adjustments()
        demo_design_variations()
        demo_batch_generation()
        demo_grading_chart()
        demo_fabric_layout()
        demo_quick_functions()
        demo_measurement_management()
        create_summary_report()
        
        print("\n" + "=" * 60)
        print("✅ All demonstrations completed successfully!")
        print("📁 Check the generated files for results")
        print("📖 See DEMO_REPORT.md for detailed information")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()