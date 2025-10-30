""
Tests for the European Hypnosis visualization.
"""
import unittest
import pygame
import sys
import os
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import our module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cs_capstone.european_hypnosis import EuropeanHypnosisVisualizer

class TestEuropeanHypnosis(unittest.TestCase):
    """Test cases for the European Hypnosis visualization."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Initialize pygame with a dummy display for testing
        pygame.init()
        pygame.display.set_mode((1, 1))
        
        # Create a visualizer instance for testing
        self.visualizer = EuropeanHypnosisVisualizer(width=400, height=300, fps=30)
    
    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()
    
    def test_initialization(self):
        """Test that the visualizer initializes correctly."""
        self.assertEqual(self.visualizer.width, 400)
        self.assertEqual(self.visualizer.height, 300)
        self.assertEqual(self.visualizer.fps, 30)
        self.assertFalse(self.visualizer.running)
        self.assertEqual(len(self.visualizer.colors), 6)
        self.assertGreater(len(self.visualizer.church_elements), 0)
    
    def test_color_generation(self):
        """Test that color generation works as expected."""
        base_color = (0, 128, 0)  # Green
        color = self.visualizer._get_green_color(base_color, 0)
        
        # Should return an RGB tuple with 3 values
        self.assertEqual(len(color), 3)
        self.assertIsInstance(color[0], int)
        self.assertIsInstance(color[1], int)
        self.assertIsInstance(color[2], int)
        
        # Values should be in 0-255 range
        self.assertTrue(0 <= color[0] <= 255)
        self.assertTrue(0 <= color[1] <= 255)
        self.assertTrue(0 <= color[2] <= 255)
    
    def test_update(self):
        """Test that the update method updates the state correctly."""
        # Get initial rotation of the first stained glass element
        initial_rotation = None
        for element in self.visualizer.church_elements:
            if element['type'] == 'stained_glass':
                initial_rotation = element['rotation']
                break
        
        # Update the visualizer
        self.visualizer.update(1.0)  # 1 second of time passed
        
        # Check that the rotation has been updated
        updated = False
        for element in self.visualizer.church_elements:
            if element['type'] == 'stained_glass':
                if element['rotation'] != initial_rotation:
                    updated = True
                    break
        
        self.assertTrue(updated, "Rotation should have been updated")
    
    @patch('pygame.draw.circle')
    @patch('pygame.draw.polygon')
    @patch('pygame.draw.rect')
    @patch('pygame.draw.arc')
    @patch('pygame.draw.lines')
    def test_draw_methods_called(self, mock_lines, mock_arc, mock_rect, mock_polygon, mock_circle):
        """Test that the draw method calls the expected pygame draw functions."""
        # Create a mock surface
        mock_surface = MagicMock()
        
        # Call the draw method
        self.visualizer.draw(mock_surface)
        
        # Verify that the expected draw methods were called
        self.assertTrue(mock_circle.called)
        self.assertTrue(mock_polygon.called)
        self.assertTrue(mock_rect.called)
        self.assertTrue(mock_arc.called)
        self.assertTrue(mock_lines.called)
    
    @patch('pygame.display.flip')
    @patch('pygame.event.get')
    @patch('pygame.time.Clock')
    def test_run_method(self, mock_clock, mock_event_get, mock_flip):
        """Test the main run method with mocked pygame functions."""
        # Set up mocks
        mock_clock.return_value.tick.return_value = 30
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]
        
        # Create a visualizer with a small window for testing
        visualizer = EuropeanHypnosisVisualizer(width=100, height=100, fps=30)
        
        # Mock the display.set_mode method
        with patch('pygame.display.set_mode') as mock_set_mode:
            mock_surface = MagicMock()
            mock_set_mode.return_value = mock_surface
            
            # Run the visualization (should exit immediately due to QUIT event)
            visualizer.run()
            
            # Verify that the display was set up
            mock_set_mode.assert_called_once_with((100, 100))
            
            # Verify that the display was updated
            mock_flip.assert_called()
            
            # Verify that the clock was ticked
            mock_clock.return_value.tick.assert_called_with(30)


if __name__ == '__main__':
    unittest.main()
