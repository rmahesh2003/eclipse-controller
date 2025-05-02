# Advanced Time-Lapse Photography Controller

A sophisticated Python-based time-lapse photography controller that provides advanced features for professional and amateur photographers alike.

> **Note:** This project will soon be expanded into a full-featured web application with additional capabilities and a user-friendly interface.

## Features

- **Multiple Shooting Modes**
  - Day mode
  - Night mode
  - Sunrise mode
  - Sunset mode
  - Custom mode

- **Advanced Camera Control**
  - Automatic exposure bracketing
  - Dynamic interval adjustment
  - White balance control
  - Multiple exposure settings for different conditions
  - Manual focus verification

- **Progress Tracking**
  - Real-time progress bar
  - Voice announcements
  - Error handling and graceful shutdown
  - Automatic file organization

## Requirements

- Python 3.x
- gphoto2
- festival (for voice announcements)
- tqdm (for progress bars)

## Installation

1. Install the required dependencies:

```bash
# On macOS
brew install gphoto2 festival

# On Ubuntu/Debian
sudo apt-get install gphoto2 festival

# Install Python dependencies
pip install tqdm
```

2. Clone this repository:
```bash
git clone https://github.com/yourusername/timelapse-controller.git
cd timelapse-controller
```

## Usage

1. Configure your settings in the `main()` function:
   - `TARGET_DIR`: Where to save the photos
   - `DURATION_HOURS`: How long to run the time-lapse
   - `MODE`: Which shooting mode to use (DAY, NIGHT, SUNRISE, SUNSET, or CUSTOM)

2. Run the script:
```bash
python3 timelapse_controller.py
```

## Upcoming Features (Web Version)

- Web-based interface for remote control
- Real-time camera preview
- Cloud storage integration
- Advanced scheduling system
- Weather condition monitoring
- Mobile app companion
- Social media integration
- Advanced post-processing options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

NO WARRANTY ON THIS SCRIPT. USE AT YOUR OWN RISK. The developers are not responsible for any damage to equipment or loss of data.

## Support

For support, please open an issue in the GitHub repository or contact the development team.

---

*This project is actively maintained and will be expanded into a full web application in the near future. Stay tuned for updates!* 