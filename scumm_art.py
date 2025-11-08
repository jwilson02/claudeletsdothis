"""
SCUMM-Style Pixel Art Generator

Generates pixel art in the style of classic LucasArts SCUMM games
(Monkey Island, Day of the Tentacle, etc.)
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64
import random
import colorsys

# Classic SCUMM color palettes (inspired by EGA/VGA era)
SCUMM_PALETTES = {
    'ega': [
        (0, 0, 0),       # Black
        (0, 0, 170),     # Blue
        (0, 170, 0),     # Green
        (0, 170, 170),   # Cyan
        (170, 0, 0),     # Red
        (170, 0, 170),   # Magenta
        (170, 85, 0),    # Brown
        (170, 170, 170), # Light Gray
        (85, 85, 85),    # Dark Gray
        (85, 85, 255),   # Light Blue
        (85, 255, 85),   # Light Green
        (85, 255, 255),  # Light Cyan
        (255, 85, 85),   # Light Red
        (255, 85, 255),  # Light Magenta
        (255, 255, 85),  # Yellow
        (255, 255, 255)  # White
    ],
    'vga_warm': [
        (34, 32, 52),    # Dark purple-blue
        (69, 40, 60),    # Purple
        (102, 57, 49),   # Brown
        (143, 86, 59),   # Light brown
        (223, 113, 38),  # Orange
        (217, 160, 102), # Tan
        (238, 195, 154), # Light tan
        (251, 242, 54),  # Yellow
        (153, 229, 80),  # Light green
        (106, 190, 48),  # Green
        (55, 148, 110),  # Teal
        (75, 105, 47),   # Dark green
        (82, 75, 36),    # Olive
        (50, 60, 57),    # Dark teal
        (63, 63, 116),   # Blue
        (48, 96, 130)    # Light blue
    ],
    'monkey_island': [
        (0, 0, 0),       # Black
        (40, 20, 0),     # Very dark brown
        (80, 40, 20),    # Dark brown
        (120, 60, 30),   # Brown
        (160, 100, 50),  # Light brown
        (200, 140, 80),  # Tan
        (240, 180, 120), # Light tan
        (255, 220, 180), # Skin
        (20, 40, 60),    # Dark blue
        (40, 80, 120),   # Blue
        (60, 120, 180),  # Light blue
        (100, 160, 220), # Sky blue
        (40, 80, 40),    # Dark green
        (80, 140, 80),   # Green
        (180, 180, 180), # Light gray
        (255, 255, 255)  # White
    ]
}

class SCUMMPixelArtGenerator:
    """Generate SCUMM-style pixel art"""

    def __init__(self, width=320, height=200, palette='vga_warm'):
        """
        Initialize the generator

        Args:
            width: Canvas width (classic SCUMM was 320px)
            height: Canvas height (classic SCUMM was 200px)
            palette: Color palette to use
        """
        self.width = width
        self.height = height
        self.palette = SCUMM_PALETTES.get(palette, SCUMM_PALETTES['vga_warm'])
        self.image = Image.new('RGB', (width, height), self.palette[0])
        self.draw = ImageDraw.Draw(self.image)

    def get_palette_color(self, index):
        """Get color from palette by index"""
        return self.palette[index % len(self.palette)]

    def find_closest_palette_color(self, rgb):
        """Find closest color in palette to given RGB"""
        min_dist = float('inf')
        closest = self.palette[0]
        for color in self.palette:
            dist = sum((a - b) ** 2 for a, b in zip(rgb, color))
            if dist < min_dist:
                min_dist = dist
                closest = color
        return closest

    def draw_character(self, x, y, char_type='hero', scale=1):
        """
        Draw a SCUMM-style character sprite

        Args:
            x, y: Position
            char_type: Type of character (hero, pirate, merchant, etc.)
            scale: Size multiplier
        """
        base_width = 16 * scale
        base_height = 24 * scale

        if char_type == 'hero':
            # Head
            self.draw_rect(x + 6*scale, y, 4*scale, 5*scale, self.get_palette_color(7))  # Skin
            # Hair
            self.draw_rect(x + 5*scale, y, 6*scale, 2*scale, self.get_palette_color(3))
            # Eyes
            self.draw_rect(x + 6*scale, y + 2*scale, 1*scale, 1*scale, self.get_palette_color(0))
            self.draw_rect(x + 8*scale, y + 2*scale, 1*scale, 1*scale, self.get_palette_color(0))
            # Body (shirt)
            self.draw_rect(x + 5*scale, y + 5*scale, 6*scale, 8*scale, self.get_palette_color(8))
            # Arms
            self.draw_rect(x + 3*scale, y + 6*scale, 2*scale, 6*scale, self.get_palette_color(7))
            self.draw_rect(x + 11*scale, y + 6*scale, 2*scale, 6*scale, self.get_palette_color(7))
            # Legs (pants)
            self.draw_rect(x + 6*scale, y + 13*scale, 2*scale, 8*scale, self.get_palette_color(1))
            self.draw_rect(x + 8*scale, y + 13*scale, 2*scale, 8*scale, self.get_palette_color(1))
            # Feet
            self.draw_rect(x + 5*scale, y + 21*scale, 3*scale, 2*scale, self.get_palette_color(2))
            self.draw_rect(x + 8*scale, y + 21*scale, 3*scale, 2*scale, self.get_palette_color(2))

        elif char_type == 'pirate':
            # Head with bandana
            self.draw_rect(x + 6*scale, y + 1*scale, 4*scale, 4*scale, self.get_palette_color(7))
            self.draw_rect(x + 5*scale, y, 6*scale, 2*scale, self.get_palette_color(4))  # Red bandana
            # Eye patch
            self.draw_rect(x + 6*scale, y + 2*scale, 2*scale, 1*scale, self.get_palette_color(0))
            # Beard
            self.draw_rect(x + 6*scale, y + 4*scale, 4*scale, 2*scale, self.get_palette_color(2))
            # Body (striped shirt)
            for i in range(4):
                color = self.get_palette_color(14) if i % 2 == 0 else self.get_palette_color(1)
                self.draw_rect(x + 5*scale, y + (6+i*2)*scale, 6*scale, 2*scale, color)
            # Arms
            self.draw_rect(x + 3*scale, y + 7*scale, 2*scale, 5*scale, self.get_palette_color(7))
            self.draw_rect(x + 11*scale, y + 7*scale, 2*scale, 5*scale, self.get_palette_color(7))
            # Legs
            self.draw_rect(x + 6*scale, y + 14*scale, 2*scale, 7*scale, self.get_palette_color(2))
            self.draw_rect(x + 8*scale, y + 14*scale, 2*scale, 7*scale, self.get_palette_color(2))
            # Boots
            self.draw_rect(x + 5*scale, y + 21*scale, 3*scale, 2*scale, self.get_palette_color(0))
            self.draw_rect(x + 8*scale, y + 21*scale, 3*scale, 2*scale, self.get_palette_color(0))

    def draw_object(self, x, y, obj_type='chest', scale=1):
        """
        Draw a SCUMM-style object

        Args:
            x, y: Position
            obj_type: Type of object
            scale: Size multiplier
        """
        if obj_type == 'chest':
            # Treasure chest
            self.draw_rect(x, y + 6*scale, 16*scale, 10*scale, self.get_palette_color(3))
            self.draw_rect(x + 2*scale, y + 8*scale, 12*scale, 6*scale, self.get_palette_color(4))
            # Lock
            self.draw_rect(x + 7*scale, y + 10*scale, 2*scale, 3*scale, self.get_palette_color(15))
            # Lid
            self.draw_rect(x, y, 16*scale, 6*scale, self.get_palette_color(2))
            self.draw_rect(x + 2*scale, y + 2*scale, 12*scale, 3*scale, self.get_palette_color(3))

        elif obj_type == 'skull':
            # Skull
            self.draw_rect(x + 2*scale, y + 2*scale, 12*scale, 10*scale, self.get_palette_color(14))
            # Eye sockets
            self.draw_rect(x + 4*scale, y + 4*scale, 3*scale, 3*scale, self.get_palette_color(0))
            self.draw_rect(x + 9*scale, y + 4*scale, 3*scale, 3*scale, self.get_palette_color(0))
            # Nose hole
            self.draw_rect(x + 7*scale, y + 7*scale, 2*scale, 2*scale, self.get_palette_color(0))
            # Teeth
            for i in range(6):
                self.draw_rect(x + (4+i*2)*scale, y + 11*scale, 1*scale, 2*scale, self.get_palette_color(0))

        elif obj_type == 'coin':
            # Gold coin
            self.draw_rect(x + 2*scale, y + 1*scale, 6*scale, 8*scale, self.get_palette_color(14))
            self.draw_rect(x + 1*scale, y + 2*scale, 8*scale, 6*scale, self.get_palette_color(14))
            # Highlight
            self.draw_rect(x + 3*scale, y + 2*scale, 2*scale, 2*scale, self.get_palette_color(15))
            # Shadow
            self.draw_rect(x + 5*scale, y + 6*scale, 2*scale, 2*scale, self.get_palette_color(4))

    def draw_background(self, scene_type='dungeon'):
        """
        Draw a SCUMM-style background scene

        Args:
            scene_type: Type of scene to draw
        """
        if scene_type == 'dungeon':
            # Stone wall background
            for y in range(0, self.height, 16):
                for x in range(0, self.width, 16):
                    # Randomize stone colors slightly
                    base_color = random.choice([1, 2, 8])
                    self.draw_rect(x, y, 16, 16, self.get_palette_color(base_color))
                    # Add some detail
                    if random.random() > 0.7:
                        self.draw_rect(x + 2, y + 2, 4, 4, self.get_palette_color(0))

        elif scene_type == 'beach':
            # Sky
            self.draw_rect(0, 0, self.width, self.height // 2, self.get_palette_color(11))
            # Sand
            self.draw_rect(0, self.height // 2, self.width, self.height // 2, self.get_palette_color(5))
            # Waves
            for i in range(0, self.width, 20):
                self.draw_rect(i, self.height // 2 - 10, 10, 5, self.get_palette_color(10))

        elif scene_type == 'forest':
            # Sky
            self.draw_rect(0, 0, self.width, self.height // 3, self.get_palette_color(10))
            # Trees
            for i in range(0, self.width, 40):
                tree_x = i + random.randint(-10, 10)
                # Trunk
                self.draw_rect(tree_x + 15, self.height // 3, 10, self.height * 2 // 3, self.get_palette_color(2))
                # Leaves
                self.draw_rect(tree_x, self.height // 3 - 20, 40, 30, self.get_palette_color(13))
            # Ground
            self.draw_rect(0, self.height * 2 // 3, self.width, self.height // 3, self.get_palette_color(12))

    def draw_rect(self, x, y, width, height, color):
        """Draw a filled rectangle"""
        self.draw.rectangle([x, y, x + width - 1, y + height - 1], fill=color)

    def draw_dithered_gradient(self, x, y, width, height, color1_idx, color2_idx):
        """Draw a dithered gradient (classic SCUMM technique)"""
        color1 = self.get_palette_color(color1_idx)
        color2 = self.get_palette_color(color2_idx)

        for dy in range(height):
            for dx in range(width):
                # Checkerboard dithering pattern
                if (dx + dy) % 2 == 0:
                    self.image.putpixel((x + dx, y + dy), color1)
                else:
                    self.image.putpixel((x + dx, y + dy), color2)

    def create_sprite_sheet(self, sprite_type='character'):
        """
        Create a sprite sheet with multiple frames

        Args:
            sprite_type: Type of sprite sheet to create
        """
        frames = 4
        frame_width = self.width // frames

        if sprite_type == 'character':
            for i in range(frames):
                # Walking animation frames
                x_offset = i * frame_width + frame_width // 2 - 8
                y_offset = self.height // 2 - 12

                # Slightly different pose for each frame
                self.draw_character(x_offset, y_offset + (i % 2), 'hero')

        elif sprite_type == 'objects':
            objects = ['chest', 'skull', 'coin', 'coin']
            for i, obj in enumerate(objects):
                x_offset = i * frame_width + frame_width // 2 - 8
                y_offset = self.height // 2 - 8
                self.draw_object(x_offset, y_offset, obj, scale=2)

    def add_scumm_border(self):
        """Add classic SCUMM verb/interface border at bottom"""
        border_height = 40
        border_y = self.height - border_height

        # Border background
        self.draw_rect(0, border_y, self.width, border_height, self.get_palette_color(0))

        # Verb buttons (simplified)
        verbs = ['LOOK', 'PICK UP', 'USE', 'TALK', 'WALK']
        button_width = self.width // len(verbs)

        for i, verb in enumerate(verbs):
            x = i * button_width
            # Button background
            self.draw_rect(x + 2, border_y + 2, button_width - 4, border_height - 4,
                          self.get_palette_color(1))

    def to_base64(self, scale_factor=1):
        """
        Convert image to base64 string for web display

        Args:
            scale_factor: Scale up the image (for better display on modern screens)
        """
        if scale_factor > 1:
            new_size = (self.width * scale_factor, self.height * scale_factor)
            scaled_image = self.image.resize(new_size, Image.NEAREST)  # Nearest neighbor for crisp pixels
        else:
            scaled_image = self.image

        buffer = io.BytesIO()
        scaled_image.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f'data:image/png;base64,{img_base64}'

    def save(self, filename, scale_factor=1):
        """
        Save the image to a file

        Args:
            filename: Output filename
            scale_factor: Scale up the image
        """
        if scale_factor > 1:
            new_size = (self.width * scale_factor, self.height * scale_factor)
            scaled_image = self.image.resize(new_size, Image.NEAREST)
        else:
            scaled_image = self.image

        scaled_image.save(filename)


def generate_preset_scene(scene_name, palette='vga_warm'):
    """
    Generate a preset SCUMM-style scene

    Args:
        scene_name: Name of the preset scene
        palette: Color palette to use

    Returns:
        Base64 encoded image string
    """
    generator = SCUMMPixelArtGenerator(320, 200, palette)

    if scene_name == 'dungeon_hero':
        generator.draw_background('dungeon')
        generator.draw_character(150, 80, 'hero', scale=2)
        generator.draw_object(50, 120, 'chest', scale=2)
        generator.draw_object(250, 130, 'skull', scale=2)

    elif scene_name == 'pirate_beach':
        generator.draw_background('beach')
        generator.draw_character(140, 70, 'pirate', scale=2)
        generator.draw_object(50, 90, 'skull', scale=1)
        generator.draw_object(260, 95, 'chest', scale=1)

    elif scene_name == 'forest_treasure':
        generator.draw_background('forest')
        generator.draw_character(100, 80, 'hero', scale=2)
        generator.draw_object(200, 100, 'chest', scale=2)
        # Add some coins
        for i in range(5):
            generator.draw_object(170 + i * 12, 135, 'coin', scale=1)

    elif scene_name == 'character_sheet':
        generator.draw_character(50, 20, 'hero', scale=3)
        generator.draw_character(150, 20, 'pirate', scale=3)
        generator.draw_character(100, 110, 'hero', scale=2)

    elif scene_name == 'objects_collection':
        generator.draw_object(30, 30, 'chest', scale=3)
        generator.draw_object(150, 30, 'skull', scale=3)
        generator.draw_object(270, 30, 'coin', scale=5)
        generator.draw_object(50, 120, 'chest', scale=2)
        generator.draw_object(150, 120, 'skull', scale=2)

    elif scene_name == 'sprite_sheet_characters':
        generator.create_sprite_sheet('character')

    elif scene_name == 'sprite_sheet_objects':
        generator.create_sprite_sheet('objects')

    elif scene_name == 'scumm_interface':
        generator.draw_background('dungeon')
        generator.draw_character(150, 50, 'pirate', scale=2)
        generator.draw_object(50, 90, 'chest', scale=2)
        generator.add_scumm_border()

    return generator.to_base64(scale_factor=2)


def generate_custom_scene(background, characters, objects, palette='vga_warm'):
    """
    Generate a custom SCUMM-style scene

    Args:
        background: Background type
        characters: List of character dictionaries with x, y, type
        objects: List of object dictionaries with x, y, type
        palette: Color palette to use

    Returns:
        Base64 encoded image string
    """
    generator = SCUMMPixelArtGenerator(320, 200, palette)

    # Draw background
    if background:
        generator.draw_background(background)

    # Draw objects (behind characters)
    for obj in objects:
        generator.draw_object(
            obj.get('x', 0),
            obj.get('y', 0),
            obj.get('type', 'chest'),
            obj.get('scale', 1)
        )

    # Draw characters
    for char in characters:
        generator.draw_character(
            char.get('x', 0),
            char.get('y', 0),
            char.get('type', 'hero'),
            char.get('scale', 1)
        )

    return generator.to_base64(scale_factor=2)
