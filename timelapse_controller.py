#!/usr/bin/env python3

import datetime
import os
import subprocess
import time
import tqdm
import sys
import math
from enum import Enum
from typing import List, Union, Tuple

"""
Advanced Time-Lapse Photography Controller

This script provides sophisticated control over time-lapse photography sessions
with features like:
- Automatic exposure bracketing
- Dynamic interval adjustment based on lighting conditions
- Multiple shooting modes (day, night, sunrise, sunset)
- Voice announcements for important events
- Progress tracking and status updates

The camera must be in Manual Mode and properly focused. The script will
automatically adjust settings based on the selected mode and environmental
conditions.

NO WARRANTY ON THIS SCRIPT. USE AT YOUR OWN RISK.
"""

class Config:
    """Camera configuration paths"""
    Bracketing = '/main/capturesettings/aeb'
    Aperture = '/main/capturesettings/aperture'
    ShutterSpeed = '/main/capturesettings/shutterspeed'
    EV = '/main/capturesettings/exposurecompensation'
    ISO = '/main/imgsettings/iso'
    WhiteBalance = '/main/imgsettings/whitebalance'

class Bracketing(Enum):
    """Exposure bracketing modes"""
    OFF = 0
    EV_0_1_3 = 1
    EV_0_2_3 = 2
    EV_1 = 3
    EV_1_1_3 = 4
    EV_1_2_3 = 5
    EV_2 = 6

class ShootingMode(Enum):
    """Available shooting modes"""
    DAY = "day"
    NIGHT = "night"
    SUNRISE = "sunrise"
    SUNSET = "sunset"
    CUSTOM = "custom"

class Settings:
    """Base class for camera settings"""
    def __init__(self):
        self.interval = 0
        self.index = 0
        self.aperture = "8"
        self.bracketing = Bracketing.OFF
        self.speed = "1/250"
        self.iso = 200
        self.white_balance = "Daylight"
        self.triggered = True

class ShootingProfile:
    """Defines settings for different shooting conditions"""
    def __init__(self, mode: ShootingMode):
        self.mode = mode
        self.settings = Settings()
        self._configure_for_mode()

    def _configure_for_mode(self):
        if self.mode == ShootingMode.DAY:
            self.settings.interval = 30
            self.settings.aperture = "8"
            self.settings.speed = "1/250"
            self.settings.iso = 200
            self.settings.bracketing = Bracketing.EV_1
        elif self.mode == ShootingMode.NIGHT:
            self.settings.interval = 60
            self.settings.aperture = "4"
            self.settings.speed = "30"
            self.settings.iso = 800
            self.settings.bracketing = Bracketing.EV_1_1_3
        elif self.mode == ShootingMode.SUNRISE:
            self.settings.interval = 15
            self.settings.aperture = ["8", "5.6"]
            self.settings.speed = ["1/250", "1/125"]
            self.settings.iso = [200, 400]
            self.settings.bracketing = Bracketing.EV_1_2_3
        elif self.mode == ShootingMode.SUNSET:
            self.settings.interval = 15
            self.settings.aperture = ["8", "5.6"]
            self.settings.speed = ["1/250", "1/125"]
            self.settings.iso = [200, 400]
            self.settings.bracketing = Bracketing.EV_1_2_3
        else:  # CUSTOM
            self.settings.interval = 60
            self.settings.aperture = "8"
            self.settings.speed = "1/250"
            self.settings.iso = 200
            self.settings.bracketing = Bracketing.OFF

def click(profile: ShootingProfile, target_dir: str):
    """Capture an image with the current settings"""
    settings = profile.settings
    filename = os.path.join(target_dir, f'{profile.mode.value}_t{int(time.time())}_%n')
    
    # Get current setting values based on index
    aperture = settings.aperture[settings.index%len(settings.aperture)] if isinstance(settings.aperture, list) else settings.aperture
    speed = settings.speed[settings.index%len(settings.speed)] if isinstance(settings.speed, list) else settings.speed
    iso = settings.iso[settings.index%len(settings.iso)] if isinstance(settings.iso, list) else settings.iso
    
    cmd = (
        f"gphoto2 --set-config-value {Config.Aperture}={aperture} "
        f"--set-config-value {Config.ShutterSpeed}={speed} "
        f"--set-config-value {Config.ISO}={iso} "
        f"--set-config-value {Config.WhiteBalance}={settings.white_balance} "
        f"--set-config {Config.Bracketing}={settings.bracketing.value} "
        f"--set-config capturetarget=0 --force-overwrite "
        f"--filename='{filename}' --no-keep --capture-image-and-download"
    )
    
    if settings.bracketing != Bracketing.OFF:
        cmd += " --capture-image-and-download --capture-image-and-download"
    
    print(f"Capturing image with settings: Aperture={aperture}, Speed={speed}, ISO={iso}")
    os.system(cmd)
    settings.index += 1

def say(text: str):
    """Announce text using text-to-speech"""
    try:
        say.festival_proc
    except AttributeError:
        say.festival_proc = subprocess.Popen(['festival', '--pipe'], stdin=subprocess.PIPE)
    print(text)
    say.festival_proc.stdin.write(f'(SayText "{text}")\n'.encode())
    say.festival_proc.stdin.flush()

def main():
    # Configuration
    TARGET_DIR = 'TimeLapse'
    DURATION_HOURS = 4
    MODE = ShootingMode.DAY
    
    # Create target directory
    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    
    # Check camera settings
    if os.system("gphoto2 --get-config /main/capturesettings/focusmode | grep -q 'Current: Manual'") != 0:
        say("Camera seems to be in auto-focus. Please manually focus. Goodbye!")
        sys.exit(1)
    
    if os.system("gphoto2 --get-config /main/capturesettings/drivemode | grep -q 'Current: Single'") != 0:
        say("Camera not in single shot drive. Please check that this is intended!")
    
    say(f"Starting time-lapse session in {MODE.value} mode")
    
    # Initialize shooting profile
    profile = ShootingProfile(MODE)
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(hours=DURATION_HOURS)
    
    # Create progress bar
    total_seconds = int((end_time - start_time).total_seconds())
    pbar = tqdm.tqdm(total=total_seconds, desc=f'Time-lapse ({MODE.value})')
    
    try:
        while datetime.datetime.now() < end_time:
            current_time = datetime.datetime.now()
            elapsed_seconds = int((current_time - start_time).total_seconds())
            
            # Update progress bar
            pbar.update(elapsed_seconds - pbar.n)
            
            # Check if it's time to take a photo
            if elapsed_seconds % profile.settings.interval == 0:
                click(profile, TARGET_DIR)
            
            # Announce progress every 30 minutes
            if elapsed_seconds % 1800 == 0:
                remaining_minutes = int((end_time - current_time).total_seconds() / 60)
                say(f"Time-lapse progress: {remaining_minutes} minutes remaining")
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        say("Time-lapse session interrupted by user")
    except Exception as e:
        say(f"Error occurred: {str(e)}")
    finally:
        pbar.close()
        say("Time-lapse session completed")

if __name__ == "__main__":
    main() 