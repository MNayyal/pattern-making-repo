import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import math
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import json

@dataclass
class Measurements:
    """Class to hold all body measurements"""
    size: float = 40.0  # Base size
    shoulder_width: float = 40.0  # cm
    waist_circumference: float = 80.0  # cm (will be calculated from size if not provided)
    hip_circumference: float = 92.0  # cm (will be calculated from size if not provided)
    chest_circumference: float = 88.0  # cm (will be calculated from size if not provided)
    jacket_length: float = 85.0  # AB length
    waist_from_A: float = 42.0  # AE
    hip_from_waist: float = 19.0  # EF
    shoulder_bone: float = 12.0
    neck_depth: float = 2.0
    
    def __post_init__(self):
        """Calculate derived measurements if not provided"""
        if self.waist_circumference == 80.0 and self.size != 40.0:
            self.waist_circumference = self.size * 2  # Basic calculation
        if self.hip_circumference == 92.0 and self.size != 40.0:
            self.hip_circumference = self.size * 2.3  # Basic calculation
        if self.chest_circumference == 88.0 and self.size != 40.0:
            self.chest_circumference = self.size * 2.2  # Basic calculation
        if self.shoulder_width == 40.0 and self.size != 40.0:
            self.shoulder_width = self.size  # Direct correlation for now

@dataclass
class PatternConstants:
    """Class to hold pattern-making constants"""
    rule_add: float = 10.0
    buttons: float = 3.0
    mid_back_seam: float = 1.0
    side_seam_back: float = 1.0
    side_seam_front: float = 1.0
    back_shoulder_add: float = 3.0
    front_dart_width: float = 5.0
    shoulder_add: float = 3.0
    u_rule_constant: float = 2.0
    back_shoulder_drop: float = 4.0
    front_shoulder_drop: float = 7.0
    waist_inset: float = 2.5
    dart_depth: float = 13.0
    u_inset: float = 3.0

class PatternGenerator:
    """Main class for generating dress patterns"""
    
    def __init__(self, measurements: Measurements, constants: PatternConstants = None):
        self.measurements = measurements
        self.constants = constants or PatternConstants()
        self.points = {}
        self.calculated_values = {}
        
    def calculate_base_values(self):
        """Calculate all the derived values from measurements and constants"""
        m = self.measurements
        c = self.constants
        
        # Basic calculations
        self.calculated_values.update({
            'shoulder_length': m.shoulder_bone + c.shoulder_add,
            'armhole_depth': (m.shoulder_width + c.rule_add) / 2 + 1,
            'width': m.shoulder_width + c.rule_add + c.buttons + c.mid_back_seam + c.side_seam_back + c.side_seam_front,
            'back_width': None,  # Will be calculated next
            'armhole_value': ((m.shoulder_width + c.rule_add) / 4) + 2,
            'back_shoulder_length': m.shoulder_width / 2 + c.back_shoulder_add,
            'u_rule': c.u_rule_constant + m.shoulder_width / 4,
        })
        
        # Back width calculation
        self.calculated_values['back_width'] = (self.calculated_values['width'] - c.mid_back_seam - c.buttons) / 2 + c.mid_back_seam
        self.calculated_values['half_arm'] = self.calculated_values['armhole_value'] / 2
        
    def calculate_points(self):
        """Calculate all pattern points"""
        m = self.measurements
        c = self.constants
        cv = self.calculated_values
        
        # Base rectangle points
        A = (0, m.jacket_length)
        B = (0, 0)
        D = (cv['width'], m.jacket_length)
        C = (cv['width'], 0)
        
        # Horizontal lines
        G = (0, m.jacket_length - cv['armhole_depth'])
        E = (0, m.jacket_length - m.waist_from_A)
        F = (0, m.jacket_length - (m.waist_from_A + m.hip_from_waist))
        
        # Corresponding right points
        G_prime = (cv['width'], G[1])
        E_prime = (cv['width'], E[1])
        F_prime = (cv['width'], F[1])
        
        # Center back line
        H = (cv['back_width'], m.jacket_length)
        H_prime = (cv['back_width'], 0)
        I = (cv['back_width'], G[1])
        
        # Armhole points
        J = (cv['back_width'] - cv['half_arm'], G[1])
        K = (cv['back_width'] + cv['half_arm'], G[1])
        J_prime = (J[0], m.jacket_length)
        K_prime = (K[0], m.jacket_length)
        
        # Shoulder points
        L = (J[0], m.jacket_length - c.back_shoulder_drop)
        M = (K[0], m.jacket_length - c.front_shoulder_drop)
        L_prime = (0, L[1])
        M_prime = (0, M[1])
        N = (cv['back_shoulder_length'], L[1])
        
        # Calculate P point
        horiz_back = math.sqrt(cv['shoulder_length']**2 - c.back_shoulder_drop**2)
        P_x = N[0] - horiz_back
        P = (P_x, m.jacket_length)
        
        # Neck calculations
        neck_width = P_x - c.mid_back_seam
        front_neck_width = neck_width + c.buttons
        R_x = cv['width'] - front_neck_width
        R = (R_x, m.jacket_length)
        S_x = R_x - c.front_dart_width
        S = (S_x, m.jacket_length)
        
        # Calculate T point
        horiz_front = math.sqrt(cv['shoulder_length']**2 - c.front_shoulder_drop**2)
        T_x = S_x - horiz_front
        T = (T_x, M[1])
        
        # More points
        Q = (0, m.jacket_length - m.neck_depth)
        Q_prime = (P_x, Q[1])
        U = (cv['width'] - cv['u_rule'], G[1])
        
        # Armhole curve helper points
        km_length = cv['armhole_depth'] - c.front_shoulder_drop
        jl_length = cv['armhole_depth'] - c.back_shoulder_drop
        V_y = K[1] + (km_length / 3)
        V = (K[0], V_y)
        V_prime_y = J[1] + (jl_length / 3)
        V_prime = (J[0], V_prime_y)
        
        # Waist and dart points
        W = (cv['back_width'], E[1])
        X = (cv['back_width'] - c.waist_inset, E[1])
        X_prime = (cv['back_width'] + c.waist_inset, E[1])
        
        # Calculate dart points
        dist_x_e = abs(X[0] - E[0])
        adj_dist = (dist_x_e - 1) / 2 + 1
        Z = (adj_dist, E[1])
        Z_prime = (Z[0] - 1, Z[1])
        Z_double_prime = (Z[0] + 1.5, Z[1])
        
        bda_x = Z[0]
        z_triple_prime = (bda_x, Z[1] - c.dart_depth)
        
        # More calculated points
        AB_point = (bda_x, G[1])
        
        # Line PN intersection with vertical line at bda_x
        dx_pn = N[0] - P[0]
        dy_pn = N[1] - P[1]
        param = (bda_x - P[0]) / dx_pn if dx_pn != 0 else 0
        ac_y = P[1] + param * dy_pn
        AC = (bda_x, ac_y)
        
        # More points
        unit_dx = dx_pn / cv['shoulder_length'] if cv['shoulder_length'] != 0 else 0
        unit_dy = dy_pn / cv['shoulder_length'] if cv['shoulder_length'] != 0 else 0
        AD = (AC[0] + unit_dx * 1, AC[1] + unit_dy * 1)
        
        AE = (1, E[1])
        U_prime_prime = (U[0], U[1] - c.u_inset)
        
        Y = (U[0], E[1])
        Y_prime = (Y[0], Y[1] + 1)
        Y_double_prime = (Y[0], Y[1] - 1.5)
        Y_triple_prime = (Y[0], Y[1] + 13)
        
        # Store all points
        self.points = {
            'A': A, 'B': B, 'C': C, 'D': D, 'G': G, 'E': E, 'F': F, 
            "G'": G_prime, "E'": E_prime, "F'": F_prime,
            'H': H, "H'": H_prime, 'I': I, 'J': J, 'K': K, 
            "J'": J_prime, "K'": K_prime, 'L': L, 'M': M,
            "L'": L_prime, "M'": M_prime, 'N': N, 'P': P, 'Q': Q, 
            "Q'": Q_prime, 'R': R, 'S': S, 'T': T, 'U': U,
            'V': V, "V'": V_prime, 'W': W, 'X': X, "X'": X_prime, 
            'Z': Z, "Z'": Z_prime, "Z''": Z_double_prime,
            "z'''": z_triple_prime, 'AB': AB_point, 'AC': AC, 'AD': AD, 
            'AE': AE, 'Y': Y, "Y'": Y_prime,
            "Y''": Y_double_prime, "Y'''": Y_triple_prime, "U''": U_prime_prime
        }
        
    def apply_adjustments(self, adjustments: Dict[str, float]):
        """Apply user adjustments to the pattern"""
        if 'waist_adjustment' in adjustments:
            # Adjust waist-related points
            waist_adj = adjustments['waist_adjustment']
            # Modify X and X' points
            if 'X' in self.points:
                x_point = list(self.points['X'])
                x_point[0] += waist_adj / 4  # Distribute adjustment
                self.points['X'] = tuple(x_point)
            if "X'" in self.points:
                x_prime_point = list(self.points["X'"])
                x_prime_point[0] -= waist_adj / 4
                self.points["X'"] = tuple(x_prime_point)
                
        if 'hip_adjustment' in adjustments:
            # Adjust hip-related points
            hip_adj = adjustments['hip_adjustment']
            # This would affect the overall width at hip level
            # Implementation depends on specific requirements
            
        if 'chest_adjustment' in adjustments:
            # Adjust chest/bust related points
            chest_adj = adjustments['chest_adjustment']
            # This would affect armhole and bust dart calculations
            
    def generate_pattern(self, adjustments: Optional[Dict[str, float]] = None):
        """Generate the complete pattern"""
        self.calculate_base_values()
        self.calculate_points()
        
        if adjustments:
            self.apply_adjustments(adjustments)
            
        return self.points
        
    def plot_pattern(self, filename: str = 'dress_pattern.pdf', show_plot: bool = True):
        """Plot and save the pattern"""
        if not self.points:
            self.generate_pattern()
            
        fig, ax = plt.subplots(figsize=(12, 18))
        cv = self.calculated_values
        m = self.measurements
        
        ax.set_xlim(-5, cv['width'] + 5)
        ax.set_ylim(-5, m.jacket_length + 5)
        ax.set_aspect('equal')
        
        # Plot points
        for label, (x, y) in self.points.items():
            ax.scatter(x, y, s=100, color='red')
            ax.text(x + 0.5, y + 0.5, label, fontsize=10)
        
        # Draw lines (same as original)
        lines = [
            (self.points['A'], self.points['B']), 
            (self.points['B'], self.points['C']), 
            (self.points['C'], self.points['D']), 
            (self.points['D'], self.points['A']),
            (self.points['G'], self.points["G'"]), 
            (self.points['E'], self.points["E'"]), 
            (self.points['F'], self.points["F'"]),
            (self.points['H'], self.points["H'"]),
            (self.points['J'], self.points["J'"]), 
            (self.points['K'], self.points["K'"]),
            (self.points['N'], self.points['P']),
            (self.points['U'], self.points['R']), 
            (self.points['U'], self.points['S']),
            (self.points['M'], self.points["M'"]),
            (self.points['S'], self.points['T']),
            (self.points["Y'''"], self.points["Y'"]),
            (self.points['U'], self.points["Y'"]), 
            (self.points['U'], self.points["Y'''"]),
            (self.points['I'], self.points['X']), 
            (self.points['I'], self.points["X'"]),
            (self.points["Z'"], self.points["z'''"]), 
            (self.points["Z''"], self.points["z'''"]),
            (self.points['AD'], self.points['AB']), 
            (self.points['AE'], self.points['A']), 
            (self.points['AE'], self.points['B']),
            (self.points["U''"], self.points["Y'"]), 
            (self.points["U''"], self.points["Y'''"]),
            (self.points['AB'], self.points["Z'"]), 
            (self.points['AB'], self.points["Z''"]), 
            (self.points['AB'], self.points['AC'])
        ]
        
        for start, end in lines:
            ax.plot([start[0], end[0]], [start[1], end[1]], 'b-')
        
        # Armhole curve
        armhole_points = [self.points['T'], self.points['V'], self.points['I'], 
                         self.points["V'"], self.points['N']]
        ax.plot([p[0] for p in armhole_points], [p[1] for p in armhole_points], 
                'g--', label='Armhole curve')
        
        # Back neck curve
        P = self.points['P']
        Q = self.points['Q']
        Q_prime = self.points["Q'"]
        
        verts = [
            P,
            (P[0], (P[1] + Q_prime[1]) / 2),
            (Q[0] + (Q_prime[0] - Q[0]) / 2, Q[1]),
            Q
        ]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        path = Path(verts, codes)
        patch = PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)
        
        plt.title(f'Dress Pattern - Size {self.measurements.size}')
        plt.grid(True, alpha=0.3)
        
        # Save to PDF
        with PdfPages(filename) as pdf:
            pdf.savefig(fig)
        
        if show_plot:
            plt.show()
        else:
            plt.close()
            
    def save_measurements(self, filename: str):
        """Save measurements to JSON file"""
        data = {
            'measurements': {
                'size': self.measurements.size,
                'shoulder_width': self.measurements.shoulder_width,
                'waist_circumference': self.measurements.waist_circumference,
                'hip_circumference': self.measurements.hip_circumference,
                'chest_circumference': self.measurements.chest_circumference,
                'jacket_length': self.measurements.jacket_length,
                'waist_from_A': self.measurements.waist_from_A,
                'hip_from_waist': self.measurements.hip_from_waist,
                'shoulder_bone': self.measurements.shoulder_bone,
                'neck_depth': self.measurements.neck_depth,
            },
            'calculated_values': self.calculated_values
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    @classmethod
    def load_measurements(cls, filename: str):
        """Load measurements from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        measurements = Measurements(**data['measurements'])
        return cls(measurements)