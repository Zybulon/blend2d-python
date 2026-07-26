#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import blend2d
import tempfile
import os


class TestComprehensive(unittest.TestCase):
    def test_context_initialization(self):
        """Test that the BLContext can be initialized properly."""
        # Test default initialization
        ctx = blend2d.BLContext()
        self.assertIsInstance(ctx, blend2d.BLContext)
        
        # Test initialization with image
        img = blend2d.BLImage(400, 300)
        ctx = blend2d.BLContext(img)
        self.assertIsInstance(ctx, blend2d.BLContext)
    
    def test_context_properties(self):
        """Test that context properties can be get and set."""
        img = blend2d.BLImage(400, 300)
        ctx = blend2d.BLContext(img)
        
        # Test read-write properties
        ctx.comp_op = blend2d.BL_COMP_OP_SRC_COPY
        self.assertEqual(ctx.comp_op, blend2d.BL_COMP_OP_SRC_COPY)
        
        ctx.global_alpha = 0.5
        self.assertAlmostEqual(ctx.global_alpha, 0.5)
        
        # Test fill style
        fill_style = blend2d.BLRgba32(255, 0, 0, 255)
        ctx.set_fill_style(fill_style)
    
    def test_font_functionality(self):
        """Test that font functionality works."""
        face = blend2d.BLFontFace()
        self.assertIsInstance(face, blend2d.BLFontFace)
        
        font = blend2d.BLFont()
        self.assertIsInstance(font, blend2d.BLFont)
        
        # Create a glyph buffer
        gb = blend2d.BLGlyphBuffer()
        self.assertIsInstance(gb, blend2d.BLGlyphBuffer)
        
        # Set some text to the glyph buffer
        gb.setText("Hello")
        self.assertEqual(gb.size, 5)
    
    def test_pattern_functionality(self):
        """Test pattern functionality."""
        img = blend2d.BLImage(100, 100)
        pattern = blend2d.BLPattern(img)
        self.assertIsInstance(pattern, blend2d.BLPattern)
        
        # Test matrix property
        matrix = blend2d.BLMatrix2D()
        matrix.reset()
        pattern.matrix = matrix
        
        # Test area property
        self.assertIsInstance(pattern.area, blend2d.BLRectI)
    
    def test_image_functionality(self):
        """Test image functionality."""
        # Create a new image
        img = blend2d.BLImage(200, 100)
        self.assertIsInstance(img, blend2d.BLImage)
        self.assertEqual(img.width, 200)
        self.assertEqual(img.height, 100)
        
        # Test creating and saving an image
        ctx = blend2d.BLContext(img)
        ctx.set_fill_style(blend2d.BLRgba32(255, 0, 0, 255))
        ctx.fill_all()
        
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            temp_filename = tmp.name
            
        try:
            img.write_to_file(temp_filename)
            self.assertTrue(os.path.exists(temp_filename))
            self.assertTrue(os.path.getsize(temp_filename) > 0)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename) 