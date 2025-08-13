# Pattern Generation System - Usage Examples

This document provides practical examples of how to use the Advanced Dress Pattern Generation System.

## 🚀 Quick Start Examples

### 1. Basic Pattern Generation

```python
from pattern_generator import PatternGenerator, Measurements

# Generate a pattern for size 50
measurements = Measurements(size=50.0)
generator = PatternGenerator(measurements)
generator.generate_pattern()
generator.plot_pattern("size_50_dress.pdf")
```

### 2. Custom Measurements

```python
# Specify exact body measurements
custom_measurements = Measurements(
    size=44.0,
    shoulder_width=42.0,
    waist_circumference=78.0,
    hip_circumference=102.0,
    chest_circumference=94.0,
    jacket_length=88.0
)

generator = PatternGenerator(custom_measurements)
generator.generate_pattern()
generator.plot_pattern("custom_fit_dress.pdf")
```

### 3. Pattern Adjustments

```python
from pattern_modifications import AdvancedPatternModifier

# Create base pattern
generator = PatternGenerator(Measurements(size=42.0))
modifier = AdvancedPatternModifier(generator)

# Apply multiple adjustments
adjustments = {
    'waist_adjustment': -4.0,     # 4cm smaller waist
    'hip_adjustment': 2.0,        # 2cm larger hips
    'chest_adjustment': -1.0,     # 1cm smaller chest
    'length_adjustment': 10.0     # 10cm longer
}

modifier.apply_advanced_adjustments(adjustments)
generator.plot_pattern("adjusted_dress.pdf")
```

### 4. Design Variations

```python
from pattern_modifications import create_a_line_dress, create_maxi_dress, create_fitted_dress

# A-line dress
a_line = create_a_line_dress(size=46.0)
a_line.plot_pattern("a_line_dress.pdf")

# Fitted dress with waist reduction
fitted = create_fitted_dress(size=46.0, waist_reduction=3.0)
fitted.plot_pattern("fitted_dress.pdf")

# Maxi dress with V-neck
maxi = create_maxi_dress(size=46.0, neckline="v_neck")
maxi.plot_pattern("maxi_vneck_dress.pdf")
```

### 5. Custom Design Options

```python
from pattern_modifications import DesignOptions, AdvancedPatternModifier

measurements = Measurements(size=44.0)
generator = PatternGenerator(measurements)
modifier = AdvancedPatternModifier(generator)

# Create design with multiple style options
design_options = DesignOptions(
    neckline_type="boat",        # Boat neckline
    dress_style="straight",      # Straight silhouette
    length_style="knee"          # Knee length
)

modifier.apply_design_variations(design_options)
generator.plot_pattern("boat_neck_straight_dress.pdf")
```

## 💻 Command Line Examples

### Basic Generation
```bash
# Generate pattern for size 42
python3 pattern_interface.py --size 42 --output my_dress.pdf

# Generate with adjustments
python3 pattern_interface.py --size 44 --waist-adj -3 --hip-adj 2 --output custom_dress.pdf

# Interactive mode (guides you through all options)
python3 pattern_interface.py --interactive
```

### Batch Generation
```python
from pattern_interface import batch_generate

# Generate patterns for multiple sizes
sizes = [38, 40, 42, 44, 46, 48, 50]
generators = batch_generate(sizes, output_dir="size_range_patterns")
```

## 🔧 Advanced Features

### 1. Measurement Profiles

```python
# Save measurements for reuse
measurements = Measurements(
    size=45.0,
    waist_circumference=82.0,
    hip_circumference=106.0,
    chest_circumference=96.0
)

generator = PatternGenerator(measurements)
generator.generate_pattern()
generator.save_measurements("client_profile.json")

# Load saved measurements
loaded_generator = PatternGenerator.load_measurements("client_profile.json")
loaded_generator.plot_pattern("from_saved_profile.pdf")
```

### 2. Grading Chart

```python
from pattern_modifications import AdvancedPatternModifier

base_generator = PatternGenerator(Measurements(size=42.0))
modifier = AdvancedPatternModifier(base_generator)

# Create grading chart for production
size_range = [38, 40, 42, 44, 46, 48, 50]
grading_chart = modifier.create_grading_chart(42.0, size_range)

# Access grading information
for size, data in grading_chart.items():
    print(f"Size {size}: Width {data['calculated_values']['width']:.1f}cm")
```

### 3. Fabric Layout Calculation

```python
# Calculate fabric requirements
generator = PatternGenerator(Measurements(size=44.0))
modifier = AdvancedPatternModifier(generator)

# Check different fabric widths
for width in [110, 140, 150, 160]:
    layout = modifier.export_cutting_layout(width)
    print(f"Fabric width {width}cm: {layout['total_fabric_needed']:.1f}cm needed")
    print(f"Efficiency: {layout['layout_efficiency']:.1f}%")
```

## 🎨 Design Style Examples

### Classic Styles

```python
# Business dress - fitted with moderate adjustments
measurements = Measurements(size=42.0, jacket_length=95.0)
generator = PatternGenerator(measurements)
modifier = AdvancedPatternModifier(generator)

adjustments = {'waist_adjustment': -2.0}  # Slightly fitted
modifier.apply_advanced_adjustments(adjustments)

design_options = DesignOptions(
    neckline_type="round",
    dress_style="fitted",
    length_style="knee"
)
modifier.apply_design_variations(design_options)
generator.plot_pattern("business_dress.pdf")
```

```python
# Evening dress - dramatic and flowing
measurements = Measurements(size=40.0)
generator = PatternGenerator(measurements)
modifier = AdvancedPatternModifier(generator)

design_options = DesignOptions(
    neckline_type="v_neck",
    dress_style="flared",
    length_style="maxi"
)
modifier.apply_design_variations(design_options)
generator.plot_pattern("evening_dress.pdf")
```

```python
# Casual sundress - comfortable and relaxed
measurements = Measurements(size=38.0)
generator = PatternGenerator(measurements)
modifier = AdvancedPatternModifier(generator)

adjustments = {'waist_adjustment': 1.0}  # Slightly loose
modifier.apply_advanced_adjustments(adjustments)

design_options = DesignOptions(
    neckline_type="square",
    dress_style="a_line",
    length_style="midi"
)
modifier.apply_design_variations(design_options)
generator.plot_pattern("sundress.pdf")
```

## 🛠 Troubleshooting Common Scenarios

### Fit Issues

```python
# Too tight in chest area
adjustments = {'chest_adjustment': 3.0}

# Too loose in waist
adjustments = {'waist_adjustment': -2.5}

# Sleeves too narrow (affects armhole)
adjustments = {'armhole_adjustment': 1.0}

# Dress too short
adjustments = {'length_adjustment': 8.0}

# Hips too tight
adjustments = {'hip_adjustment': 4.0}
```

### Style Modifications

```python
# Convert fitted dress to A-line
design_options = DesignOptions(dress_style="a_line")

# Change neckline from round to V-neck
design_options = DesignOptions(neckline_type="v_neck")

# Make mini dress into maxi
design_options = DesignOptions(length_style="maxi")
```

## 📊 Production Examples

### Size Run Generation

```python
# Generate complete size run for production
sizes = [34, 36, 38, 40, 42, 44, 46, 48, 50, 52]

for size in sizes:
    # Base dress
    generator = PatternGenerator(Measurements(size=size))
    generator.generate_pattern()
    generator.plot_pattern(f"production/base_dress_size_{size}.pdf")
    
    # A-line variation
    a_line = create_a_line_dress(size)
    a_line.plot_pattern(f"production/a_line_dress_size_{size}.pdf")
    
    # Fitted variation
    fitted = create_fitted_dress(size, waist_reduction=2.0)
    fitted.plot_pattern(f"production/fitted_dress_size_{size}.pdf")
```

### Quality Control Checks

```python
# Verify pattern measurements
def check_pattern_quality(generator):
    cv = generator.calculated_values
    m = generator.measurements
    
    # Check proportions
    width_to_length_ratio = cv['width'] / m.jacket_length
    armhole_to_width_ratio = cv['armhole_depth'] / cv['width']
    
    print(f"Width/Length ratio: {width_to_length_ratio:.2f}")
    print(f"Armhole/Width ratio: {armhole_to_width_ratio:.2f}")
    
    # Flag potential issues
    if width_to_length_ratio > 0.8:
        print("⚠️  Pattern may be too wide for its length")
    if armhole_to_width_ratio < 0.3:
        print("⚠️  Armhole may be too shallow")

# Use quality check
generator = PatternGenerator(Measurements(size=44.0))
generator.generate_pattern()
check_pattern_quality(generator)
```

## 🔄 Integration Examples

### With External Systems

```python
# Integration with measurement database
def generate_pattern_from_database(customer_id):
    # Simulate database lookup
    measurements_data = get_customer_measurements(customer_id)
    
    measurements = Measurements(**measurements_data)
    generator = PatternGenerator(measurements)
    generator.generate_pattern()
    
    # Save with customer reference
    generator.plot_pattern(f"patterns/customer_{customer_id}_pattern.pdf")
    generator.save_measurements(f"profiles/customer_{customer_id}_measurements.json")
    
    return generator

# Batch processing
def process_order_batch(order_list):
    for order in order_list:
        size = order['size']
        style = order['style']
        adjustments = order.get('adjustments', {})
        
        if style == 'a_line':
            generator = create_a_line_dress(size, adjustments)
        elif style == 'fitted':
            generator = create_fitted_dress(size, adjustments.get('waist_reduction', 0), adjustments)
        else:
            generator = PatternGenerator(Measurements(size=size))
            if adjustments:
                modifier = AdvancedPatternModifier(generator)
                modifier.apply_advanced_adjustments(adjustments)
        
        generator.plot_pattern(f"orders/order_{order['id']}_pattern.pdf")
```

---

**These examples demonstrate the flexibility and power of the pattern generation system. Start with basic examples and gradually explore more advanced features as needed!** 🎉