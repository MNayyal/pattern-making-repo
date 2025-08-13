"""
Advanced Pattern Modification System
Provides sophisticated pattern adjustments and design variations
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pattern_generator import PatternGenerator, Measurements, PatternConstants

@dataclass
class DesignOptions:
    """Design variations and style options"""
    sleeve_type: str = "sleeveless"  # sleeveless, short, long, cap
    neckline_type: str = "round"  # round, v_neck, square, boat
    dress_style: str = "fitted"  # fitted, a_line, straight, flared
    dart_style: str = "standard"  # standard, princess, bust_dart, french
    length_style: str = "midi"  # mini, midi, maxi, knee
    back_closure: str = "zipper"  # zipper, buttons, lace_up

class AdvancedPatternModifier:
    """Advanced pattern modification and design variation system"""
    
    def __init__(self, generator: PatternGenerator):
        self.generator = generator
        self.original_points = None
        
    def apply_advanced_adjustments(self, adjustments: Dict[str, float]):
        """Apply sophisticated pattern adjustments"""
        if not self.generator.points:
            self.generator.generate_pattern()
        
        # Store original points for reference
        if self.original_points is None:
            self.original_points = self.generator.points.copy()
        
        # Apply waist adjustments
        if 'waist_adjustment' in adjustments:
            self._adjust_waist(adjustments['waist_adjustment'])
        
        # Apply hip adjustments
        if 'hip_adjustment' in adjustments:
            self._adjust_hip(adjustments['hip_adjustment'])
        
        # Apply bust/chest adjustments
        if 'chest_adjustment' in adjustments:
            self._adjust_chest(adjustments['chest_adjustment'])
        
        # Apply shoulder adjustments
        if 'shoulder_adjustment' in adjustments:
            self._adjust_shoulder(adjustments['shoulder_adjustment'])
        
        # Apply length adjustments
        if 'length_adjustment' in adjustments:
            self._adjust_length(adjustments['length_adjustment'])
        
        # Apply armhole adjustments
        if 'armhole_adjustment' in adjustments:
            self._adjust_armhole(adjustments['armhole_adjustment'])
            
    def _adjust_waist(self, adjustment: float):
        """Adjust waist circumference"""
        # Distribute adjustment across multiple points
        half_adj = adjustment / 2
        quarter_adj = adjustment / 4
        
        # Adjust center back waist points
        if 'X' in self.generator.points:
            x, y = self.generator.points['X']
            self.generator.points['X'] = (x - quarter_adj, y)
        
        if 'X\'' in self.generator.points:
            x, y = self.generator.points['X\'']
            self.generator.points['X\''] = (x + quarter_adj, y)
        
        # Adjust side seam points
        if 'Z' in self.generator.points:
            x, y = self.generator.points['Z']
            self.generator.points['Z'] = (x + quarter_adj, y)
        
        # Adjust dart width if needed
        if abs(adjustment) > 2:  # Significant adjustment
            dart_adj = adjustment * 0.3  # 30% through dart modification
            self._adjust_dart_width(dart_adj)
    
    def _adjust_hip(self, adjustment: float):
        """Adjust hip circumference"""
        # Hip adjustments affect the lower portion of the pattern
        hip_level = self.generator.points['F'][1] if 'F' in self.generator.points else 0
        
        # Adjust side seams at hip level
        quarter_adj = adjustment / 4
        
        # Find and adjust points at hip level
        for point_name, (x, y) in self.generator.points.items():
            if abs(y - hip_level) < 2:  # Points near hip level
                if x > self.generator.calculated_values['width'] / 2:  # Right side
                    self.generator.points[point_name] = (x + quarter_adj, y)
                elif x > 0:  # Left side (not center back)
                    self.generator.points[point_name] = (x - quarter_adj, y)
    
    def _adjust_chest(self, adjustment: float):
        """Adjust chest/bust circumference"""
        # Chest adjustments primarily affect armhole and bust dart areas
        quarter_adj = adjustment / 4
        
        # Adjust armhole width
        if 'K' in self.generator.points:
            x, y = self.generator.points['K']
            self.generator.points['K'] = (x + quarter_adj, y)
            # Update corresponding points
            self.generator.points['K\''] = (x + quarter_adj, self.generator.points['K\''][1])
        
        if 'J' in self.generator.points:
            x, y = self.generator.points['J']
            self.generator.points['J'] = (x - quarter_adj, y)
            self.generator.points['J\''] = (x - quarter_adj, self.generator.points['J\''][1])
        
        # Adjust bust dart if significant change
        if abs(adjustment) > 3:
            bust_dart_adj = adjustment * 0.4
            self._adjust_bust_dart(bust_dart_adj)
    
    def _adjust_shoulder(self, adjustment: float):
        """Adjust shoulder width and slope"""
        # Adjust shoulder points
        half_adj = adjustment / 2
        
        if 'N' in self.generator.points:
            x, y = self.generator.points['N']
            self.generator.points['N'] = (x + half_adj, y)
        
        if 'T' in self.generator.points:
            x, y = self.generator.points['T']
            self.generator.points['T'] = (x - half_adj, y)
        
        # Recalculate dependent points
        self._recalculate_shoulder_dependent_points()
    
    def _adjust_length(self, adjustment: float):
        """Adjust overall dress length"""
        # Move all points up or down proportionally
        for point_name, (x, y) in self.generator.points.items():
            if point_name in ['A', 'D', 'H', 'J\'', 'K\'', 'P', 'Q', 'Q\'', 'R', 'S']:
                # Top edge points
                continue
            else:
                # Adjust other points proportionally
                new_y = y + adjustment
                self.generator.points[point_name] = (x, new_y)
        
        # Update measurements
        self.generator.measurements.jacket_length += adjustment
    
    def _adjust_armhole(self, adjustment: float):
        """Adjust armhole depth and shape"""
        # Adjust armhole depth
        current_depth = self.generator.calculated_values['armhole_depth']
        new_depth = current_depth + adjustment
        self.generator.calculated_values['armhole_depth'] = new_depth
        
        # Recalculate armhole points
        self._recalculate_armhole_points()
    
    def _adjust_dart_width(self, adjustment: float):
        """Adjust dart width"""
        if "Z'" in self.generator.points and "z'''" in self.generator.points:
            z_prime_x, z_prime_y = self.generator.points["Z'"]
            z_double_prime_x, z_double_prime_y = self.generator.points["Z''"]
            
            # Adjust dart points
            self.generator.points["Z'"] = (z_prime_x - adjustment/2, z_prime_y)
            self.generator.points["Z''"] = (z_double_prime_x + adjustment/2, z_double_prime_y)
    
    def _adjust_bust_dart(self, adjustment: float):
        """Adjust bust dart size and position"""
        # This is a simplified bust dart adjustment
        # In reality, this would involve complex calculations
        if 'S' in self.generator.points and 'R' in self.generator.points:
            s_x, s_y = self.generator.points['S']
            r_x, r_y = self.generator.points['R']
            
            # Adjust dart width
            dart_width_change = adjustment * 0.5
            self.generator.points['S'] = (s_x - dart_width_change, s_y)
    
    def _recalculate_shoulder_dependent_points(self):
        """Recalculate points that depend on shoulder adjustments"""
        # This would involve recalculating P, armhole curves, etc.
        # Simplified version
        pass
    
    def _recalculate_armhole_points(self):
        """Recalculate armhole-related points"""
        # Recalculate based on new armhole depth
        m = self.generator.measurements
        cv = self.generator.calculated_values
        
        # Update G points (armhole line)
        new_g_y = m.jacket_length - cv['armhole_depth']
        self.generator.points['G'] = (0, new_g_y)
        self.generator.points['G\''] = (cv['width'], new_g_y)
        self.generator.points['I'] = (cv['back_width'], new_g_y)
    
    def apply_design_variations(self, design_options: DesignOptions):
        """Apply design variations to the pattern"""
        if design_options.neckline_type != "round":
            self._modify_neckline(design_options.neckline_type)
        
        if design_options.dress_style != "fitted":
            self._modify_silhouette(design_options.dress_style)
        
        if design_options.dart_style != "standard":
            self._modify_dart_style(design_options.dart_style)
        
        if design_options.length_style != "midi":
            self._modify_length_style(design_options.length_style)
    
    def _modify_neckline(self, neckline_type: str):
        """Modify neckline shape"""
        if neckline_type == "v_neck":
            # Lower the front neckline
            if 'R' in self.generator.points:
                x, y = self.generator.points['R']
                self.generator.points['R'] = (x, y - 3)  # 3cm deeper
        
        elif neckline_type == "square":
            # Create square neckline
            if 'Q' in self.generator.points and 'R' in self.generator.points:
                q_x, q_y = self.generator.points['Q']
                r_x, r_y = self.generator.points['R']
                # Make front and back the same depth
                self.generator.points['R'] = (r_x, q_y)
        
        elif neckline_type == "boat":
            # Wider, shallower neckline
            if 'Q' in self.generator.points and 'R' in self.generator.points:
                q_x, q_y = self.generator.points['Q']
                r_x, r_y = self.generator.points['R']
                # Raise neckline and widen
                self.generator.points['Q'] = (q_x, q_y + 1)
                self.generator.points['R'] = (r_x - 2, r_y + 1)
    
    def _modify_silhouette(self, dress_style: str):
        """Modify overall dress silhouette"""
        if dress_style == "a_line":
            # Gradually increase width towards hem
            hem_increase = 8  # 8cm total increase at hem
            self._apply_a_line_flare(hem_increase)
        
        elif dress_style == "straight":
            # Remove waist shaping
            self._remove_waist_shaping()
        
        elif dress_style == "flared":
            # Significant flare from waist down
            flare_increase = 15  # 15cm total increase
            self._apply_flare_from_waist(flare_increase)
    
    def _modify_dart_style(self, dart_style: str):
        """Modify dart style and placement"""
        if dart_style == "princess":
            # Convert to princess seams
            self._convert_to_princess_seams()
        
        elif dart_style == "french":
            # Move dart to side seam
            self._convert_to_french_dart()
    
    def _modify_length_style(self, length_style: str):
        """Modify dress length according to style"""
        current_length = self.generator.measurements.jacket_length
        
        if length_style == "mini":
            new_length = 60  # Mini dress length
        elif length_style == "knee":
            new_length = 70  # Knee length
        elif length_style == "midi":
            new_length = 85  # Midi length (current default)
        elif length_style == "maxi":
            new_length = 120  # Maxi length
        else:
            return
        
        length_adjustment = new_length - current_length
        self._adjust_length(length_adjustment)
    
    def _apply_a_line_flare(self, hem_increase: float):
        """Apply A-line flare to the pattern"""
        quarter_increase = hem_increase / 4
        
        # Adjust bottom points
        if 'C' in self.generator.points:
            x, y = self.generator.points['C']
            self.generator.points['C'] = (x + quarter_increase, y)
        
        if 'B' in self.generator.points:
            x, y = self.generator.points['B']
            self.generator.points['B'] = (x - quarter_increase, y)
    
    def _remove_waist_shaping(self):
        """Remove waist shaping for straight silhouette"""
        # Make waist points align with bust/hip
        if 'X' in self.generator.points and 'I' in self.generator.points:
            i_x, i_y = self.generator.points['I']
            self.generator.points['X'] = (i_x, self.generator.points['X'][1])
        
        if "X'" in self.generator.points:
            self.generator.points["X'"] = (i_x, self.generator.points["X'"][1])
    
    def _apply_flare_from_waist(self, flare_increase: float):
        """Apply flare from waist down"""
        waist_y = self.generator.points['E'][1] if 'E' in self.generator.points else 0
        quarter_increase = flare_increase / 4
        
        # Adjust points below waist
        for point_name, (x, y) in self.generator.points.items():
            if y < waist_y:  # Below waist
                if x > self.generator.calculated_values['width'] / 2:  # Right side
                    # Gradually increase flare towards hem
                    flare_factor = (waist_y - y) / waist_y
                    adjustment = quarter_increase * flare_factor
                    self.generator.points[point_name] = (x + adjustment, y)
                elif x > 0:  # Left side
                    flare_factor = (waist_y - y) / waist_y
                    adjustment = quarter_increase * flare_factor
                    self.generator.points[point_name] = (x - adjustment, y)
    
    def _convert_to_princess_seams(self):
        """Convert darts to princess seams"""
        # This is a complex operation that would require significant
        # pattern manipulation. Simplified implementation here.
        pass
    
    def _convert_to_french_dart(self):
        """Convert waist dart to French (side seam) dart"""
        # Move dart to side seam
        # Simplified implementation
        pass
    
    def create_grading_chart(self, base_size: float, size_range: List[float]) -> Dict[float, Dict]:
        """Create a grading chart for multiple sizes"""
        grading_chart = {}
        
        # Generate base pattern
        base_measurements = Measurements(size=base_size)
        base_generator = PatternGenerator(base_measurements)
        base_generator.generate_pattern()
        
        grading_chart[base_size] = {
            'measurements': base_measurements,
            'calculated_values': base_generator.calculated_values.copy()
        }
        
        # Generate patterns for other sizes
        for size in size_range:
            if size != base_size:
                size_measurements = Measurements(size=size)
                size_generator = PatternGenerator(size_measurements)
                size_generator.generate_pattern()
                
                grading_chart[size] = {
                    'measurements': size_measurements,
                    'calculated_values': size_generator.calculated_values.copy(),
                    'size_difference': size - base_size
                }
        
        return grading_chart
    
    def export_cutting_layout(self, fabric_width: float = 150.0) -> Dict:
        """Generate cutting layout for fabric"""
        if not self.generator.points:
            self.generator.generate_pattern()
        
        # Calculate pattern piece dimensions
        pattern_width = self.generator.calculated_values['width']
        pattern_length = self.generator.measurements.jacket_length
        
        # Simple layout calculation
        pieces_per_width = int(fabric_width // pattern_width)
        total_fabric_needed = pattern_length * (2 / pieces_per_width)  # Front and back pieces
        
        layout = {
            'fabric_width': fabric_width,
            'pattern_width': pattern_width,
            'pattern_length': pattern_length,
            'pieces_per_width': pieces_per_width,
            'total_fabric_needed': total_fabric_needed,
            'layout_efficiency': (pattern_width * pieces_per_width) / fabric_width * 100
        }
        
        return layout

# Convenience functions for common modifications
def create_a_line_dress(size: float, adjustments: Optional[Dict] = None) -> PatternGenerator:
    """Create an A-line dress pattern"""
    measurements = Measurements(size=size)
    generator = PatternGenerator(measurements)
    modifier = AdvancedPatternModifier(generator)
    
    # Apply base adjustments if provided
    if adjustments:
        modifier.apply_advanced_adjustments(adjustments)
    
    # Apply A-line design
    design_options = DesignOptions(dress_style="a_line")
    modifier.apply_design_variations(design_options)
    
    return generator

def create_fitted_dress(size: float, waist_reduction: float = 0, adjustments: Optional[Dict] = None) -> PatternGenerator:
    """Create a fitted dress pattern"""
    measurements = Measurements(size=size)
    generator = PatternGenerator(measurements)
    modifier = AdvancedPatternModifier(generator)
    
    # Apply waist reduction for fitted look
    fit_adjustments = {'waist_adjustment': -waist_reduction}
    if adjustments:
        fit_adjustments.update(adjustments)
    
    modifier.apply_advanced_adjustments(fit_adjustments)
    
    return generator

def create_maxi_dress(size: float, neckline: str = "round", adjustments: Optional[Dict] = None) -> PatternGenerator:
    """Create a maxi dress pattern"""
    measurements = Measurements(size=size)
    generator = PatternGenerator(measurements)
    modifier = AdvancedPatternModifier(generator)
    
    # Apply base adjustments if provided
    if adjustments:
        modifier.apply_advanced_adjustments(adjustments)
    
    # Apply maxi design
    design_options = DesignOptions(length_style="maxi", neckline_type=neckline)
    modifier.apply_design_variations(design_options)
    
    return generator