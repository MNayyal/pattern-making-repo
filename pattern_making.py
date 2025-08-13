import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import math

# Parameters based on instructions (for size 40 example)
shoulder_width = 40.0  # cm
rule_add = 10.0
buttons = 3.0
mid_back_seam = 1.0
side_seam_back = 1.0
side_seam_front = 1.0
jacket_length = 85.0  # AB length
armhole_depth = (shoulder_width + rule_add) / 2 + 1  # AG
waist_from_A = 42.0  # AE
hip_from_waist = 19.0  # EF
back_shoulder_add = 3.0
front_dart_width = 5.0  # fixed
shoulder_bone = 12.0
shoulder_add = 3.0
shoulder_length = shoulder_bone + shoulder_add  # 15
neck_depth = 2.0
u_rule_constant = 2.0
back_shoulder_drop = 4.0
front_shoulder_drop = 7.0
waist_inset = 2.5  # WX = 2.5
dart_depth = 13.0  # for Y''', Z'''
u_inset = 3.0  # U to U'' = 3cm

# Calculated values
width = shoulder_width + rule_add + buttons + mid_back_seam + side_seam_back + side_seam_front  # 56
back_width = (width - mid_back_seam - buttons) / 2 + mid_back_seam  # 27
armhole_value = ((shoulder_width + rule_add) / 4) + 2  # 14.5
half_arm = armhole_value / 2  # 7.25
back_shoulder_length = shoulder_width / 2 + back_shoulder_add  # 23
u_rule = u_rule_constant + shoulder_width / 4  # 12

# Coordinate system: x right, y up, A at (0, jacket_length), B at (0,0)
A = (0, jacket_length)
B = (0, 0)
D = (width, jacket_length)
C = (width, 0)
G = (0, jacket_length - armhole_depth)
E = (0, jacket_length - waist_from_A)
F = (0, jacket_length - (waist_from_A + hip_from_waist))
G_prime = (width, G[1])
E_prime = (width, E[1])
F_prime = (width, F[1])
H = (back_width, jacket_length)
H_prime = (back_width, 0)
I = (back_width, G[1])
J = (back_width - half_arm, G[1])
K = (back_width + half_arm, G[1])
J_prime = (J[0], jacket_length)
K_prime = (K[0], jacket_length)
L = (J[0], jacket_length - back_shoulder_drop)
M = (K[0], jacket_length - front_shoulder_drop)
L_prime = (0, L[1])
M_prime = (0, M[1])
N = (back_shoulder_length, L[1])
horiz_back = math.sqrt(shoulder_length**2 - back_shoulder_drop**2)
P_x = N[0] - horiz_back
P = (P_x, jacket_length)
neck_width = P_x - mid_back_seam  # PA -1
front_neck_width = neck_width + buttons
R_x = width - front_neck_width
R = (R_x, jacket_length)
S_x = R_x - front_dart_width
S = (S_x, jacket_length)
horiz_front = math.sqrt(shoulder_length**2 - front_shoulder_drop**2)
T_x = S_x - horiz_front  # choose left
T = (T_x, M[1])
Q = (0, jacket_length - neck_depth)
Q_prime = (P_x, Q[1])
U = (width - u_rule, G[1])
km_length = armhole_depth - front_shoulder_drop
jl_length = armhole_depth - back_shoulder_drop
V_y = K[1] + (km_length / 3)
V = (K[0], V_y)
V_prime_y = J[1] + (jl_length / 3)
V_prime = (J[0], V_prime_y)
W = (back_width, E[1])
X = (back_width - waist_inset, E[1])
X_prime = (back_width + waist_inset, E[1])
dist_x_e = abs(X[0] - E[0])
adj_dist = (dist_x_e - 1) / 2 + 1
Z = (adj_dist, E[1])  # from E right
Z_prime = (Z[0] - 1, Z[1])  # ZZ' =1 left
Z_double_prime = (Z[0] + 1.5, Z[1])  # ZZ'' =1.5 right
bda_x = Z[0]  # vertical line at x = Z[0]
z_triple_prime = (bda_x, Z[1] - dart_depth)  # down 13cm
# AB_point = GG' cross BDA
AB_point = (bda_x, G[1])
# AC = PN cross BDA
# Line PN: from P to N
dx_pn = N[0] - P[0]
dy_pn = N[1] - P[1]
param = (bda_x - P[0]) / dx_pn
ac_y = P[1] + param * dy_pn
AC = (bda_x, ac_y)
# AD_point on PN, AC to AD =1cm
unit_dx = dx_pn / shoulder_length
unit_dy = dy_pn / shoulder_length
AD = (AC[0] + unit_dx * 1, AC[1] + unit_dy * 1)  # direction to N
# AE on EE', E to AE =1cm right
AE = (1, E[1])
# UU' from U to BC perpendicular, BC horizontal, so vertical down from U to y=0
U_prime_prime = (U[0], U[1] - u_inset)  # down 3cm from U
# Y where UU' crosses EE'
Y = (U[0], E[1])
Y_prime = (Y[0], Y[1] + 1)  # YY' =1cm up (towards top)
Y_double_prime = (Y[0], Y[1] - 1.5)  # YY'' =1.5cm down
Y_triple_prime = (Y[0], Y[1] + 13)  # YY''' =13cm up? Wait, on YU' , YU' is from Y to U' at 0, but U' at (U[0],0), so down.


# The instructions "assign point Y''' on the line YU' to make the ditance YY''' be 13cm " 
# YU' is from Y (U[0], E[1]) to U' (U[0],0), down decreasing y.
# So YY''' =13, probably down, y = E[1] -13
# Y_triple_prime = (Y[0], Y[1] - 13)
# # Then z''' on BDA, ZZ''' =13, probably down, z_triple_prime = (bda_x, Z[1] -13)
# yes.

# Now, to plot
fig, ax = plt.subplots(figsize=(12, 18))
ax.set_xlim(-5, width + 5)
ax.set_ylim(-5, jacket_length + 5)
ax.set_aspect('equal')

# Points dict for labeling
points = {
    'A': A, 'B': B, 'C': C, 'D': D, 'G': G, 'E': E, 'F': F, 'G\'': G_prime, 'E\'': E_prime, 'F\'': F_prime,
    'H': H, 'H\'': H_prime, 'I': I, 'J': J, 'K': K, 'J\'': J_prime, 'K\'': K_prime, 'L': L, 'M': M,
    'L\'': L_prime, 'M\'': M_prime, 'N': N, 'P': P, 'Q': Q, 'Q\'': Q_prime, 'R': R, 'S': S, 'T': T, 'U': U,
    'V': V, 'V\'': V_prime, 'W': W, 'X': X, 'X\'': X_prime, 'Z': Z, 'Z\'': Z_prime, 'Z\'\'': Z_double_prime,
    'z\'\'\'': z_triple_prime, 'AB': AB_point, 'AC': AC, 'AD': AD, 'AE': AE, 'Y': Y, 'Y\'': Y_prime,
    'Y\'\'': Y_double_prime, 'Y\'\'\'': Y_triple_prime, 'U\'\'': U_prime_prime
}

# Plot points
for label, (x, y) in points.items():
    ax.scatter(x, y, s=100, color='red')
    ax.text(x + 0.5, y + 0.5, label, fontsize=12)

# Draw straight lines

lines = [
    (A, B), (B, C), (C, D), (D, A),  # rectangle ABCD
    (G, G_prime), (E, E_prime), (F, F_prime),  # GG', EE', FF'
    (H, H_prime),  # HH'
    (J, J_prime), (K, K_prime),  # JJ', KK'
    (N, P),  # NP
    (U, R), (U, S),  # UR, US
    (M, M_prime),  # MM'
    (S, T),  # ST
    # Add other straight lines
    (Y_triple_prime, Y_double_prime), (Y_triple_prime, Y_prime), (U, Y_prime), (U, Y_double_prime),
    # Slightly curved from I to X, I to X', but straight for now
    (I, X), (I, X_prime),
    (Z_prime, z_triple_prime), (Z_double_prime, z_triple_prime),
    (AD, AB_point), (AE, A), (AE, B),  # (AE)A ? A is point, perhaps (AE, A[0] or something, but A is (0,jacket_length), AE (1, E[1])
    # Perhaps lines from AE to point A and to B
    (AE, A), (AE, B),
    (U_prime_prime, Y_prime), (U_prime_prime, Y_double_prime),
    (AB_point, Z_prime), (AB_point, Z_double_prime), (AB_point, AC)
]

for start, end in lines:
    ax.plot([start[0], end[0]], [start[1], end[1]], 'b-')

# Curved lines
# Armhole curve TVIV'N
armhole_points = [T, V, I, V_prime, N]
ax.plot([p[0] for p in armhole_points], [p[1] for p in armhole_points], 'g--', label='Armhole curve (approx straight)')

# To make curved, we can use simple interpolation, but for better, use Bezier or skip for now

# Back neck curve Q to P, touching QQ' and PQ'
# Bezier curve
verts = [
    P,  # start
    (P[0], (P[1] + Q_prime[1]) / 2),  # control1 near vertical
    (Q[0] + (Q_prime[0] - Q[0]) / 2, Q[1]),  # control2 near horizontal
    Q   # end
]
codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
path = Path(verts, codes)
patch = PathPatch(path, facecolor='none', lw=2)
ax.add_patch(patch)

# Save to PDF
with PdfPages('jacket_pattern.pdf') as pdf:
    pdf.savefig(fig)

plt.show()