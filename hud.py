#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hud_manager.py - Futuristic Dynamic HUD manager class
"""

import blend2d
import math
import os
import sys
import time
import threading
import random
import statistics
import tempfile
import numpy as np
import cv2
import time
from urllib.parse import urlparse  
import requests
# Define some useful constants
TWO_PI = 2 * math.pi
PI = math.pi
HALF_PI = math.pi / 2

# Constants for the HUD appearance
WIDTH = 800
HEIGHT = 480
BG_COLOR = (0.02, 0.03, 0.07, 1.0)  # Background color
ACCENT_COLOR = (0.8, 0.7, 0.3, 1.0)  # Accent color
TEXT_COLOR = (1.0, 1.0, 1.0, 1.0)    # White text

# HUD elements positioning
HUD_CIRCLE_RADIUS = 110
COMPASS_Y = 35

# Color cache to prefer solid colors
COLOR_CACHE = {}

def get_cached_color(r, g, b, a=1.0):
    """Get a color from cache or create a new one"""
    # For performance, use solid colors (alpha=1.0) when possible
    if a < 1.0:
        a = 1.0  # Force full opacity
    cache_key = (r, g, b, a)
    if cache_key not in COLOR_CACHE:
        COLOR_CACHE[cache_key] = (r, g, b, a)
    return COLOR_CACHE[cache_key]

# Define common colors
TRANSPARENT_BLACK = get_cached_color(0.0, 0.0, 0.0, 1.0)
WHITE_COLOR = get_cached_color(1.0, 1.0, 1.0, 1.0)
WHITE_TRANSPARENT = get_cached_color(0.6, 0.6, 0.6, 1.0)
RED_COLOR = get_cached_color(1.0, 0.3, 0.3, 1.0)
RED_GLOW = get_cached_color(1.0, 0.3, 0.3, 1.0)
ACCENT_TRANSPARENT = get_cached_color(ACCENT_COLOR[0], ACCENT_COLOR[1], ACCENT_COLOR[2], 1.0)

# Font cache to avoid repeated font loading
FONT_PATH = None
FONT_CACHE = {}

def fast_sin(angle):
    """Faster sine approximation for animations"""
    # Convert to range [0, 1)
    angle = (angle % (2 * math.pi)) / (2 * math.pi)
    
    # Apply a quick and accurate sine approximation
    y = 4 * angle * (1 - angle)  # Parabolic approximation
    y = 0.225 * (y * (2 - y) - 1) + y  # Correction for better accuracy
    
    return y * 2 - 1  # Range [-1, 1]

def get_cached_font(size, extra_size=0):
    """Get a font from cache or create a new one"""
    cache_key = (size, extra_size)
    if cache_key in FONT_CACHE:
        return FONT_CACHE[cache_key]
    
    try:
        font_face = blend2d.BLFontFace.create_from_file(find_font_path())
        font = blend2d.BLFont.create_new(font_face, size + extra_size)
        FONT_CACHE[cache_key] = font
        return font
    except Exception as e:
        print(f"Font error: {e}")
        # Return a previously cached font as fallback if available
        if FONT_CACHE:
            return next(iter(FONT_CACHE.values()))
        raise  # Re-raise if no fallback available

def find_font_path():
    """Find a usable font on the system"""
    global FONT_PATH
    
    if FONT_PATH is not None:
        return FONT_PATH
        
    # Try common font locations
    possible_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:/Windows/Fonts/arial.ttf"
    ]
    
    for path in possible_fonts:
        if os.path.exists(path):
            FONT_PATH = path
            return path
            
    # If we couldn't find any of the common fonts, raise an exception
    raise Exception("Could not find a usable font on this system")

# Create a class to manage sensor data
class SensorSystem:
    """Manages sensor data and provides updates for the HUD"""
    
    def __init__(self):
        # Initialize with default values
        self.heading = 331.0
        self.altitude = 63
        self.ammo_count = 28
        self.ammo_max = 3
        self.health = 85
        self.shield = 70
        self.weapon_name = "PLASMAGUN"
        self.ammo_type = "Energy"
        self.ammo_capacity = 32  # Max ammo in a magazine
        
        # Physical movement simulation
        self.position = [0.0, 0.0, 0.0]  # [x, y, z] in meters
        self.velocity = [0.0, 0.0, 0.0]  # [vx, vy, vz] in m/s
        self.target_velocity = [0.0, 0.0, 0.0]
        self.max_speed = 5.0  # Maximum speed in m/s
        self.is_moving = False
        self.movement_pattern = "idle"  # Current movement pattern
        
        # Environment simulation
        self.targets = []  # List of potential targets with positions
        self.obstacles = []  # List of obstacles to avoid
        self.terrain_height = 0.0  # Current terrain height
        self.gravity = -9.8  # m/s^2
        self.is_grounded = True
        self.jump_velocity = 0.0
        
        # Targets for smooth transitions
        self.target_heading = self.heading
        self.target_altitude = self.altitude
        self.target_health = self.health
        self.target_shield = self.shield
        
        # Flags for events
        self.firing = False
        self.firing_effect_time = 0  # For crosshair firing effect
        self.taking_damage = False
        self.shield_recharging = False
        self.is_reloading = False
        self.reload_start_time = 0
        self.reload_duration = 2.0  # seconds
        
        # Threat indicators (for red dots on compass)
        self.threats = []  # List of (angle, intensity) tuples
        
        # Animation thread
        self.running = False
        self.animation_thread = None
        self.lock = threading.Lock()
        
        # Initialize environment
        self._init_environment()
        
        # Cache for calculations to avoid repeating work
        self._cache = {}
        self._last_cache_time = 0
    
    def _init_environment(self):
        """Set up the simulated environment with targets and obstacles"""
        # Create some targets at various locations
        for i in range(5):
            angle = random.uniform(0, 360)
            dist = random.uniform(50, 200)
            x = dist * math.cos(math.radians(angle))
            y = dist * math.sin(math.radians(angle))
            z = random.uniform(-10, 10)
            target_type = random.choice(["enemy", "neutral", "resource"])
            self.targets.append({
                'position': [x, y, z],
                'type': target_type,
                'health': 100 if target_type == "enemy" else 0,
                'detected': False,
                'visible': False
            })
            
        # Create some terrain obstacles
        for i in range(10):
            angle = random.uniform(0, 360)
            dist = random.uniform(20, 150)
            x = dist * math.cos(math.radians(angle))
            y = dist * math.sin(math.radians(angle))
            radius = random.uniform(5, 15)
            height = random.uniform(2, 10)
            self.obstacles.append({
                'position': [x, y, 0],
                'radius': radius,
                'height': height,
                'type': random.choice(["rock", "tree", "building"])
            })
    
    def start(self):
        """Start the sensor system animation thread"""
        self.running = True
        self.animation_thread = threading.Thread(target=self._animation_loop)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def stop(self):
        """Stop the sensor system animation thread"""
        self.running = False
        if self.animation_thread:
            self.animation_thread.join(timeout=1.0)
    
    def _animation_loop(self):
        """Main animation loop that updates sensor values over time"""
        last_time = time.time()
        
        # Natural movement cycles
        movement_cycles = [
            ("patrol", 10),     # Patrol for 10 seconds
            ("investigate", 5), # Investigate for 5 seconds
            ("combat", 8),      # Combat mode for 8 seconds
            ("retreat", 3),     # Retreat for 3 seconds
            ("idle", 4)         # Rest for 4 seconds
        ]
        current_cycle = 0
        cycle_start_time = time.time()
        
        # Frame time timing
        frame_count = 0
        frame_time_accumulator = 0
        
        while self.running:
            frame_start = time.time()
            current_time = frame_start
            dt = current_time - last_time
            last_time = current_time
            
            # Cache time values to reduce repeated calculations
            self._last_cache_time = current_time
            
            # Check if we should switch movement patterns
            cycle_elapsed = current_time - cycle_start_time
            if cycle_elapsed > movement_cycles[current_cycle][1]:
                current_cycle = (current_cycle + 1) % len(movement_cycles)
                self.set_movement_pattern(movement_cycles[current_cycle][0])
                cycle_start_time = current_time
            
            with self.lock:
                # Update position based on velocity (basic physics)
                for i in range(3):
                    self.position[i] += self.velocity[i] * dt
                
                # Update velocity (with smoothing and physics)
                for i in range(3):
                    # Move toward target velocity with smoothing
                    self.velocity[i] += (self.target_velocity[i] - self.velocity[i]) * min(dt * 3, 1.0)
                
                # Apply gravity if not grounded
                if not self.is_grounded:
                    self.velocity[2] += self.gravity * dt
                    # Check if we've hit the ground
                    if self.position[2] <= self.terrain_height:
                        self.position[2] = self.terrain_height
                        self.velocity[2] = 0
                        self.is_grounded = True
                
                # Update heading based on movement direction
                if abs(self.velocity[0]) > 0.1 or abs(self.velocity[1]) > 0.1:
                    # Calculate heading from velocity direction
                    movement_heading = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))
                    # Adjust to 0-360 range
                    movement_heading = (movement_heading + 90) % 360
                    
                    # Only update heading if actively moving
                    if self.is_moving:
                        # Add some natural motion to the heading (like head movement)
                        # Use fast_sin for better performance
                        heading_jitter = fast_sin(current_time * 2) * 2  # Small head movement
                        self.target_heading = movement_heading + heading_jitter
                
                # Smooth heading changes (compass rotation)
                heading_diff = (self.target_heading - self.heading + 180) % 360 - 180
                self.heading += heading_diff * min(dt * 2, 1.0)
                
                # Update altitude based on target distance - only recalculate when needed
                if self.targets and frame_count % 5 == 0:  # Only update every 5 frames
                    # Find closest target
                    closest_target = min(self.targets, key=lambda t: self._distance_to(t['position']))
                    if closest_target['visible']:
                        # Calculate distance to target
                        self.target_altitude = int(self._distance_to(closest_target['position']))
                
                # Smooth altitude changes
                alt_diff = self.target_altitude - self.altitude
                self.altitude += alt_diff * min(dt * 3, 1.0)
                
                # Smooth health & shield changes
                health_diff = self.target_health - self.health
                self.health += health_diff * min(dt * 5, 1.0)
                
                shield_diff = self.target_shield - self.shield
                self.shield += shield_diff * min(dt * 3, 1.0)
                
                # Reload logic
                if self.is_reloading:
                    if current_time - self.reload_start_time > self.reload_duration:
                        self.is_reloading = False
                        self.ammo_count = self.ammo_capacity
                        self.ammo_max -= 1
                        if self.ammo_max <= 0:
                            # Out of mags - can't reload anymore
                            self.ammo_max = 0
                
                # Automatically reset firing flag after effect time
                if self.firing and current_time - self.firing_effect_time > 0.2:  # 200ms firing effect to match pulse duration
                    self.firing = False
                
                # Shield recharging
                if self.shield_recharging and self.shield < 100:
                    self.shield = min(100, self.shield + dt * 10)
                
                # Update target visibility and threats - do less frequently
                if frame_count % 3 == 0:  # Only update every 3 frames to save CPU
                    self._update_target_visibility()
                    self._update_threats_from_targets()
            
            # Calculate frame time for timing statistics
            frame_end = time.time()
            frame_time = frame_end - frame_start
            frame_time_accumulator += frame_time
            frame_count += 1
            
            # Sleep to limit CPU usage - use a consistent frame rate
            # Calculate sleep time to maintain target frame rate
            target_frame_time = 1/60  # Target 60 updates per second
            sleep_time = max(0, target_frame_time - frame_time)
            time.sleep(sleep_time)
    
    def _distance_to(self, target_pos):
        """Calculate distance to a target position"""
        # Cache distance calculations for frequently accessed targets
        cache_key = str(target_pos)
        if cache_key in self._cache:
            # Only recalculate if we've moved significantly since last calc
            last_pos = self._cache.get('last_position')
            if last_pos and self._distance_between(last_pos, self.position) < 0.1:
                return self._cache[cache_key]
        
        # Do the actual calculation if needed
        dx = target_pos[0] - self.position[0]
        dy = target_pos[1] - self.position[1]
        dz = target_pos[2] - self.position[2]
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        # Cache the result
        self._cache[cache_key] = distance
        self._cache['last_position'] = self.position.copy()
        
        return distance
    
    def _distance_between(self, pos1, pos2):
        """Calculate distance between two positions"""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def _angle_to(self, target_pos):
        """Calculate angle to a target position (in degrees)"""
        # Cache angle calculations for performance
        cache_key = 'angle_' + str(target_pos)
        if cache_key in self._cache:
            # Only recalculate if we've moved significantly or time has passed
            last_pos = self._cache.get('last_position')
            if (last_pos and 
                self._distance_between(last_pos, self.position) < 0.5 and
                time.time() - self._last_cache_time < 0.1):
                return self._cache[cache_key]
        
        dx = target_pos[0] - self.position[0]
        dy = target_pos[1] - self.position[1]
        # Convert to 0-360 range
        angle = math.degrees(math.atan2(dy, dx))
        angle = (angle + 90) % 360
        
        # Cache the result
        self._cache[cache_key] = angle
        
        return angle
    
    def _update_target_visibility(self):
        """Update which targets are visible based on position and heading"""
        for target in self.targets:
            # Calculate angle to target
            target_angle = self._angle_to(target['position'])
            
            # Calculate angle difference (accounting for wraparound at 360)
            angle_diff = min(
                abs(target_angle - self.heading),
                abs(target_angle - self.heading + 360),
                abs(target_angle - self.heading - 360)
            )
            
            # Check if target is in field of view (±60 degrees)
            in_fov = angle_diff < 60
            
            # Check distance 
            distance = self._distance_to(target['position'])
            in_range = distance < 200  # Visibility range
            
            # Update visibility
            target['visible'] = in_fov and in_range
            
            # Once detected, stay detected for a while (memory effect)
            if target['visible']:
                target['detected'] = True
    
    def _update_threats_from_targets(self):
        """Update threat indicators based on visible targets"""
        # Clear old threats
        self.threats = []
        
        # Add threats from detected targets
        for target in self.targets:
            if target['detected'] and target['type'] == 'enemy':
                angle = self._angle_to(target['position'])
                
                # Intensity based on distance (closer = more intense)
                distance = self._distance_to(target['position'])
                intensity = max(0.3, min(1.0, 200 / max(distance, 1)))
                
                # Increase intensity if the target is visible
                if target['visible']:
                    intensity = min(1.0, intensity * 1.5)
                
                self.threats.append((angle, intensity))
    
    def set_movement_pattern(self, pattern):
        """Set a movement pattern that determines behavior"""
        self.movement_pattern = pattern
        
        if pattern == "idle":
            # Stop moving
            self.target_velocity = [0, 0, 0]
            self.is_moving = False
            
        elif pattern == "patrol":
            # Move in a general direction with minor variations
            angle = random.uniform(0, 360)
            speed = random.uniform(2.0, 3.0)
            self.target_velocity = [
                speed * math.cos(math.radians(angle - 90)),
                speed * math.sin(math.radians(angle - 90)),
                0
            ]
            self.is_moving = True
            
        elif pattern == "investigate":
            # Move towards closest detected target
            detected_targets = [t for t in self.targets if t['detected']]
            if detected_targets:
                closest = min(detected_targets, key=lambda t: self._distance_to(t['position']))
                angle = self._angle_to(closest['position'])
                speed = random.uniform(1.0, 2.0)
                self.target_velocity = [
                    speed * math.cos(math.radians(angle - 90)),
                    speed * math.sin(math.radians(angle - 90)),
                    0
                ]
                self.is_moving = True
                
        elif pattern == "combat":
            # Move evasively while targeting enemies
            enemies = [t for t in self.targets if t['detected'] and t['type'] == 'enemy']
            if enemies:
                # Face the enemy
                enemy = min(enemies, key=lambda t: self._distance_to(t['position']))
                self.target_heading = self._angle_to(enemy['position'])
                
                # Strafe/circle around the enemy
                perp_angle = (self._angle_to(enemy['position']) + random.choice([90, -90])) % 360
                speed = random.uniform(3.0, 4.0)
                self.target_velocity = [
                    speed * math.cos(math.radians(perp_angle - 90)),
                    speed * math.sin(math.radians(perp_angle - 90)),
                    0
                ]
                self.is_moving = True
                
                # Occasionally fire at enemies in combat mode
                if random.random() < 0.2:
                    self.fire_weapon()
                    
        elif pattern == "retreat":
            # Move away from threats
            threats = [t for t in self.targets if t['detected'] and t['type'] == 'enemy']
            if threats:
                threat = min(threats, key=lambda t: self._distance_to(t['position']))
                # Move away from the threat
                angle = (self._angle_to(threat['position']) + 180) % 360
                speed = random.uniform(4.0, 5.0)
                self.target_velocity = [
                    speed * math.cos(math.radians(angle - 90)),
                    speed * math.sin(math.radians(angle - 90)),
                    0
                ]
                self.is_moving = True
    
    def jump(self):
        """Make the player jump"""
        if self.is_grounded:
            self.velocity[2] = 5.0  # Initial upward velocity
            self.is_grounded = False
    
    def reload(self):
        """Reload the weapon"""
        if not self.is_reloading and self.ammo_count < self.ammo_capacity and self.ammo_max > 0:
            self.is_reloading = True
            self.reload_start_time = time.time()
            return True
        return False
    
    def get_values(self):
        """Get current sensor values as a dict"""
        with self.lock:
            return {
                'heading': self.heading,
                'altitude': int(self.altitude),
                'ammo_count': self.ammo_count,
                'ammo_max': self.ammo_max,
                'ammo_capacity': self.ammo_capacity,
                'health': self.health,
                'shield': self.shield,
                'weapon_name': self.weapon_name,
                'ammo_type': self.ammo_type,
                'threats': self.threats.copy(),
                'firing': self.firing,
                'firing_effect_time': self.firing_effect_time,
                'is_moving': self.is_moving,
                'movement_pattern': self.movement_pattern,
                'is_reloading': self.is_reloading,
                'position': self.position.copy(),
                'velocity': self.velocity.copy()
            }
            
    def set_heading(self, heading):
        """Set target heading (degrees)"""
        with self.lock:
            self.target_heading = heading % 360
            
    def set_altitude(self, altitude):
        """Set target altitude"""
        with self.lock:
            self.target_altitude = altitude
            
    def set_ammo(self, count, max_ammo=None):
        """Set ammo count and optionally max ammo"""
        with self.lock:
            self.ammo_count = count
            if max_ammo is not None:
                self.ammo_max = max_ammo
                
    def set_health(self, health):
        """Set target health percentage"""
        with self.lock:
            self.target_health = max(0, min(100, health))
            
    def set_shield(self, shield):
        """Set target shield percentage"""
        with self.lock:
            self.target_shield = max(0, min(100, shield))
            
    def set_weapon(self, name, ammo_type=None):
        """Set weapon name and optionally ammo type"""
        with self.lock:
            self.weapon_name = name
            if ammo_type:
                self.ammo_type = ammo_type
                
    def fire_weapon(self):
        """Simulate firing the weapon"""
        with self.lock:
            if self.ammo_count > 0:
                self.firing = True
                self.firing_effect_time = time.time()  # Start firing effect
                self.ammo_count = max(0, self.ammo_count - 1)
                return True
            return False
            
    def take_damage(self, amount):
        """Simulate taking damage"""
        with self.lock:
            self.taking_damage = True
            
            # Damage goes to shield first, then health
            if self.shield > 0:
                shield_damage = min(self.shield, amount)
                self.target_shield -= shield_damage
                amount -= shield_damage
            
            if amount > 0:
                self.target_health -= amount
                
            # Ensure we don't go below 0
            self.target_health = max(0, self.target_health)
            self.target_shield = max(0, self.target_shield)
            
    def recharge_shield(self, enable=True):
        """Enable or disable shield recharging"""
        with self.lock:
            self.shield_recharging = enable
            
    def add_threat(self, angle, intensity=1.0):
        """Add a threat at the specified angle"""
        with self.lock:
            self.threats.append((angle % 360, min(1.0, max(0.0, intensity))))
            
    def clear_threats(self):
        """Clear all threats"""
        with self.lock:
            self.threats = []

# Compass renderer class
class CompassRenderer:
    """Optimized compass renderer that pre-computes position data for all angles"""
    
    def __init__(self, width, compass_y):
        """Initialize the compass renderer with display dimensions"""
        self.width = width
        self.cy = compass_y
        self.cx = width / 2
        
        # Pre-compute compass dimensions once
        self.compass_width = width * 0.9
        self.compass_half_width = self.compass_width / 2
        self.compass_start_x = self.cx - self.compass_half_width
        self.compass_end_x = self.cx + self.compass_half_width
        
        # Pre-define all useful angles
        self.cardinal_degrees = (0, 90, 180, 270)
        self.ordinal_degrees = (45, 135, 225, 315)
        self.regular_degrees = (15, 30, 60, 75, 105, 120, 150, 165, 
                               195, 210, 240, 255, 285, 300, 330, 345)
        self.all_degrees = (*self.cardinal_degrees, *self.ordinal_degrees, *self.regular_degrees)
        
        # Define marker heights (half-heights for efficiency)
        self.cardinal_half_height = 6  # 12/2
        self.ordinal_half_height = 5   # 10/2
        self.regular_half_height = 3   # 6/2
        
        # Create comprehensive caches
        self.position_cache = {}        # Maps (angle, heading) -> screen x position
        self.visibility_cache = {}      # Maps heading -> (visible cardinals, ordinals, regular markers)
        self.marker_path_cache = {}     # Maps heading -> (cardinal_path, ordinal_path, regular_path)
        self.label_cache = {}           # Maps heading -> (cardinal labels, ordinal labels with brightness)
        self.brightness_groups_cache = {}  # Maps heading -> grouped labels by brightness
        self.central_triangles = None   # Central indicator triangles (static) 
        
        # Font metrics caches (global scope)
        self.cardinal_metrics_cache = {}
        self.ordinal_metrics_cache = {}
        self.heading_metrics_cache = {}
        
        # Pre-cached primitive shapes
        self.main_line_rect = blend2d.BLRect(self.compass_start_x, self.cy - 0.5, self.compass_width, 1.0)
        
        # Initialize fonts
        self.cardinal_font = None
        self.ordinal_font = None
        self.heading_font = None
        
        # Compass labels
        self.compass_directions = [
            # Cardinal directions: name, angle, is_cardinal
            ("N", 0, True),
            ("E", 90, True),
            ("S", 180, True),
            ("W", 270, True),
            # Ordinal directions
            ("NE", 45, False),
            ("SE", 135, False),
            ("SW", 225, False),
            ("NW", 315, False),
        ]
        
        # Placeholder for triangle coordinates
        self.triangle_coords = {
            'outer': ((0, -6), (-8, 6), (8, 6)),       # Large triangle coordinates
            'inner': ((0, -4), (-6, 4), (6, 4)),       # Small triangle coordinates
            'marker': ((0, -15), (-5, -20), (5, -20))  # Threat marker triangle (no glow)
        }
        
        # Pre-compute shared paths and metrics
        self._initialize_pre_computations()
        
    def _initialize_pre_computations(self):
        """Initialize all pre-computed data"""
        # Pre-compute positions for all possible combinations
        self._precompute_positions()
        
        # Pre-compute visibility for all headings
        self._precompute_visibility()
        
        # Pre-compute marker paths for all headings
        self._precompute_marker_paths()
        
        # Create static central triangle paths
        self._create_central_triangles()
    
    def _precompute_positions(self):
        """Pre-compute x positions for all combinations of degree markers and headings"""
        # Pre-compute positions for all degrees and all possible headings (0-359)
        for heading in range(360):
            heading_offset_pos = heading - 540
            
            # Compute and cache position for each possible degree
            for degree in self.all_degrees:
                rel_angle = (degree + heading_offset_pos) % 360 - 180
                x_pos = self.cx + (rel_angle / 180) * self.compass_half_width
                self.position_cache[(degree, heading)] = x_pos
    
    def _precompute_visibility(self):
        """Pre-compute which markers and labels are visible for each heading"""
        # For each possible heading, determine which markers are visible
        for heading in range(360):
            cardinals = []
            ordinals = []
            regular = []
            
            # Check visibility for each marker type
            for degree in self.cardinal_degrees:
                x_pos = self.position_cache[(degree, heading)]
                if self.compass_start_x <= x_pos <= self.compass_end_x:
                    cardinals.append(x_pos)
                    
            for degree in self.ordinal_degrees:
                x_pos = self.position_cache[(degree, heading)]
                if self.compass_start_x <= x_pos <= self.compass_end_x:
                    ordinals.append(x_pos)
                    
            for degree in self.regular_degrees:
                x_pos = self.position_cache[(degree, heading)]
                if self.compass_start_x <= x_pos <= self.compass_end_x:
                    regular.append(x_pos)
            
            # Cache the visibility results for this heading
            self.visibility_cache[heading] = (cardinals, ordinals, regular)
    
    def _precompute_marker_paths(self):
        """Pre-compute marker paths for all headings"""
        # For each possible heading, create and cache marker paths
        for heading in range(360):
            cardinals, ordinals, regular = self.visibility_cache[heading]
            
            # Create path for cardinal markers
            cardinal_path = blend2d.BLPath()
            for x_pos in cardinals:
                cardinal_path.move_to(x_pos, self.cy - self.cardinal_half_height)
                cardinal_path.line_to(x_pos, self.cy + self.cardinal_half_height)
            
            # Create path for ordinal markers
            ordinal_path = blend2d.BLPath()
            for x_pos in ordinals:
                ordinal_path.move_to(x_pos, self.cy - self.ordinal_half_height)
                ordinal_path.line_to(x_pos, self.cy + self.ordinal_half_height)
            
            # Create path for regular markers
            regular_path = blend2d.BLPath()
            for x_pos in regular:
                regular_path.move_to(x_pos, self.cy - self.regular_half_height)
                regular_path.line_to(x_pos, self.cy + self.regular_half_height)
            
            # Cache the marker paths for this heading
            self.marker_path_cache[heading] = (cardinal_path, ordinal_path, regular_path)
    
    def _create_central_triangles(self):
        """Create the pre-computed central indicator triangles"""
        # Create a path object for the central triangles
        self.central_triangles = (blend2d.BLPath(), blend2d.BLPath())
        
        # Outer (larger) triangle
        self.central_triangles[0].move_to(self.cx + self.triangle_coords['outer'][0][0], 
                                         self.cy + self.triangle_coords['outer'][0][1])
        self.central_triangles[0].line_to(self.cx + self.triangle_coords['outer'][1][0], 
                                         self.cy + self.triangle_coords['outer'][1][1])
        self.central_triangles[0].line_to(self.cx + self.triangle_coords['outer'][2][0], 
                                         self.cy + self.triangle_coords['outer'][2][1])
        self.central_triangles[0].close()
        
        # Inner (smaller) triangle
        self.central_triangles[1].move_to(self.cx + self.triangle_coords['inner'][0][0], 
                                         self.cy + self.triangle_coords['inner'][0][1])
        self.central_triangles[1].line_to(self.cx + self.triangle_coords['inner'][1][0], 
                                         self.cy + self.triangle_coords['inner'][1][1])
        self.central_triangles[1].line_to(self.cx + self.triangle_coords['inner'][2][0], 
                                         self.cy + self.triangle_coords['inner'][2][1])
        self.central_triangles[1].close()
    
    def init_fonts(self):
        """Initialize fonts and pre-compute text metrics if not already done"""
        if self.cardinal_font is None:
            self.cardinal_font = get_cached_font(18)
            self.ordinal_font = get_cached_font(14)
            self.heading_font = get_cached_font(30)
            
            # Pre-compute all metrics for compass labels
            for name, angle, is_cardinal in self.compass_directions:
                try:
                    if is_cardinal:
                        if name not in self.cardinal_metrics_cache:
                            self.cardinal_metrics_cache[name] = self.cardinal_font.get_text_metrics(name)
                    else:
                        if name not in self.ordinal_metrics_cache:
                            self.ordinal_metrics_cache[name] = self.ordinal_font.get_text_metrics(name)
                except Exception:
                    # Fallback approximation if metrics calculation fails
                    if is_cardinal:
                        self.cardinal_metrics_cache[name] = (len(name) * 8, 0)
                    else:
                        self.ordinal_metrics_cache[name] = (len(name) * 6, 0)
            
            # Pre-compute heading metrics for all possible headings (0-359)
            for h in range(360):
                heading_text = f"{h}°"
                try:
                    self.heading_metrics_cache[heading_text] = self.heading_font.get_text_metrics(heading_text)
                except Exception:
                    self.heading_metrics_cache[heading_text] = (len(heading_text) * 15, 0)
            
            # Pre-compute all visible labels and their brightness groups for each heading
            self._precompute_labels()
    
    def _precompute_labels(self):
        """Pre-compute label data including brightness groups for all headings"""
        # For each possible heading, pre-compute visible labels and brightness grouping
        for heading in range(360):
            heading_offset_neg = heading - 180
            
            cardinal_directions = []
            ordinal_directions = []
            
            # Check visibility for each compass direction
            for name, angle, is_cardinal in self.compass_directions:
                x_pos = self.position_cache[(angle, heading)]
                
                if self.compass_start_x <= x_pos <= self.compass_end_x:
                    # Calculate brightness based on proximity to center
                    rel_angle = (angle + heading_offset_neg) % 360 - 180
                    proximity = 1.0 - (abs(rel_angle) / 180)
                    brightness = 0.5 + 0.5 * proximity
                    
                    if is_cardinal:
                        width = self.cardinal_metrics_cache[name][0]
                        cardinal_directions.append((name, x_pos, width, brightness))
                    else:
                        width = self.ordinal_metrics_cache[name][0]
                        ordinal_directions.append((name, x_pos, width, brightness))
            
            # Cache the visible labels
            self.label_cache[heading] = (cardinal_directions, ordinal_directions)
            
            # Pre-compute brightness groups for text rendering
            if cardinal_directions:
                # Group cardinal labels by brightness
                cardinal_text_groups = {}
                
                for name, x_pos, width, brightness in cardinal_directions:
                    rounded = round(brightness * 5) / 5
                    if rounded not in cardinal_text_groups:
                        cardinal_text_groups[rounded] = []
                    
                    cardinal_text_groups[rounded].append((name, x_pos, width))
            else:
                cardinal_text_groups = {}
            
            # Group ordinal labels by brightness
            if ordinal_directions:
                ordinal_text_groups = {}
                
                for name, x_pos, width, brightness in ordinal_directions:
                    rounded = round(brightness * 5) / 5
                    if rounded not in ordinal_text_groups:
                        ordinal_text_groups[rounded] = []
                    
                    ordinal_text_groups[rounded].append((name, x_pos, width))
            else:
                ordinal_text_groups = {}
            
            # Cache all brightness groups for this heading
            self.brightness_groups_cache[heading] = {
                'cardinal_text': cardinal_text_groups,
                'ordinal_text': ordinal_text_groups
            }
    
    def get_threat_path(self, visible_threats):
        """Create path for threat indicators based on the given visible threats"""
        path = blend2d.BLPath()
        
        # Add each threat triangle to the path (no glow triangles)
        coords = self.triangle_coords['marker']
        for x_pos, _ in visible_threats:
            path.move_to(x_pos + coords[0][0], self.cy + coords[0][1])
            path.line_to(x_pos + coords[1][0], self.cy + coords[1][1])
            path.line_to(x_pos + coords[2][0], self.cy + coords[2][1])
            path.close()
        
        return path
    
    def draw_compass(self, ctx, heading, threats=None):
        """Draw the compass using pre-computed values for maximum performance"""
        # Ensure fonts are initialized
        self.init_fonts()
        
        ctx.save()
        
        # Normalize heading to 0-359 range
        heading = int(heading) % 360
        
        # Draw main horizontal line using cached rectangle
        ctx.set_fill_style(get_cached_color(ACCENT_COLOR[0], ACCENT_COLOR[1], ACCENT_COLOR[2], 1.0))
        ctx.fill_rect(self.main_line_rect)
        
        # Get cached marker paths for this heading
        cardinal_path, ordinal_path, regular_path = self.marker_path_cache[heading]
        
        # Draw cardinal markers if any exist
        if not cardinal_path.empty():
            ctx.set_stroke_style(ACCENT_COLOR)
            ctx.stroke_width = 1.5
            ctx.stroke_path(cardinal_path)
        
        # Draw ordinal markers if any exist
        if not ordinal_path.empty():
            ctx.stroke_width = 1.2
            ctx.stroke_path(ordinal_path)
        
        # Draw regular markers if any exist
        if not regular_path.empty():
            ctx.set_stroke_style(get_cached_color(ACCENT_COLOR[0] * 0.7, ACCENT_COLOR[1] * 0.7, ACCENT_COLOR[2] * 0.7, 1.0))
            ctx.stroke_width = 1.0
            ctx.stroke_path(regular_path)
        
        # Get brightness groups for this heading from cache
        brightness_groups = self.brightness_groups_cache[heading]
        
        # Text rendering y offset
        y_offset = 17
        
        # Draw cardinal main text (no glow effect)
        for brightness, items in brightness_groups['cardinal_text'].items():
            ctx.set_fill_style(get_cached_color(brightness, brightness, brightness, 1.0))
            
            for name, x_pos, width in items:
                ctx.fill_text(blend2d.BLPoint(x_pos - width/2, self.cy - y_offset), self.cardinal_font, name)
        
        # Draw ordinal direction text
        for brightness, items in brightness_groups['ordinal_text'].items():
            gray = brightness * 0.9
            ctx.set_fill_style(get_cached_color(gray, gray, gray, 1.0))
            
            for name, x_pos, width in items:
                ctx.fill_text(blend2d.BLPoint(x_pos - width/2, self.cy - y_offset), self.ordinal_font, name)
        
        # Handle threats with efficient rendering (no glow triangles)
        if threats and len(threats) > 0:
            # Filter visible threats
            visible_threats = []
            
            for angle, intensity in threats:
                # Get cached position if available or calculate
                angle_int = int(angle) % 360
                if angle_int in self.all_degrees:
                    x_pos = self.position_cache[(angle_int, heading)]
                else:
                    # For non-standard angles, calculate position
                    heading_offset_pos = heading - 540
                    rel_angle = (angle + heading_offset_pos) % 360 - 180
                    x_pos = self.cx + (rel_angle / 180) * self.compass_half_width
                
                if self.compass_start_x <= x_pos <= self.compass_end_x:
                    visible_threats.append((x_pos, intensity))
            
            # Efficient threat rendering (only single red triangles, no glow)
            if visible_threats:
                # Create and draw main threat indicators in a single operation
                marker_path = self.get_threat_path(visible_threats)
                ctx.set_fill_style(RED_COLOR)
                ctx.fill_path(marker_path)
        
        # Draw current heading value using cached metrics
        heading_text = f"{heading}°"
        
        # Use pre-computed metrics
        metrics = self.heading_metrics_cache.get(heading_text, (len(heading_text) * 15, 0))
        ctx.set_fill_style(TEXT_COLOR)
        ctx.fill_text(blend2d.BLPoint(self.cx - metrics[0]/2, self.cy + 40), self.heading_font, heading_text)
        
        # Draw central indicator triangles using pre-computed paths
        ctx.set_fill_style(ACCENT_COLOR)
        ctx.fill_path(self.central_triangles[0])  # Outer triangle
        ctx.fill_path(self.central_triangles[1])  # Inner triangle
        
        ctx.restore()

# Altitude renderer
class AltitudeRenderer:
    """Optimized renderer for altitude display"""
    
    def __init__(self, width, compass_y):
        """Initialize the altitude renderer with display dimensions"""
        self.width = width
        self.cy = compass_y + 60  # Increased to avoid overlap with heading
        self.cx = width / 2
        
        # Font and metrics cache
        self.font = None
        self.metrics_cache = {}
        
    def init_font(self):
        """Initialize font and pre-compute text metrics if not already done"""
        if self.font is None:
            self.font = get_cached_font(16)
    
    def draw_altitude(self, ctx, altitude):
        """Draw the altitude indicator (distance to target)"""
        # Ensure font is initialized
        self.init_font()
        
        ctx.save()
        
        # Convert altitude to text
        alt_text = f"{altitude}m"
        
        # Use cached metrics if available, or compute them
        if alt_text not in self.metrics_cache:
            try:
                self.metrics_cache[alt_text] = self.font.get_text_metrics(alt_text)
            except Exception:
                # Fallback approximation
                self.metrics_cache[alt_text] = (len(alt_text) * 8, 0)
        
        metrics = self.metrics_cache[alt_text]
        
        # Draw text with single operation
        ctx.set_fill_style(TEXT_COLOR)
        ctx.fill_text(blend2d.BLPoint(self.cx - metrics[0]/2, self.cy), self.font, alt_text)
        
        ctx.restore()

# Reticle renderer
class ReticleRenderer:
    """Optimized renderer for the central reticle"""
    
    def __init__(self, width, height):
        """Initialize the reticle renderer with display dimensions"""
        self.width = width
        self.height = height
        self.cx = width / 2
        self.cy = height / 2
        
        # Pre-compute useful constants
        self.radius = HUD_CIRCLE_RADIUS
        self.crosshair_inner = 10
        self.crosshair_outer = 20
        
        # Pre-create paths for efficiency
        self.segment_path = blend2d.BLPath()
        self.crosshair_path = blend2d.BLPath()
        self.x_path = blend2d.BLPath()
        self.tick_path = blend2d.BLPath()
        
        # Pre-compute segment parameters
        self.segment_count = 8
        self.segment_fraction = 0.3  # Each segment covers 30% of its section
        self.angle_increment = TWO_PI / self.segment_count
        self.segment_angle = self.angle_increment * self.segment_fraction
        
        # Pre-compute tick parameters
        self.tick_count = 24
        self.tick_length = 5
        self.tick_radius = self.radius - 10
        self.tick_radius_outer = self.tick_radius + self.tick_length
        self.tick_angle_increment = TWO_PI / self.tick_count
        
        # Pulse effect parameters
        self.pulse_start_time = 0
        self.pulse_duration = 0.2  # Duration of pulse animation in seconds
        self.pulse_size_start = 20   # Starting size of pulse
        self.pulse_size_end = self.radius * 1.5  # Maximum size of pulse
        self.is_pulse_active = False  # Flag to track if pulse is currently active
        
        # Pre-compute reticle decorations
        self._precompute_paths()
    
    def _precompute_paths(self):
        """Pre-compute crosshair and X paths for reuse"""
        # Crosshair path
        self.crosshair_path.clear()
        # Horizontal lines
        self.crosshair_path.move_to(self.cx - self.crosshair_outer, self.cy)
        self.crosshair_path.line_to(self.cx - self.crosshair_inner, self.cy)
        self.crosshair_path.move_to(self.cx + self.crosshair_inner, self.cy)
        self.crosshair_path.line_to(self.cx + self.crosshair_outer, self.cy)
        # Vertical lines
        self.crosshair_path.move_to(self.cx, self.cy - self.crosshair_outer)
        self.crosshair_path.line_to(self.cx, self.cy - self.crosshair_inner)
        self.crosshair_path.move_to(self.cx, self.cy + self.crosshair_inner)
        self.crosshair_path.line_to(self.cx, self.cy + self.crosshair_outer)
        
        # X path for no ammo
        self.x_path.clear()
        self.x_path.move_to(self.cx - 6, self.cy - 6)
        self.x_path.line_to(self.cx + 6, self.cy + 6)
        self.x_path.move_to(self.cx + 6, self.cy - 6)
        self.x_path.line_to(self.cx - 6, self.cy + 6)
        
        # Pre-compute accent tick paths
        self.accent_tick_path = blend2d.BLPath()
        for i in range(0, self.tick_count, 4):
            angle = self.tick_angle_increment * i
            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)
            
            inner_x = self.cx + self.tick_radius * cos_angle
            inner_y = self.cy + self.tick_radius * sin_angle
            outer_x = self.cx + self.tick_radius_outer * cos_angle
            outer_y = self.cy + self.tick_radius_outer * sin_angle
            
            self.accent_tick_path.move_to(inner_x, inner_y)
            self.accent_tick_path.line_to(outer_x, outer_y)
        
        # Pre-compute regular tick paths
        self.regular_tick_path = blend2d.BLPath()
        for i in range(self.tick_count):
            if i % 4 == 0:
                continue  # Skip accent ticks
            
            angle = self.tick_angle_increment * i
            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)
            
            inner_x = self.cx + self.tick_radius * cos_angle
            inner_y = self.cy + self.tick_radius * sin_angle
            outer_x = self.cx + self.tick_radius_outer * cos_angle
            outer_y = self.cy + self.tick_radius_outer * sin_angle
            
            self.regular_tick_path.move_to(inner_x, inner_y)
            self.regular_tick_path.line_to(outer_x, outer_y)
    
    def draw_reticle(self, ctx, has_ammo=True, is_firing=False):
        """Draw a futuristic central reticle with ammo indicator and firing effect"""
        ctx.save()
        
        # Check if we need to start a new pulse
        current_time = time.time()
        if is_firing and not self.is_pulse_active:
            self.pulse_start_time = current_time
            self.is_pulse_active = True
        
        # Calculate pulse animation progress
        pulse_elapsed = current_time - self.pulse_start_time
        pulse_progress = pulse_elapsed / self.pulse_duration
        
        # Reset pulse if animation is complete
        if pulse_progress >= 1.0 and self.is_pulse_active:
            self.is_pulse_active = False
        
        # Draw the main circle with appropriate color
        if has_ammo:
            ctx.set_stroke_style(ACCENT_COLOR)
        else:
            ctx.set_stroke_style(RED_COLOR)
            
        ctx.stroke_width = 1.5
        ctx.stroke_circle(self.cx, self.cy, self.radius)
        
        # Draw segments (reusing path object)
        for i in range(self.segment_count):
            angle_start = self.angle_increment * i
            
            self.segment_path.clear()
            self.segment_path.arc_to(self.cx, self.cy, self.radius, self.radius, angle_start, self.segment_angle)
            
            # Use accent color for some segments
            if i % 2 == 0:
                ctx.set_stroke_style(ACCENT_COLOR)
            else:
                ctx.set_stroke_style(TEXT_COLOR)
                
            ctx.stroke_path(self.segment_path)
        
        # Draw crosshairs (pre-computed)
        ctx.set_stroke_style(TEXT_COLOR)
        ctx.stroke_width = 1.0
        ctx.stroke_path(self.crosshair_path)
        
        # Draw pulse effect if active
        if self.is_pulse_active and pulse_progress < 1.0:
            # Calculate pulse size and opacity
            pulse_size = self.pulse_size_start + (self.pulse_size_end - self.pulse_size_start) * pulse_progress
            pulse_opacity = max(0, 1.0 - pulse_progress)  # Fade from 1.0 to 0.0
            
            # Draw the pulse ring
            ctx.set_stroke_style(get_cached_color(1.0, 1.0, 1.0, pulse_opacity))
            ctx.stroke_width = 2.0 * (1.0 - pulse_progress * 0.5)  # Slightly thinner as it expands
            ctx.stroke_circle(self.cx, self.cy, pulse_size)
        
        # Draw center dot/element
        if not has_ammo:
            # Red X when out of ammo
            ctx.set_stroke_style(RED_COLOR)
            ctx.stroke_width = 2.0
            ctx.stroke_path(self.x_path)
        elif is_firing:
            # Draw a slightly enlarged center dot when firing
            ctx.set_fill_style(WHITE_COLOR)
            ctx.fill_circle(self.cx, self.cy, 5)
        else:
            # Normal state - draw a futuristic center element
            ctx.set_fill_style(WHITE_COLOR)
            # Inner dot
            ctx.fill_circle(self.cx, self.cy, 2)
            
            # Outer ring with accent color
            ctx.set_stroke_style(ACCENT_COLOR)
            ctx.stroke_width = 1.5
            ctx.stroke_circle(self.cx, self.cy, 5)
        
        # Draw tick marks using pre-computed paths
        # Draw accent colored ticks
        ctx.set_stroke_style(ACCENT_COLOR)
        ctx.stroke_width = 1.5
        ctx.stroke_path(self.accent_tick_path)
        
        # Draw regular ticks
        ctx.set_stroke_style(get_cached_color(0.7, 0.7, 0.7, 1.0))
        ctx.stroke_width = 1.0
        ctx.stroke_path(self.regular_tick_path)
        
        ctx.restore()

# Ammo counter renderer
class AmmoCounterRenderer:
    """Optimized renderer for ammo counter display"""
    
    def __init__(self, width, height):
        """Initialize the ammo counter renderer with display dimensions"""
        self.width = width
        self.height = height
        
        # Position for ammo counter
        self.x = 25
        self.y = height - 20
        
        # Font caches
        self.font_large = None
        self.font_small = None
        self.font_percent = None
        self.font_reload = None
        
        # Metrics cache 
        self.metrics_cache = {}
        
        # Pre-computed reload circle parameters
        self.circle_x = self.x + 70
        self.circle_y = self.y - 40
        self.circle_radius = 25
        
        # Paths for reuse
        self.reload_path = blend2d.BLPath()
    
    def init_fonts(self):
        """Initialize fonts if not already done"""
        if self.font_large is None:
            self.font_large = get_cached_font(140)
            self.font_small = get_cached_font(20)
            self.font_percent = get_cached_font(14)
            self.font_reload = get_cached_font(20)
    
    def draw_ammo_counter(self, ctx, ammo, ammo_max, is_reloading=False):
        """Draw a futuristic ammo counter with reload animation"""
        # Ensure fonts are initialized
        self.init_fonts()
        
        ctx.save()
        
        # Convert ammo to text
        ammo_text = f"{ammo}"
        
        if is_reloading:
            self._draw_reloading_state(ctx, ammo_text, ammo_max)
        else:
            self._draw_normal_state(ctx, ammo_text, ammo_max, ammo)
        
        ctx.restore()
    
    def _draw_reloading_state(self, ctx, ammo_text, ammo_max):
        """Draw the ammo counter in reloading state"""
        # Calculate reload completion percentage
        reload_time = time.time() % 2.0
        reload_percent = reload_time / 2.0  # 0.0 to 1.0
        
        # Draw reload progress circular indicator - background
        ctx.set_stroke_style(get_cached_color(0.3, 0.3, 0.3, 1.0))
        ctx.stroke_width = 3
        ctx.stroke_circle(self.circle_x, self.circle_y, self.circle_radius)
        
        # Progress arc
        arc_end = TWO_PI * reload_percent
        self.reload_path.clear()
        self.reload_path.arc_to(self.circle_x, self.circle_y, self.circle_radius, self.circle_radius, 0, arc_end)
        
        # Use cached colors for progress indicator 
        if reload_percent < 0.33:
            ctx.set_stroke_style(get_cached_color(1.0, 0.5, 0.0, 1.0))  # Orange
        elif reload_percent < 0.66:
            ctx.set_stroke_style(get_cached_color(0.5, 0.65, 0.5, 1.0))  # Greenish
        else:
            ctx.set_stroke_style(get_cached_color(0.0, 0.8, 1.0, 1.0))  # Blue
            
        ctx.stroke_width = 5
        ctx.stroke_path(self.reload_path)
        
        # Draw percentage in center of circle
        percent_text = f"{int(reload_percent * 100)}%"
        
        # Get metrics for percentage text
        if percent_text not in self.metrics_cache:
            try:
                self.metrics_cache[percent_text] = self.font_percent.get_text_metrics(percent_text)
            except Exception:
                self.metrics_cache[percent_text] = (len(percent_text) * 7, 0)
        
        metrics = self.metrics_cache[percent_text]
        
        # Draw percentage text
        ctx.set_fill_style(TEXT_COLOR)
        ctx.fill_text(blend2d.BLPoint(self.circle_x - metrics[0]/2, self.circle_y + 4), 
                      self.font_percent, percent_text)
        
        # Draw "RELOADING" text with subtle pulse
        reload_label = "RELOADING"
        
        # Very subtle pulse for the RELOADING text 
        pulse = (0.8 + 0.2 * math.sin(time.time() * 3))  # 0.8 to 1.0, very slow pulse
        
        # Draw the main text
        ctx.set_fill_style(get_cached_color(0.9, 0.7, 0.3, 1.0))  # Golden color
        ctx.fill_text(blend2d.BLPoint(self.x, self.y - 100), self.font_reload, reload_label)
    
    def _draw_normal_state(self, ctx, ammo_text, ammo_max, ammo):
        """Draw the ammo counter in normal state"""
        # Select color based on ammo level
        if ammo < 5:
            text_color = RED_COLOR
        else:
            text_color = TEXT_COLOR
        
        # Draw main ammo count
        ctx.set_fill_style(text_color)
        ctx.fill_text(blend2d.BLPoint(self.x, self.y), self.font_large, ammo_text)
        
        # Draw max ammo
        max_text = f"/ {ammo_max}"
        
        # Get metrics for max ammo text
        if max_text not in self.metrics_cache:
            try:
                self.metrics_cache[max_text] = self.font_small.get_text_metrics(max_text)
            except Exception:
                self.metrics_cache[max_text] = (len(max_text) * 10, 0)
        
        # Draw max ammo text
        ctx.set_fill_style(TEXT_COLOR)
        ctx.fill_text(blend2d.BLPoint(self.x + 175, self.y), self.font_small, max_text)

# Weapon info renderer
class WeaponInfoRenderer:
    """Optimized renderer for weapon information bar"""
    
    def __init__(self, width, height):
        """Initialize the weapon info renderer with display dimensions"""
        self.width = width
        self.height = height
        self.cx = width / 2
        self.y = height - 40
        self.bar_width = 240
        self.bar_height = 20
        
        # Calculated positions
        self.x = self.cx - self.bar_width / 2
        
        # Font and metrics cache
        self.font = None
        self.metrics_cache = {}
        
        # Cached colors
        self.bg_color = get_cached_color(0.15, 0.15, 0.15, 1.0)
        self.red_color = RED_COLOR
        self.orange_color = get_cached_color(1.0, 0.6, 0.0, 1.0)
        self.blue_color = get_cached_color(0.3, 0.6, 1.0, 1.0)
        self.tick_color = get_cached_color(0.5, 0.5, 0.5, 1.0)
        
        # Pre-computed paths
        self.tick_path = blend2d.BLPath()
    
    def init_font(self):
        """Initialize font if not already done"""
        if self.font is None:
            self.font = get_cached_font(16)
    
    def _create_tick_path(self, tick_count):
        """Create the tick marks path based on capacity"""
        self.tick_path.clear()
        
        tick_spacing = self.bar_width / tick_count
        
        # Draw all tick marks in one path
        for i in range(1, tick_count):
            tick_x = self.x + i * tick_spacing
            self.tick_path.move_to(tick_x, self.y + 2)
            self.tick_path.line_to(tick_x, self.y + self.bar_height - 2)
    
    def draw_weapon_info(self, ctx, weapon_name, ammo_type, ammo_count, ammo_capacity):
        """Draw an extremely efficient ammo counter bar with bullet tick marks"""
        # Ensure font is initialized
        self.init_font()
        
        ctx.save()
        
        # Pre-check to avoid unnecessary calculations if ammo_capacity is 0
        if ammo_capacity <= 0:
            # Draw just a gray empty bar with text
            ctx.set_fill_style(self.bg_color)
            ctx.fill_rect(blend2d.BLRect(self.x, self.y, self.bar_width, self.bar_height))
            
            # Draw "NO AMMO" text
            ctx.set_fill_style(self.red_color)
            ctx.fill_text(blend2d.BLPoint(self.cx - 30, self.y + 15), self.font, "NO AMMO")
            ctx.restore()
            return  # Exit early
        
        # 1. Draw background
        ctx.set_fill_style(self.bg_color)
        ctx.fill_rect(blend2d.BLRect(self.x, self.y, self.bar_width, self.bar_height))
        
        # 2. Draw remaining ammo indicator
        if ammo_count > 0:
            # Calculate filled width
            ammo_ratio = ammo_count / ammo_capacity
            filled_width = self.bar_width * ammo_ratio
            
            # Select color based on ammo level
            if ammo_ratio < 0.25:  # Less than 25% ammo
                ctx.set_fill_style(self.red_color)
            elif ammo_ratio < 0.5:  # Less than 50% ammo
                ctx.set_fill_style(self.orange_color)
            else:
                ctx.set_fill_style(self.blue_color)
                
            # Draw filled portion
            ctx.fill_rect(blend2d.BLRect(self.x, self.y, filled_width, self.bar_height))
        
        # 3. Draw tick marks
        if ammo_capacity > 1:  # Only need ticks if we have multiple bullets
            # Determine tick count based on capacity
            if ammo_capacity <= 10:
                # For low capacity weapons, show every bullet
                tick_count = ammo_capacity
            else:
                # For high capacity weapons, show fewer evenly spaced ticks
                tick_count = 10
            
            # Create tick path
            self._create_tick_path(tick_count)
            
            # Draw all ticks in a single operation
            ctx.set_stroke_style(self.tick_color)
            ctx.stroke_width = 1
            ctx.stroke_path(self.tick_path)
        
        # 4. Draw ammo count text
        ammo_text = f"{ammo_count}/{ammo_capacity}"
        
        # Get or calculate text metrics
        if ammo_text not in self.metrics_cache:
            try:
                self.metrics_cache[ammo_text] = self.font.get_text_metrics(ammo_text)
            except Exception:
                self.metrics_cache[ammo_text] = (len(ammo_text) * 8, 0)
        
        metrics = self.metrics_cache[ammo_text]
        
        # Draw text centered on bar
        ctx.set_fill_style(TEXT_COLOR)
        ctx.fill_text(blend2d.BLPoint(self.cx - metrics[0]/2, self.y + 15), self.font, ammo_text)
        
        ctx.restore()

# Health and shield renderer
class HealthShieldRenderer:
    """Optimized renderer for health and shield bars"""
    
    def __init__(self, width, height):
        """Initialize the health/shield renderer with display dimensions"""
        self.width = width
        self.height = height
        
        # Position constants
        self.x = width - 210
        self.y = height - 45
        self.bar_width = 150
        self.bar_height = 12
        self.spacing = 13
        
        # Font and metrics cache
        self.font = None
        self.metrics_cache = {}
        
        # Pre-cached colors
        self.bg_color = get_cached_color(0.15, 0.15, 0.15, 1.0)
        self.critical_health_color = RED_COLOR
        self.low_health_color = get_cached_color(1.0, 0.5, 0.0, 1.0)
        self.normal_health_color = ACCENT_COLOR
        self.shield_color = get_cached_color(0.4, 0.6, 0.9, 1.0)
        self.highlight_color = get_cached_color(1.0, 1.0, 1.0, 1.0)
    
    def init_font(self):
        """Initialize font if not already done"""
        if self.font is None:
            self.font = get_cached_font(14)
    
    def draw_health_shield(self, ctx, health, shield):
        """Draw futuristic health and shield bars"""
        # Ensure font is initialized
        self.init_font()
        
        ctx.save()
        
        # Draw background for health bar
        ctx.set_fill_style(self.bg_color)
        ctx.fill_rect(blend2d.BLRect(self.x, self.y, self.bar_width, self.bar_height))
        
        # Draw background for shield bar
        ctx.fill_rect(blend2d.BLRect(self.x, self.y + self.spacing, self.bar_width, self.bar_height))
        
        # Handle health bar
        self._draw_health_bar(ctx, health)
        
        # Handle shield bar
        self._draw_shield_bar(ctx, shield)
        
        # Draw percentages
        self._draw_percentages(ctx, health, shield)
        
        ctx.restore()
    
    def _draw_health_bar(self, ctx, health):
        """Draw the health bar with appropriate color based on health level"""
        # Calculate filled width
        filled_width = (health / 100.0) * self.bar_width
        
        # Determine health bar color based on level
        if health < 25:
            ctx.set_fill_style(self.critical_health_color)
        elif health < 50:
            ctx.set_fill_style(self.low_health_color)
        else:
            ctx.set_fill_style(self.normal_health_color)
        
        # Draw filled health bar
        ctx.fill_rect(blend2d.BLRect(self.x, self.y, filled_width, self.bar_height))
        
        # Add highlight to health bar
        ctx.set_fill_style(self.highlight_color)
        ctx.fill_rect(blend2d.BLRect(self.x, self.y, filled_width, 2))
    
    def _draw_shield_bar(self, ctx, shield):
        """Draw the shield bar with pulsing effect if recharging"""
        # Calculate filled width
        filled_width = (shield / 100.0) * self.bar_width
        
        # Determine if shield is recharging (simple heuristic)
        is_recharging = shield < 100 and shield > 0
        
        # Draw shield bar with optional pulse effect
        if is_recharging:
            # Pulsating shield bar
            pulse = 0.7 + 0.3 * math.sin(time.time() * 5)
            pulsing_shield_color = get_cached_color(0.4 * pulse, 0.6 * pulse, 0.9, 1.0)
            ctx.set_fill_style(pulsing_shield_color)
        else:
            # Normal shield bar
            ctx.set_fill_style(self.shield_color)
        
        # Draw filled shield bar
        ctx.fill_rect(blend2d.BLRect(self.x, self.y + self.spacing, filled_width, self.bar_height))
        
        # Add highlight to shield bar
        ctx.set_fill_style(self.highlight_color)
        ctx.fill_rect(blend2d.BLRect(self.x, self.y + self.spacing, filled_width, 2))
    
    def _draw_percentages(self, ctx, health, shield):
        """Draw percentage text for health and shield"""
        # Format percentage texts
        health_text = f"{int(health)}%"
        shield_text = f"{int(shield)}%"
        
        # Cache metrics if not already cached
        for text in (health_text, shield_text):
            if text not in self.metrics_cache:
                try:
                    self.metrics_cache[text] = self.font.get_text_metrics(text)
                except Exception:
                    self.metrics_cache[text] = (len(text) * 7, 0)
        
        # Draw health percentage
        ctx.set_fill_style(ACCENT_COLOR)
        ctx.fill_text(blend2d.BLPoint(self.x + self.bar_width + 10, self.y + 9), 
                       self.font, health_text)
        
        # Draw shield percentage
        ctx.fill_text(blend2d.BLPoint(self.x + self.bar_width + 10, self.y + self.spacing + 9), 
                       self.font, shield_text)

# Movement indicator renderer
class MovementIndicatorRenderer:
    """Optimized renderer for movement pattern indicator"""
    
    def __init__(self, height):
        """Initialize the movement indicator renderer"""
        self.x = 30
        self.y = height - 80
        
        # Font and metrics cache
        self.font = None
        self.metrics_cache = {}
        
        # Pre-cached colors and icons for different movement patterns
        self.movement_types = {
            'combat': {
                'color': get_cached_color(1.0, 0.3, 0.3, 1.0),
                'icon': "⚔"  # Combat icon
            },
            'patrol': {
                'color': get_cached_color(0.3, 0.7, 0.3, 1.0),
                'icon': "↻"  # Patrol icon
            },
            'investigate': {
                'color': get_cached_color(0.7, 0.7, 0.3, 1.0),
                'icon': "⚲"  # Investigate icon
            },
            'retreat': {
                'color': get_cached_color(1.0, 0.5, 0.0, 1.0),
                'icon': "←"  # Retreat icon
            },
            'idle': {
                'color': get_cached_color(0.5, 0.5, 0.5, 1.0),
                'icon': "⊙"  # Idle icon
            }
        }
    
    def init_font(self):
        """Initialize font if not already done"""
        if self.font is None:
            self.font = get_cached_font(18)
    
    def draw_movement_indicator(self, ctx, movement_pattern):
        """Draw an indicator of the current movement pattern"""
        # Ensure font is initialized
        self.init_font()
        
        ctx.save()
        
        # Get the appropriate color and icon for the movement pattern
        if movement_pattern in self.movement_types:
            pattern = self.movement_types[movement_pattern]
        else:
            # Fallback to idle if unknown pattern
            pattern = self.movement_types['idle']
        
        # Get the icon and color
        color = pattern['color']
        icon = pattern['icon']
        
        # Draw the icon with a background circle
        ctx.set_fill_style(color)
        ctx.fill_circle(self.x, self.y, 12)
        
        # Get or calculate metrics for the icon
        if icon not in self.metrics_cache:
            try:
                self.metrics_cache[icon] = self.font.get_text_metrics(icon)
            except Exception:
                # Fallback approximation
                self.metrics_cache[icon] = (16, 0)
        
        metrics = self.metrics_cache[icon]
        
        # Draw icon text centered
        ctx.set_fill_style(color)
        ctx.fill_text(blend2d.BLPoint(self.x - metrics[0]/2, self.y + 6), self.font, icon)
        
        ctx.restore()

# FPS counter renderer
class FpsCounterRenderer:
    """Optimized renderer for FPS counter"""
    
    def __init__(self, compass_y):
        """Initialize the FPS counter renderer"""
        self.x = 40
        self.y = compass_y + 130  # Positioned to avoid overlapping with reticle
        
        # Font and metrics cache
        self.font = None
        self.metrics_cache = {}
    
    def init_font(self):
        """Initialize font if not already done"""
        if self.font is None:
            self.font = get_cached_font(14)
    
    def draw_fps_counter(self, ctx, fps):
        """Draw the FPS counter with futuristic styling"""
        # Ensure font is initialized
        self.init_font()
        
        ctx.save()
        
        # Format FPS with one decimal place
        fps_text = f"{fps:.1f} FPS"
        
        # Get or calculate text metrics
        if fps_text not in self.metrics_cache:
            try:
                self.metrics_cache[fps_text] = self.font.get_text_metrics(fps_text)
            except Exception:
                # Fallback approximation
                self.metrics_cache[fps_text] = (len(fps_text) * 7, 0)
        
        metrics = self.metrics_cache[fps_text]
        
        # Draw text
        ctx.set_fill_style(ACCENT_COLOR)
        ctx.fill_text(blend2d.BLPoint(self.x - metrics[0]/2, self.y), self.font, fps_text)
        
        ctx.restore()

# HUD Renderer class to manage all individual renderers
class HudRenderer:
    """Main HUD renderer that encapsulates all individual component renderers"""
    
    def __init__(self, width, height):
        """Initialize the HUD renderer with all component renderers"""
        self.width = width
        self.height = height
        
        # Initialize component renderers
        self.compass_renderer = CompassRenderer(width, COMPASS_Y)
        self.altitude_renderer = AltitudeRenderer(width, COMPASS_Y)
        self.reticle_renderer = ReticleRenderer(width, height)
        self.ammo_counter_renderer = AmmoCounterRenderer(width, height)
        self.weapon_info_renderer = WeaponInfoRenderer(width, height)
        self.health_shield_renderer = HealthShieldRenderer(width, height)
        self.fps_counter_renderer = FpsCounterRenderer(COMPASS_Y)
        self.movement_indicator_renderer = MovementIndicatorRenderer(height)
    
    def draw_hud(self, ctx, sensor_data):
        """Draw the complete HUD with all components using their optimized renderers"""
        # Clear the canvas with the background color
        ctx.comp_op = blend2d.BLCompOp.SRC_COPY  # Use SRC_COPY for faster rendering without alpha blending
        # clear the canvas
        ctx.clear_all()

        #ctx.set_fill_style(BG_COLOR)
        #ctx.fill_all()
        
        # Draw the compass at the top
        self.compass_renderer.draw_compass(ctx, sensor_data['heading'], sensor_data['threats'])
        
        # Draw altitude text (distance to target)
        self.altitude_renderer.draw_altitude(ctx, sensor_data['altitude'])
        
        # Draw the central reticle
        self.reticle_renderer.draw_reticle(ctx, sensor_data['ammo_count'] > 0, sensor_data['firing'])
        
        # Draw the ammo counter
        self.ammo_counter_renderer.draw_ammo_counter(ctx, sensor_data['ammo_count'], 
                                                    sensor_data['ammo_max'], 
                                                    sensor_data['is_reloading'])
        
        # Draw the weapon info bar (centered at bottom)
        self.weapon_info_renderer.draw_weapon_info(ctx, sensor_data['weapon_name'], 
                                                  sensor_data['ammo_type'], 
                                                  sensor_data['ammo_count'], 
                                                  sensor_data['ammo_capacity'])
        
        # Draw health and shield bars (bottom right)
        self.health_shield_renderer.draw_health_shield(ctx, sensor_data['health'], sensor_data['shield'])
        
        # Draw movement status indicator if moving
        if sensor_data.get('is_moving', False):
            self.movement_indicator_renderer.draw_movement_indicator(ctx, sensor_data['movement_pattern'])
        
        # Draw FPS counter
        fps = sensor_data.get('fps', 0)
        self.fps_counter_renderer.draw_fps_counter(ctx, fps)

# Main HUD Manager class
class HudManager:
    """Class to manage HUD rendering onto frames, replacing global functions"""
    
    def __init__(self, width=800, height=480):
        """Initialize the HUD manager with display dimensions"""
        self.width = width
        self.height = height
        
        # Initialize blend2d image and context for rendering
        self.img = blend2d.BLImage(width, height)
        self.ctx = blend2d.BLContext(self.img)
        
        # Initialize the sensor system
        self.sensors = SensorSystem()
        self.sensors.start()
        
        # Initialize HUD renderer
        self.hud_renderer = HudRenderer(width, height)
        
        # FPS tracking
        self.fps_values = []
        self.last_fps_update = time.time()
        self.current_fps_display = 0
        
        # Create a temporary file for image transfer (if needed)
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
    
    def update_sensors(self, input_data=None):
        """Update sensor data with optional input from external sources"""
        # If input_data is provided, use it to update sensors
        if input_data:
            # Update heading if provided
            if 'heading' in input_data:
                self.sensors.set_heading(input_data['heading'])
                
            # Update altitude if provided
            if 'altitude' in input_data:
                self.sensors.set_altitude(input_data['altitude'])
                
            # Update ammo if provided
            if 'ammo_count' in input_data:
                max_ammo = input_data.get('ammo_max', None)
                self.sensors.set_ammo(input_data['ammo_count'], max_ammo)
                
            # Update health and shield if provided
            if 'health' in input_data:
                self.sensors.set_health(input_data['health'])
                
            if 'shield' in input_data:
                self.sensors.set_shield(input_data['shield'])
                
            # Update weapon info if provided
            if 'weapon_name' in input_data:
                ammo_type = input_data.get('ammo_type', None)
                self.sensors.set_weapon(input_data['weapon_name'], ammo_type)
                
            # Handle firing state
            if input_data.get('firing', False):
                self.sensors.fire_weapon()
                
            # Handle reload state
            if input_data.get('reloading', False):
                self.sensors.reload()
                
            # Update movement pattern if provided
            if 'movement_pattern' in input_data:
                self.sensors.set_movement_pattern(input_data['movement_pattern'])
        
        # Get the current sensor values
        sensor_data = self.sensors.get_values()
        
        # Add FPS information to sensor data
        sensor_data['fps'] = self.current_fps_display
        
        return sensor_data
    
    def render_hud(self, frame):
        """
        Render the HUD onto a frame
        
        Args:
            frame (numpy.ndarray): Frame to overlay HUD onto
        
        Returns:
            numpy.ndarray: Frame with HUD overlay
        """
        # Get current sensor values
        sensor_data = self.update_sensors()
        
        # Measure frame time for FPS calculation
        start_time = time.time()
        
        # Draw the HUD onto our blend2d image
        self.hud_renderer.draw_hud(self.ctx, sensor_data)
        
        # Calculate and update FPS
        frame_time = time.time() - start_time
        self._update_fps(frame_time)
        
        # Convert blend2d image to numpy array
        hud_array = self._blend2d_to_numpy()
        
        # Overlay the HUD onto the provided frame
        result_frame = self._overlay_hud(frame, hud_array)
        
        return result_frame
    
    def _blend2d_to_numpy(self):
        """Convert blend2d image to numpy array"""
        try:
            # Access raw pixel data from blend2d image
            
            img_array = self.img.getDataAsNumPy()
       
            # Convert to numpy array (assuming BGRA format)
            #img_array = np.frombuffer(img_data, dtype=np.uint8).reshape(self.height, self.width, 4)
            
            # Convert from BGRA to RGBA
            #img_array = img_array[:, :, [2, 1, 0, 3]]
            
            return img_array
        except Exception as e:
            print(f"Warning: Direct pixel access failed ({e}). Using file method instead.")
            return self._blend2d_to_numpy_using_file()
    
    def _blend2d_to_numpy_using_file(self):
        """Convert blend2d image to numpy array using temporary file"""
        import cv2
        
        # Save the blend2d image to the temporary file
        self.img.writeToFile(self.temp_file)
        
        # Read the file with OpenCV
        img_array = cv2.imread(self.temp_file, cv2.IMREAD_UNCHANGED)
        
        # Convert from BGR to RGB if needed
        if img_array.shape[2] >= 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2RGBA)
            
        return img_array
    
    def _overlay_hud(self, frame, hud_array):
        """Overlay the HUD onto the frame using alpha blending"""
        # Ensure the hud_array is the same size as the frame
        if hud_array.shape[0] != frame.shape[0] or hud_array.shape[1] != frame.shape[1]:
            import cv2
            hud_array = cv2.resize(hud_array, (frame.shape[1], frame.shape[0]))
        
        # Check if the frame is RGB or RGBA
        if frame.shape[2] == 3:
            # If the frame is RGB, create a copy to avoid modifying the original
            result_frame = frame.copy()
            
            # Alpha blending (only for visible pixels to improve performance)
            # Get alpha channel
            alpha = hud_array[:, :, 3] / 255.0
            
            # Find pixels with non-zero alpha
            mask = alpha > 0.01  # Small threshold to avoid processing transparent pixels
            
            # Apply alpha blending only to visible pixels
            for c in range(3):
                # This vectorized operation is much faster than pixel-by-pixel blending
                result_frame[:, :, c][mask] = (
                    hud_array[:, :, c][mask] * alpha[mask] + 
                    result_frame[:, :, c][mask] * (1 - alpha[mask])
                ).astype(np.uint8)
            
            return result_frame
        else:
            # For RGBA frames, handle the alpha channel as well
            result_frame = frame.copy()
            
            # Extract alpha channels
            frame_alpha = frame[:, :, 3] / 255.0
            hud_alpha = hud_array[:, :, 3] / 255.0
            
            # Calculate resulting alpha (standard alpha compositing formula)
            result_alpha = hud_alpha + frame_alpha * (1 - hud_alpha)
            
            # Find pixels with non-zero HUD alpha
            mask = hud_alpha > 0.01
            
            # Create a mask to avoid division by zero
            valid_mask = result_alpha > 0
            combined_mask = np.logical_and(mask, valid_mask)
            
            # Apply alpha blending for RGB channels
            for c in range(3):
                result_frame[:, :, c][combined_mask] = (
                    (hud_array[:, :, c][combined_mask] * hud_alpha[combined_mask] + 
                     frame[:, :, c][combined_mask] * frame_alpha[combined_mask] * 
                     (1 - hud_alpha[combined_mask])) / result_alpha[combined_mask]
                ).astype(np.uint8)
            
            # Update alpha channel
            result_frame[:, :, 3] = (result_alpha * 255).astype(np.uint8)
            
            return result_frame
    
    def _update_fps(self, frame_time):
        """Update FPS calculation"""
        # Avoid division by zero
        current_fps = 1.0 / max(frame_time, 0.000001)
        
        self.fps_values.append(current_fps)
        
        # Only keep the last 30 frames for FPS calculation
        if len(self.fps_values) > 30:
            self.fps_values.pop(0)
        
        # Update the displayed FPS value periodically
        current_time = time.time()
        if current_time - self.last_fps_update >= 0.5:  # Update every half second
            if self.fps_values:
                self.current_fps_display = statistics.mean(self.fps_values)
            else:
                self.current_fps_display = 0
            self.last_fps_update = current_time
    
    # Convenience methods to control the HUD behavior
    
    def fire_weapon(self):
        """Fire the weapon"""
        return self.sensors.fire_weapon()
    
    def reload(self):
        """Reload the weapon"""
        return self.sensors.reload()
    
    def set_movement_pattern(self, pattern):
        """Set the movement pattern"""
        self.sensors.set_movement_pattern(pattern)
    
    def set_heading(self, heading):
        """Set the heading direction"""
        self.sensors.set_heading(heading)
    
    def set_altitude(self, altitude):
        """Set the altitude/distance to target"""
        self.sensors.set_altitude(altitude)
    
    def take_damage(self, amount):
        """Take damage to health/shield"""
        self.sensors.take_damage(amount)
    
    def set_ammo(self, count, max_ammo=None):
        """Set current ammo count and optionally max ammo"""
        self.sensors.set_ammo(count, max_ammo)
    
    def add_threat(self, angle, intensity=1.0):
        """Add a threat indicator at specified angle"""
        self.sensors.add_threat(angle, intensity)
    
    def clear_threats(self):
        """Clear all threat indicators"""
        self.sensors.clear_threats()
    
    def stop(self):
        """Stop the sensor system and clean up resources"""
        if self.sensors:
            self.sensors.stop()
        
        # Remove temporary file if it exists
        import os
        if hasattr(self, 'temp_file') and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except:
                pass

def download_video(url, save_path='/tmp'):
    """
    Download a video from URL to the specified path.
    
    Args:
        url (str): The URL of the video to download
        save_path (str): Directory to save the video to
    
    Returns:
        str: Path to the downloaded video file
    """
    print(f"Downloading video from {url}...")
    
    # For Dropbox URLs, modify to get direct download
    if 'dropbox.com' in url and '?dl=0' in url:
        url = url.replace('?dl=0', '?dl=1')
    elif 'dropbox.com' in url and 'dl=0' in url:
        url = url.replace('dl=0', 'dl=1')
    
    # Get the filename from the URL
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path).split('?')[0]
    
    # If the filename doesn't have an extension, add .mp4
    if not filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        filename += '.mp4'
    
    # Complete save path
    save_path = os.path.join(save_path, filename)
    
    # Download the file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video downloaded successfully to {save_path}")
        return save_path
    else:
        print(f"Failed to download video: {response.status_code}")
        return None

# Example usage if this file is run directly
if __name__ == "__main__":
    print("Running HUD Manager demo...")
    
    # Initialize the HUD manager
    width, height = 800, 480
    hud_manager = HudManager(width, height)
    
    # Download the video from URL if provided, otherwise use local file
    video_path = "/tmp/shooting-demo.mp4"

    if not os.path.exists(video_path):
        video_url = "https://www.dropbox.com/scl/fi/ueuwy4r3u71avr3673csi/shooting-demo.mp4?rlkey=1qi90xyr1fsqkxjubher0fegd&st=2j0ndn6m&dl=1"
        video_path = download_video(video_url)
    

    
    # Create a video capture object to stream the video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        exit()
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1.0 / fps if fps > 0 else 0.033
    
    try:
        # Main loop
        frame_count = 0
        running = True
        
        while running:
            # Read a frame from the video
            ret, frame = cap.read()
            
            # If frame read was not successful, break the loop
            if not ret:
                print("End of video or error reading frame")
                break
            
            # Resize frame if needed to match HUD dimensions
            if frame.shape[0] != height or frame.shape[1] != width:
                frame = cv2.resize(frame, (width, height))
            
            # Apply HUD overlay to the frame
            result_frame = hud_manager.render_hud(frame)
            
            # Display the frame
            #cv2.imshow('HUD Demo', result_frame)
            
            # Save the current frame (optional)
            #if frame_count % 30 == 0:  # Save every 30th frame
            cv2.imwrite(f'hud.png', result_frame)
            
            frame_count += 1
            
            # Update HUD elements
            
            # Rotate heading continuously
            heading = (frame_count / 2) % 360
            hud_manager.set_heading(heading)
            
            # Add random threats occasionally
            if frame_count % 60 == 0:
                threat_angle = np.random.uniform(0, 360)
                hud_manager.add_threat(threat_angle)
            
            # Fire weapon occasionally
            if frame_count % 30 == 0:
                hud_manager.fire_weapon()
            
            # Take damage occasionally
            if frame_count % 90 == 0:
                hud_manager.take_damage(10)
            
            # Reload occasionally
            if frame_count % 120 == 0:
                hud_manager.reload()
            
            # Check for exit key
            #key = cv2.waitKey(1)
            #if key == 27:  # ESC key
            #    running = False
            
            # Limit frame rate to match video
            time.sleep(frame_delay)
    
    except KeyboardInterrupt:
        print("Program interrupted.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        hud_manager.stop()
        cap.release()
        #cv2.destroyAllWindows()
        print("HUD Demo terminated.")