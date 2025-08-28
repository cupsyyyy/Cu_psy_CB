import math
import random
import time
import numpy as np

class WindMouse:
    """
    WindMouse algorithm for human-like mouse movement.
    Based on the original WindMouse algorithm with enhancements for smoothness.
    """
    
    def __init__(self):
        self.last_x = 0
        self.last_y = 0
        self.last_time = time.time()
        
    def wind_mouse(self, start_x, start_y, dest_x, dest_y, gravity, wind, 
                   min_wait, max_wait, max_step, target_area):
        """
        Generate human-like mouse movement path from start to destination.
        """
        current_x, current_y = float(start_x), float(start_y)
        velocity_x = velocity_y = wind_x = wind_y = 0.0
        path = []
        
        # Debug print
        print(f"[DEBUG] WindMouse: Moving from ({start_x}, {start_y}) to ({dest_x}, {dest_y})")
        print(f"[DEBUG] WindMouse params: gravity={gravity}, wind={wind}, max_step={max_step}")
        
        while True:
            # Calculate distance to target
            distance = math.sqrt((dest_x - current_x) ** 2 + (dest_y - current_y) ** 2)
            
            # Break if we're close enough to target
            if distance < target_area:
                break
                
            # Update wind (random force)
            wind_x = wind_x / math.sqrt(3) + (random.random() - 0.5) * wind * 2
            wind_y = wind_y / math.sqrt(3) + (random.random() - 0.5) * wind * 2
            
            # Calculate gravitational pull towards target
            if distance > 1:
                gravity_x = gravity * (dest_x - current_x) / distance
                gravity_y = gravity * (dest_y - current_y) / distance
            else:
                gravity_x = gravity_y = 0
                
            # Update velocity with wind and gravity
            velocity_x += wind_x + gravity_x
            velocity_y += wind_y + gravity_y
            
            # Apply drag/friction
            velocity_x *= 0.99
            velocity_y *= 0.99
            
            # Limit maximum step size
            step_size = math.sqrt(velocity_x ** 2 + velocity_y ** 2)
            if step_size > max_step:
                velocity_x = (velocity_x / step_size) * max_step
                velocity_y = (velocity_y / step_size) * max_step
            
            # Calculate next position
            next_x = current_x + velocity_x
            next_y = current_y + velocity_y
            
            # Add some micro-corrections and overshooting
            if distance < 50:
                # Add slight randomness when close to target
                next_x += (random.random() - 0.5) * 2
                next_y += (random.random() - 0.5) * 2
            
            # Calculate delay for this step (human-like timing)
            delay = random.uniform(min_wait, max_wait)
            
            # Add to path
            path.append((int(next_x - current_x), int(next_y - current_y), delay))
            
            current_x, current_y = next_x, next_y
            
            # Safety break to prevent infinite loops
            if len(path) > 200:  # Reduced from 500
                break
                
        print(f"[DEBUG] WindMouse generated {len(path)} movement steps")
        return path

class SmoothAiming:
    """
    Advanced smooth aiming system with multiple humanization techniques.
    """
    
    def __init__(self):
        self.windmouse = WindMouse()
        self.last_target = None
        self.target_history = []
        self.aim_fatigue = 0.0
        self.reaction_delay = 0.0
        self.last_reaction_time = 0
        
    def calculate_smooth_path(self, dx, dy, config):
        """
        Calculate smooth movement path to target using configured settings.
        """
        current_time = time.time()
        
        print(f"[DEBUG] SmoothAiming: Target at ({dx:.1f}, {dy:.1f})")
        
        # Skip if movement is too small
        distance = math.sqrt(dx**2 + dy**2)
        if distance < 2:
            print("[DEBUG] SmoothAiming: Target too close, skipping")
            return []
        
        # Human reaction time simulation
        if self.last_target is None or self._target_changed(dx, dy):
            self.reaction_delay = random.uniform(config.smooth_reaction_min, config.smooth_reaction_max)
            self.last_target = (dx, dy)
            self.last_reaction_time = current_time
            print(f"[DEBUG] SmoothAiming: New target, reaction delay: {self.reaction_delay:.3f}s")
            
        # Check if we're still in reaction delay
        if current_time - self.last_reaction_time < self.reaction_delay:
            remaining_delay = self.reaction_delay - (current_time - self.last_reaction_time)
            print(f"[DEBUG] SmoothAiming: Still in reaction delay, {remaining_delay:.3f}s remaining")
            return [(0, 0, min(remaining_delay, 0.05))]  # Return small delay chunk
        
        # Dynamic speed based on distance (closer = slower)
        if distance < config.smooth_close_range:
            speed_multiplier = config.smooth_close_speed
        elif distance > config.smooth_far_range:
            speed_multiplier = config.smooth_far_speed
        else:
            # Interpolate between close and far speeds
            ratio = (distance - config.smooth_close_range) / (config.smooth_far_range - config.smooth_close_range)
            speed_multiplier = config.smooth_close_speed + ratio * (config.smooth_far_speed - config.smooth_close_speed)
        
        print(f"[DEBUG] SmoothAiming: Distance={distance:.1f}, Speed multiplier={speed_multiplier:.2f}")
        
        # Apply fatigue (longer aiming = more shaky)
        self.aim_fatigue = min(self.aim_fatigue + 0.01, 1.0)
        fatigue_shake = self.aim_fatigue * config.smooth_fatigue_effect
        
        # Calculate WindMouse parameters based on config
        gravity = config.smooth_gravity + random.uniform(-1, 1)
        wind = config.smooth_wind + fatigue_shake + random.uniform(-0.5, 0.5)
        
        # Dynamic step size based on distance and speed
        max_step = distance * speed_multiplier * config.smooth_max_step_ratio
        max_step = max(config.smooth_min_step, min(max_step, config.smooth_max_step))
        
        # Target area (stop when close enough)
        target_area = max(2, distance * config.smooth_target_area_ratio)
        
        print(f"[DEBUG] SmoothAiming: Using gravity={gravity:.1f}, wind={wind:.1f}, max_step={max_step:.1f}")
        
        # Generate movement path
        path = self.windmouse.wind_mouse(
            0, 0, dx, dy,
            gravity=gravity,
            wind=wind,
            min_wait=config.smooth_min_delay,
            max_wait=config.smooth_max_delay,
            max_step=max_step,
            target_area=target_area
        )
        
        # Apply smoothing and filtering
        filtered_path = self._apply_smoothing_filters(path, config)
        print(f"[DEBUG] SmoothAiming: Generated {len(filtered_path)} final movements")
        return filtered_path
    
    def _target_changed(self, dx, dy, threshold=10):
        """Check if target has changed significantly."""
        if self.last_target is None:
            return True
        
        last_dx, last_dy = self.last_target
        change = math.sqrt((dx - last_dx)**2 + (dy - last_dy)**2)
        return change > threshold
    
    def _apply_smoothing_filters(self, path, config):
        """Apply additional smoothing and humanization to the movement path."""
        if len(path) < 2:
            return path
        
        smoothed_path = []
        
        # Apply acceleration/deceleration curves
        for i, (dx, dy, delay) in enumerate(path):
            progress = i / len(path)
            
            # Ease-in-out curve for more natural acceleration
            if progress < 0.3:
                # Acceleration phase
                multiplier = self._ease_in(progress / 0.3) * config.smooth_acceleration
            elif progress > 0.7:
                # Deceleration phase  
                multiplier = self._ease_out((progress - 0.7) / 0.3) * config.smooth_deceleration
            else:
                # Constant speed phase
                multiplier = 1.0
            
            # Apply micro-corrections and jitter
            if config.smooth_micro_corrections > 0 and random.random() < 0.1:
                dx += random.randint(-config.smooth_micro_corrections, config.smooth_micro_corrections)
                dy += random.randint(-config.smooth_micro_corrections, config.smooth_micro_corrections)
            
            # Scale movement
            final_dx = int(dx * multiplier)
            final_dy = int(dy * multiplier)
            
            # Add slight delay variation
            final_delay = delay * random.uniform(0.8, 1.2)
            
            if final_dx != 0 or final_dy != 0:  # Only add non-zero movements
                smoothed_path.append((final_dx, final_dy, final_delay))
        
        return smoothed_path
    
    def _ease_in(self, t):
        """Ease-in function for smooth acceleration."""
        return t * t
    
    def _ease_out(self, t):
        """Ease-out function for smooth deceleration."""
        return 1 - (1 - t) * (1 - t)
    
    def reset_fatigue(self):
        """Reset aim fatigue (call when not aiming for a while)."""
        self.aim_fatigue = max(0, self.aim_fatigue - 0.1)

# Global smooth aiming instance
smooth_aimer = SmoothAiming()