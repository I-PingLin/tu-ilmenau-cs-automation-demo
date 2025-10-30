"""
European Hypnosis Visualization

Implements the "完全秒傷付非大切プロテスタントヨーロッパイマーグリーン催眠" visualization.
Creates an interactive visualization with green-hued patterns inspired by European Protestant church architecture.
"""

import numpy as np
import pygame
import math
import random
from typing import Tuple, List
import colorsys

class EuropeanHypnosisVisualizer:
    def __init__(self, width: int = 800, height: int = 800, fps: int = 60):
        """Initialize the European Hypnosis visualizer.
        
        Args:
            width: Width of the visualization window
            height: Height of the visualization window
            fps: Frames per second for the animation
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.running = False
        self.clock = pygame.time.Clock()
        self.screen = None
        self.time = 0
        
        # Colors
        self.background_color = (5, 20, 5)  # Dark green background
        self.colors = [
            (34, 139, 34),    # Forest Green
            (0, 100, 0),      # Dark Green
            (50, 205, 50),    # Lime Green
            (107, 142, 35),   # Olive Drab
            (0, 128, 0),      # Green
            (60, 179, 113),   # Medium Sea Green
        ]
        
        # Church architecture elements
        self.church_elements = []
        self._init_church_elements()
    
    def _init_church_elements(self):
        """Initialize church architecture elements."""
        # Add stained glass windows (circular patterns)
        for _ in range(5):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            radius = random.randint(30, 80)
            segments = random.choice([6, 8, 12])  # Common in church windows
            self.church_elements.append({
                'type': 'stained_glass',
                'x': x,
                'y': y,
                'radius': radius,
                'segments': segments,
                'rotation': random.uniform(0, 2 * math.pi),
                'rotation_speed': random.uniform(0.01, 0.05) * (1 if random.random() > 0.5 else -1)
            })
        
        # Add arches (common in church architecture)
        for _ in range(3):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height - 100)
            width = random.randint(50, 150)
            height = random.randint(30, 80)
            self.church_elements.append({
                'type': 'arch',
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'thickness': random.randint(2, 5)
            })
    
    def _get_green_color(self, base_color: Tuple[int, int, int], time: float, offset: float = 0) -> Tuple[int, int, int]:
        """Generate a dynamic green color with subtle variations.
        
        Args:
            base_color: Base RGB color tuple
            time: Current time for animation
            offset: Time offset for variation
            
        Returns:
            RGB color tuple with dynamic variations
        """
        # Convert to HSV for easier manipulation of hue and saturation
        h, s, v = colorsys.rgb_to_hsv(*[c/255 for c in base_color])
        
        # Add subtle hue variation over time
        h = (h + 0.1 * math.sin((time + offset) * 0.5)) % 1.0
        
        # Slight variation in saturation
        s = min(1.0, max(0.6, s + 0.1 * math.sin(time * 0.3 + offset)))
        
        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)
    
    def _draw_stained_glass(self, element: dict, surface: pygame.Surface):
        """Draw a stained glass window element."""
        x, y = element['x'], element['y']
        radius = element['radius']
        segments = element['segments']
        rotation = element['rotation']
        
        # Draw outer circle
        pygame.draw.circle(surface, (50, 50, 50), (x, y), radius, 2)
        
        # Draw segments
        angle_step = 2 * math.pi / segments
        for i in range(segments):
            angle1 = rotation + i * angle_step
            angle2 = rotation + (i + 1) * angle_step
            
            # Calculate triangle points
            points = [
                (x, y),
                (x + radius * math.cos(angle1), y + radius * math.sin(angle1)),
                (x + radius * math.cos(angle2), y + radius * math.sin(angle2))
            ]
            
            # Draw segment with dynamic color
            color = self.colors[i % len(self.colors)]
            dynamic_color = self._get_green_color(color, self.time, i * 0.5)
            pygame.draw.polygon(surface, dynamic_color, points)
            pygame.draw.polygon(surface, (0, 0, 0), points, 1)
            
            # Add decorative elements
            if i % 2 == 0:
                inner_radius = radius * 0.7
                inner_points = [
                    (x + inner_radius * math.cos(angle1 + angle_step/2), 
                     y + inner_radius * math.sin(angle1 + angle_step/2))
                ]
                pygame.draw.circle(surface, (200, 255, 200), 
                                 (int(inner_points[0][0]), int(inner_points[0][1])), 
                                 int(radius * 0.1))
    
    def _draw_arch(self, element: dict, surface: pygame.Surface):
        """Draw a gothic arch element."""
        x, y = element['x'], element['y']
        width, height = element['width'], element['height']
        thickness = element['thickness']
        
        # Draw the arch (semi-circle on top of a rectangle)
        rect = pygame.Rect(x - width//2, y - height//2, width, height)
        pygame.draw.rect(surface, (0, 30, 0), rect, 0)
        pygame.draw.rect(surface, (0, 100, 0), rect, thickness)
        
        # Draw the arch top (semi-circle)
        pygame.draw.arc(surface, (0, 100, 0), 
                       (x - width//2, y - height, width, height*2), 
                       0, math.pi, thickness)
        
        # Add decorative elements
        for i in range(3):
            y_pos = y - height//2 + i * (height // 2)
            pygame.draw.line(surface, (0, 150, 0), 
                           (x - width//4, y_pos), 
                           (x + width//4, y_pos), 1)
    
    def _draw_hypnotic_pattern(self, surface: pygame.Surface):
        """Draw the main hypnotic pattern."""
        center_x, center_y = self.width // 2, self.height // 2
        max_radius = max(self.width, self.height) * 0.6
        
        # Draw concentric circles with dynamic colors
        for i in range(30, 0, -1):
            radius = max_radius * (i / 30) ** 0.8
            color_idx = i % len(self.colors)
            color = self._get_green_color(self.colors[color_idx], self.time + i * 0.1)
            
            # Vary the thickness for visual interest
            thickness = 2 + int(3 * math.sin(self.time * 0.5 + i * 0.2))
            
            # Draw the circle
            pygame.draw.circle(surface, color, (center_x, center_y), 
                             int(radius), thickness)
            
            # Add decorative elements at certain radii
            if i % 3 == 0:
                points = []
                for j in range(8):
                    angle = self.time * 0.2 + j * (math.pi / 4)
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    points.append((x, y))
                    
                    # Draw small circles at the points
                    pygame.draw.circle(surface, (200, 255, 200), 
                                     (int(x), int(y)), 3)
                
                # Connect the points with lines
                if len(points) > 1:
                    pygame.draw.lines(surface, (100, 200, 100), True, points, 1)
    
    def update(self, dt: float):
        """Update the visualization state.
        
        Args:
            dt: Time delta since last update in seconds
        """
        self.time += dt
        
        # Update rotation of stained glass elements
        for element in self.church_elements:
            if element['type'] == 'stained_glass':
                element['rotation'] += element['rotation_speed'] * dt * 60
    
    def draw(self, surface: pygame.Surface):
        """Draw the visualization.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Fill with dark green background
        surface.fill(self.background_color)
        
        # Draw the main hypnotic pattern
        self._draw_hypnotic_pattern(surface)
        
        # Draw church architecture elements
        for element in self.church_elements:
            if element['type'] == 'stained_glass':
                self._draw_stained_glass(element, surface)
            elif element['type'] == 'arch':
                self._draw_arch(element, surface)
        
        # Add some floating particles for a dreamy effect
        for _ in range(20):
            x = random.randint(0, self.width)
            y = int((self.time * 20 + x * 0.5) % (self.height + 20) - 10)
            size = random.randint(1, 3)
            alpha = random.randint(50, 150)
            color = (200, 255, 200, alpha)
            
            # Create a surface with per-pixel alpha
            particle = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle, color, (size, size), size)
            surface.blit(particle, (x - size, y - size))
    
    def run(self):
        """Run the visualization."""
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("完全秒傷付非大切プロテスタントヨーロッパイマーグリーン催眠")
        
        # Main loop
        self.running = True
        last_time = pygame.time.get_ticks()
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Calculate delta time
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 1000.0
            last_time = current_time
            
            # Update and draw
            self.update(dt)
            self.draw(self.screen)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        # Clean up
        pygame.quit()


def main():
    """Run the European Hypnosis visualization."""
    visualizer = EuropeanHypnosisVisualizer(width=1024, height=768, fps=60)
    visualizer.run()


if __name__ == "__main__":
    main()
