import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check for joystick(s) and initialize them
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")
else:
    print("No joystick detected")
    pygame.quit()
    sys.exit()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Joystick Input Example")

# Colors
background_color = (0, 0, 0)  # Black
object_color = (0, 255, 0)    # Green

# Object properties (controlled by joystick)
rect_width, rect_height = 50, 50
rect_x, rect_y = width // 2, height // 2
rect_speed = 5

# Rotation and throttle controls (for joystick axes)
rotation_angle = 0
rotation_speed = 5

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle joystick button press
        if event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(0):  # Button 0 pressed
                print("Button 0 pressed")
            if joystick.get_button(1):  # Button 1 pressed
                print("Button 1 pressed")

        # Handle hat (D-pad) input
        if event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = joystick.get_hat(0)
            print(f"Hat moved: {hat_x}, {hat_y}")

    # Handle joystick axis input (e.g., for throttle, rotation, etc.)
    # Example: Axis 0 for horizontal movement, Axis 1 for vertical movement
    axis_x = joystick.get_axis(0)  # Left/Right on stick
    axis_y = joystick.get_axis(1)  # Up/Down on stick
    print(f'axis x: {axis_x} | axis y: {axis_y}')
    # throttle = joystick.get_axis(2)  # Throttle axis

    # Move the object using joystick axes
    rect_x += int(axis_x * rect_speed)
    rect_y += int(axis_y * rect_speed)

    # Rotate the object using a separate axis (e.g., Axis 3 for rotation)
    # rotation_angle += joystick.get_axis(3) * rotation_speed

    # Clear the screen
    screen.fill(background_color)

    # Create a rotated surface for the object
    object_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    object_surface.fill(object_color)
    rotated_surface = pygame.transform.rotate(object_surface, rotation_angle)
    new_rect = rotated_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))

    # Blit the rotated object onto the screen
    screen.blit(rotated_surface, new_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
