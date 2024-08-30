# ALL UNITS ARE MEASURED IN METERS

import pygame, math
from pg_utils import *

# Vector2 Setup
vector2 = Vector2()
vector2.init_vectors()

# Vector3 Setup
vector3 = Vector3()
vector3.init_vectors()

# Colors Setup
colors = Color()
colors.init_colors()

# PyGame Setup
pygame.init()

SCREEN = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN if FULLSCREEN else 0)
pygame.display.set_caption(WINDOW_NAME)
# pygame.display.set_icon(pygame.image.load(ICON_LOCATION))  # Uncomment if you have an icon

clock = pygame.time.Clock()
delta_time = 0.0

font_size = 32
big_font_size = font_size * 3 // 2
arial = pygame.font.SysFont("Arial", font_size)
arial_big = pygame.font.SysFont("Arial", big_font_size)

c = 299_792_458  # Speed of light
acceleration_factor = 10000000  # This controls the time it takes to reach speeds close to c

# SCALE
METERS_TO_PIXELS = 100 / 1


class Particle:
    def __init__(
        self,
        mass: float = 1,
        radius: float = 0.1,
        distance: float = 6,
        color: Color = colors.WHITE,
    ):
        self.position = vector2.ZERO
        self.velocity = 0
        self.mass = mass
        self.radius = radius
        self.distance = distance
        self.color = color
        self.speed = 0
        self.angle = 0
        self.joules = 0
        self.newtons = 0

    def update(self):
        # Increase speed with diminishing returns as it approaches the speed of light
        if self.velocity < c:
            increment = acceleration_factor * (1 - (self.velocity / c))
            self.velocity += increment * delta_time

        # Cap the speed to the speed of light
        if self.velocity > c:
            self.velocity = c

        # Update the angle of rotation based on the speed
        self.angle += self.velocity / self.distance * delta_time

        # Update the particle's position in meters to rotate around the center
        self.position.x = self.distance * math.cos(self.angle)
        self.position.y = self.distance * math.sin(self.angle)

        # Calculate kinetic energy in joules
        self.joules = 0.5 * self.mass * self.velocity**2

        # Calculate the centrifugal force in newtons
        self.newtons = self.mass * (self.velocity**2) / self.distance

    def draw(self):
        screen_x = int(self.position.x * METERS_TO_PIXELS) + WIDTH // 2
        screen_y = int(self.position.y * METERS_TO_PIXELS) + HEIGHT // 2
        pygame.draw.circle(
            SCREEN,
            self.color.get_tup(),
            (screen_x, screen_y),
            int(self.radius * METERS_TO_PIXELS),
        )


def draw_ui():
    fs = font_size + font_size // 2
    offset = big_font_size + big_font_size // 2

    width = 450
    height = font_size * 17 + offset

    pygame.draw.rect(
        SCREEN,
        (16, 16, 16),
        pygame.Rect(
            font_size,
            font_size,
            width,
            height,
        ),
    )

    title = Text(
        "STATS:", arial_big, colors.WHITE.get_tup(), (width // 2 + font_size, fs)
    )
    title.draw(SCREEN, title.mid_top)

    t1 = Text(
        f"FPS: {clock.get_fps():.2f}",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 1 + offset),
    )
    t1.draw(SCREEN, t1.top_left)
    t2 = Text(f"C = {c:.2e} m/s", arial, colors.WHITE.get_tup(), (fs, fs * 2 + offset))
    t2.draw(SCREEN, t2.top_left)
    t3 = Text(
        f"Mass = {p.mass} kg", arial, colors.WHITE.get_tup(), (fs, fs * 3 + offset)
    )
    t3.draw(SCREEN, t3.top_left)
    t4 = Text(
        f"Velocity: {p.velocity:.2e} m/s",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 4 + offset),
    )
    t4.draw(SCREEN, t4.top_left)
    t5 = Text(
        f"Speed of Light: {p.velocity / c * 100:.5f}%",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 5 + offset),
    )
    t5.draw(SCREEN, t5.top_left)
    t6 = Text(
        f"*100% = Very close to 100%",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 6 + offset),
    )
    t6.draw(SCREEN, t6.top_left)
    t7 = Text(
        f"Meters Travelled: {t*p.velocity:.0e}m",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 7 + offset),
    )
    t7.draw(SCREEN, t7.top_left)
    t8 = Text(
        f"Time Elapsed: {t:.3f}s",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 8 + offset),
    )
    t8.draw(SCREEN, t8.top_left)
    t9 = Text(
        f"Collision Energy: {p.joules:.2e} J",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 9 + offset),
    )
    t9.draw(SCREEN, t9.top_left)
    t10 = Text(
        f"Collision Force: {p.newtons:.2e} N",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 10 + offset),
    )
    t10.draw(SCREEN, t10.top_left)
    t11 = Text(
        f"Object Energy: {p.mass * c**2:.2e} J",
        arial,
        colors.WHITE.get_tup(),
        (fs, fs * 11 + offset),
    )
    t11.draw(SCREEN, t11.top_left)


def main():
    global delta_time, p, t

    running = True
    get_ticks_last_frame = 0.0

    p = Particle(mass=1, radius=0.1, distance=6, color=colors.WHITE)
    t = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        t += delta_time

        SCREEN.fill(colors.BLACK.get_tup())

        p.update()
        p.draw()

        draw_ui()

        pygame.display.flip()

        get_ticks_last_frame, delta_time = manage_frame_rate(
            clock, get_ticks_last_frame
        )

    pygame.quit()


if __name__ == "__main__":
    main()
