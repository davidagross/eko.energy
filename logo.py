import math

def generate_logo(max_h_factor, output_file):
    width, height = 700, 700 
    cx, cy = width / 2, height / 2
    r = 135
    e_radius = 82
    stroke_w = 50
    num_triangles = 37
    step = 7

    colors = ["#FFE135", "#FFD700", "#FFC300", "#FFB300", "#F4D03F", "#F1C40F", "#E6C200"]
    angle_step = 360.0 / num_triangles
    base_length = 2 * r * math.sin(math.radians(angle_step / 2))
    
    min_h = 0.5 * base_length
    max_h = max_h_factor * base_length
    
    linear_heights = [min_h + (max_h - min_h) * i / (num_triangles - 1) for i in range(num_triangles)]
    
    heights = [0] * num_triangles
    idx = 0
    for h in linear_heights:
        heights[idx] = h
        idx = (idx + step) % num_triangles

    svg_elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        f'  <rect width="100%" height="100%" fill="#FDFAF0" />', 
        f'  <g id="compass-rose">'
    ]

    for i in range(num_triangles):
        center_angle_deg = i * angle_step
        center_angle = math.radians(center_angle_deg - 90)
        left_angle = math.radians(center_angle_deg - angle_step / 2 - 90)
        right_angle = math.radians(center_angle_deg + angle_step / 2 - 90)

        h = heights[i]
        color = colors[i % len(colors)]

        x1 = cx + r * math.cos(left_angle)
        y1 = cy + r * math.sin(left_angle)
        x2 = cx + r * math.cos(right_angle)
        y2 = cy + r * math.sin(right_angle)
        x3 = cx + (r + h) * math.cos(center_angle)
        y3 = cy + (r + h) * math.sin(center_angle)

        svg_elements.append(f'    <polygon points="{x1:.2f},{y1:.2f} {x2:.2f},{y2:.2f} {x3:.2f},{y3:.2f}" fill="{color}" stroke="#FDFAF0" stroke-width="1"/>')

    svg_elements.append('  </g>')
    svg_elements.append(f'  <circle cx="{cx}" cy="{cy}" r="{r + 1}" fill="none" stroke="#FFC300" stroke-width="6" opacity="0.5" />')
    svg_elements.append(f'  <circle cx="{cx}" cy="{cy}" r="{r - 18}" fill="none" stroke="#FFC300" stroke-width="2" opacity="0.25" />')

    x_end = e_radius * math.cos(math.radians(56))
    y_end = e_radius * math.sin(math.radians(56))
    
    custom_e_path = (
        f'  <path d="M -{e_radius-18},0 '
        f'L {e_radius},0 '
        f'A {e_radius},{e_radius} 0 0,0 -{e_radius},0 '
        f'A {e_radius},{e_radius} 0 0,0 {x_end:.2f},{y_end:.2f}" '
        f'fill="none" stroke="#FFB300" stroke-width="{stroke_w}" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'transform="translate({cx}, {cy}) rotate(-35)" />'
    )
    svg_elements.append(custom_e_path)
    svg_elements.append('</svg>')

    with open(output_file, "w") as f:
        f.write("\n".join(svg_elements))
