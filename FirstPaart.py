import matplotlib.pyplot as plt

INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

def compute_out_code(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    if y < ymin: code |= BOTTOM
    elif y > ymax: code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    out_code1 = compute_out_code(x1, y1, xmin, ymin, xmax, ymax)
    out_code2 = compute_out_code(x2, y2, xmin, ymin, xmax, ymax)
    accept = False

    while True:
        if not (out_code1 | out_code2):
            accept = True
            break
        elif out_code1 & out_code2:
            break
        else:
            x, y = 0, 0
            out_code_out = out_code1 if out_code1 else out_code2
            if out_code_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif out_code_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif out_code_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif out_code_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin
            if out_code_out == out_code1:
                x1, y1 = x, y
                out_code1 = compute_out_code(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                out_code2 = compute_out_code(x2, y2, xmin, ymin, xmax, ymax)

    if accept:
        return (x1, y1, x2, y2)
    else:
        return None

def visualize_clipping(segments, window, output_file):
    fig, ax = plt.subplots(figsize=(8, 8))
    xmin, ymin, xmax, ymax = window
    ax.plot([xmin, xmax, xmax, xmin, xmin],
            [ymin, ymin, ymax, ymax, ymin], color='blue', label='Clipping Window')
    for x1, y1, x2, y2 in segments:
        ax.plot([x1, x2], [y1, y2], color='gray', linestyle='--', label='Original Line' if 'Original Line' not in ax.get_legend_handles_labels()[1] else "")
    for x1, y1, x2, y2 in segments:
        clipped = cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax)
        if clipped:
            x1_c, y1_c, x2_c, y2_c = clipped
            ax.plot([x1_c, x2_c], [y1_c, y2_c], color='red', label='Clipped Line' if 'Clipped Line' not in ax.get_legend_handles_labels()[1] else "")
    ax.legend()
    ax.set_title("Cohen-Sutherland Clipping Algorithm")
    ax.set_xlim(xmin - 10, xmax + 10)
    ax.set_ylim(ymin - 10, ymax + 10)
    ax.set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.savefig(output_file, bbox_inches='tight')
    plt.close(fig)

segments = [
    (-15, -15, 15, 15),
    (0, -20, 0, 20),
    (-20, 0, 20, 0),
    (-30, -30, -10, -10)
]
window = (-10, -10, 10, 10)

visualize_clipping(segments, window, "cohen_sutherland_demo.png")
