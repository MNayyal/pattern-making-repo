#!/usr/bin/env python3
"""
Interactive Pattern Generation Interface
Provides CLI and programmatic interfaces for creating dress patterns
"""

import argparse
import sys
import json
from pathlib import Path
from pattern_generator import PatternGenerator, Measurements, PatternConstants

class PatternInterface:
    """Interactive interface for pattern generation"""
    
    def __init__(self):
        self.generator = None
        
    def get_user_measurements(self):
        """Interactively get measurements from user"""
        print("=== Dress Pattern Generator ===")
        print("Please enter your measurements (or press Enter for default values):")
        
        # Get size first
        size_input = input(f"Size (default: 40): ").strip()
        size = float(size_input) if size_input else 40.0
        
        # Get other measurements with defaults based on size
        measurements = {}
        measurements['size'] = size
        
        # Calculate smart defaults based on size
        default_shoulder = size
        default_waist = size * 2
        default_hip = size * 2.3
        default_chest = size * 2.2
        
        shoulder_input = input(f"Shoulder width in cm (default: {default_shoulder}): ").strip()
        measurements['shoulder_width'] = float(shoulder_input) if shoulder_input else default_shoulder
        
        waist_input = input(f"Waist circumference in cm (default: {default_waist}): ").strip()
        measurements['waist_circumference'] = float(waist_input) if waist_input else default_waist
        
        hip_input = input(f"Hip circumference in cm (default: {default_hip}): ").strip()
        measurements['hip_circumference'] = float(hip_input) if hip_input else default_hip
        
        chest_input = input(f"Chest circumference in cm (default: {default_chest}): ").strip()
        measurements['chest_circumference'] = float(chest_input) if chest_input else default_chest
        
        length_input = input(f"Dress length in cm (default: 85): ").strip()
        measurements['jacket_length'] = float(length_input) if length_input else 85.0
        
        waist_from_a_input = input(f"Waist position from top in cm (default: 42): ").strip()
        measurements['waist_from_A'] = float(waist_from_a_input) if waist_from_a_input else 42.0
        
        hip_from_waist_input = input(f"Hip position from waist in cm (default: 19): ").strip()
        measurements['hip_from_waist'] = float(hip_from_waist_input) if hip_from_waist_input else 19.0
        
        return Measurements(**measurements)
    
    def get_adjustments(self):
        """Get pattern adjustments from user"""
        print("\n=== Pattern Adjustments ===")
        print("Enter adjustments in cm (positive = larger, negative = smaller, 0 = no change):")
        
        adjustments = {}
        
        waist_adj = input("Waist adjustment (0): ").strip()
        if waist_adj:
            adjustments['waist_adjustment'] = float(waist_adj)
            
        hip_adj = input("Hip adjustment (0): ").strip()
        if hip_adj:
            adjustments['hip_adjustment'] = float(hip_adj)
            
        chest_adj = input("Chest adjustment (0): ").strip()
        if chest_adj:
            adjustments['chest_adjustment'] = float(chest_adj)
            
        return adjustments if adjustments else None
    
    def interactive_mode(self):
        """Run interactive pattern generation"""
        try:
            # Get measurements
            measurements = self.get_user_measurements()
            
            # Create generator
            self.generator = PatternGenerator(measurements)
            
            # Get adjustments
            adjustments = self.get_adjustments()
            
            # Generate pattern
            print("\nGenerating pattern...")
            points = self.generator.generate_pattern(adjustments)
            
            # Ask for output options
            print("\n=== Output Options ===")
            filename = input("Output filename (default: dress_pattern.pdf): ").strip()
            if not filename:
                filename = "dress_pattern.pdf"
            
            save_data = input("Save measurements to JSON? (y/n): ").strip().lower()
            
            # Generate output
            self.generator.plot_pattern(filename, show_plot=False)
            print(f"Pattern saved to {filename}")
            
            if save_data == 'y':
                json_filename = filename.replace('.pdf', '_measurements.json')
                self.generator.save_measurements(json_filename)
                print(f"Measurements saved to {json_filename}")
            
            # Display summary
            self.display_summary()
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"Error: {e}")
    
    def display_summary(self):
        """Display pattern summary"""
        if not self.generator:
            return
            
        m = self.generator.measurements
        cv = self.generator.calculated_values
        
        print("\n=== Pattern Summary ===")
        print(f"Size: {m.size}")
        print(f"Pattern Width: {cv['width']:.1f} cm")
        print(f"Pattern Length: {m.jacket_length:.1f} cm")
        print(f"Armhole Depth: {cv['armhole_depth']:.1f} cm")
        print(f"Back Width: {cv['back_width']:.1f} cm")
        print("Pattern generated successfully!")

def load_from_file(filename):
    """Load measurements from file and generate pattern"""
    try:
        generator = PatternGenerator.load_measurements(filename)
        print(f"Loaded measurements from {filename}")
        return generator
    except Exception as e:
        print(f"Error loading file {filename}: {e}")
        return None

def generate_pattern_from_size(size, adjustments=None, output_file=None):
    """Generate pattern from size with optional adjustments"""
    measurements = Measurements(size=size)
    generator = PatternGenerator(measurements)
    
    points = generator.generate_pattern(adjustments)
    
    if output_file:
        generator.plot_pattern(output_file, show_plot=False)
        print(f"Pattern saved to {output_file}")
    
    return generator

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Generate dress patterns from measurements")
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    parser.add_argument('--size', '-s', type=float, 
                       help='Generate pattern for specific size')
    parser.add_argument('--load', '-l', type=str,
                       help='Load measurements from JSON file')
    parser.add_argument('--output', '-o', type=str, default='dress_pattern.pdf',
                       help='Output filename (default: dress_pattern.pdf)')
    parser.add_argument('--waist-adj', type=float, default=0,
                       help='Waist adjustment in cm')
    parser.add_argument('--hip-adj', type=float, default=0,
                       help='Hip adjustment in cm')
    parser.add_argument('--chest-adj', type=float, default=0,
                       help='Chest adjustment in cm')
    parser.add_argument('--show', action='store_true',
                       help='Show pattern plot')
    
    args = parser.parse_args()
    
    # Prepare adjustments
    adjustments = {}
    if args.waist_adj != 0:
        adjustments['waist_adjustment'] = args.waist_adj
    if args.hip_adj != 0:
        adjustments['hip_adjustment'] = args.hip_adj
    if args.chest_adj != 0:
        adjustments['chest_adjustment'] = args.chest_adj
    
    adjustments = adjustments if adjustments else None
    
    if args.interactive:
        # Interactive mode
        interface = PatternInterface()
        interface.interactive_mode()
        
    elif args.load:
        # Load from file
        generator = load_from_file(args.load)
        if generator:
            generator.generate_pattern(adjustments)
            generator.plot_pattern(args.output, show_plot=args.show)
            print(f"Pattern generated and saved to {args.output}")
            
    elif args.size:
        # Generate from size
        generator = generate_pattern_from_size(args.size, adjustments, args.output)
        if args.show:
            generator.plot_pattern(args.output, show_plot=True)
            
    else:
        # Show help if no arguments
        parser.print_help()

if __name__ == "__main__":
    main()

# Example usage functions for programmatic access
def quick_generate(size, waist_adj=0, hip_adj=0, chest_adj=0, filename=None):
    """Quick pattern generation function"""
    adjustments = {}
    if waist_adj != 0:
        adjustments['waist_adjustment'] = waist_adj
    if hip_adj != 0:
        adjustments['hip_adjustment'] = hip_adj
    if chest_adj != 0:
        adjustments['chest_adjustment'] = chest_adj
    
    adjustments = adjustments if adjustments else None
    
    if filename is None:
        filename = f"pattern_size_{size}.pdf"
    
    return generate_pattern_from_size(size, adjustments, filename)

def batch_generate(sizes, output_dir="patterns"):
    """Generate patterns for multiple sizes"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    generators = []
    for size in sizes:
        filename = os.path.join(output_dir, f"pattern_size_{size}.pdf")
        generator = generate_pattern_from_size(size, output_file=filename)
        generators.append(generator)
        print(f"Generated pattern for size {size}")
    
    return generators