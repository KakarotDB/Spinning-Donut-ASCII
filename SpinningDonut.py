import math
import os
import time


screen_width = 80  ##dimensions of the screen
screen_height = 40

r = 1  # radii of the two circles
R = 2

A = 0
B = 0  ##angles for the spin

# Character palette (darkest to brightest)
palette = ".,-~:;=!*#$@"

while True:
    # creating a blank canvas for the frame
    output = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
    z_buffer = [[0.0 for _ in range(screen_width)] for _ in range (screen_height)]
    # looping through the angles
    theta = 0.0
    theta_spacing = 0.07
    while theta <= 2 * math.pi:
        phi_spacing = 0.02
        phi = 0.0
        while phi <= 2 * math.pi:
            # calculating the (x, y, z) co-ordinates
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
            x = (R + r * cos_phi) * cos_theta
            y = (R + r * cos_phi) * sin_theta
            z = r * sin_phi

            cosA = math.cos(A)
            sinA = math.sin(A)
            cosB = math.cos(B)
            sinB = math.sin(B)

            ##Rotating about x-axis by angle A
            x_rotated = x
            y_rotated = y * cosA - z * sinA
            z_rotated = y * sinA + z * cosA

            ##Rotating again around z axis by angle B
            x_final = x_rotated * cosB - y_rotated * sinB
            y_final = x_rotated * sinB + y_rotated * cosB
            z_final = z_rotated

            # projecting it to 2D

            K2 = 5  # distance to push donut away from viewer

            K1 = screen_width * K2 * 3 / (8 * (r + R))  # Scaling factor, based on screen width and distance
            One_over_z = 1 / (z_final + K2)

            xp = int(screen_width / 2 + K1 * One_over_z * x_final)
            yp = int(screen_height / 2 - K1 * One_over_z * y_final) ##exact pixels where it should be drawn

            ##Now we have to do shading
            ##We use surface normals to aid us in that
            nx = math.cos(theta) * math.cos(phi)
            ny = math.sin(theta) * math.cos(phi)
            nz = math.sin(phi)

            #rotating normal vectors around x-axis
            nx_rotated_x = nx
            ny_rotated_x = ny * cosA - nz * sinA
            nz_rotated_x = ny * sinA + nz * cosA

            #rotating normals around z axis
            nx_final = nx_rotated_x * cosB - ny_rotated_x * sinB
            ny_final = nx_rotated_x * sinB + ny_rotated_x * cosB
            nz_final = nz_rotated_x

            luminance = nz_final

            if 0 <= xp < screen_width and 0 <= yp < screen_height and luminance > 0:
                if One_over_z > z_buffer[yp][xp]:
                    z_buffer[yp][xp] = One_over_z

                    #Mapping luminance
                    L_index = int(luminance * 11)

                    output[yp][xp] = palette[L_index]


            phi += phi_spacing
        theta += theta_spacing

    ##Now we render the frame
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n".join("".join(row) for row in output))

    A += 0.04
    B += 0.02

    time.sleep(0.01)
