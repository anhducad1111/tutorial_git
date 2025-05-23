# BLE Monitor

GUI application to monitor BLE devices with IMU sensors

## Requirements
- Python 3.10+
- Packages in requirements.txt

## Installation

1. Install Python dependencies:
```
pip install -r requirements.txt
```

2. Font requirements:
- Primary: Inter font family
- Fallback: System default sans-serif font

## Supported BLE Devices
- ESP32 with IMU sensors
- Custom BLE protocol for IMU data
- Timestamp synchronization support

## Usage
1. Run the application:
```
python main.py
```

2. Click "Connect Device" to scan for BLE devices
3. Select device from list and click "Connect"
4. Use IMU controls to read/monitor sensor data
5. Use timestamp controls to sync device time

## Features
- Device scanning and connection
- IMU sensor monitoring (Accelerometer, Gyroscope, Magnetometer)
- Device timestamp synchronization  
- Real-time data notifications
- Clean and modern dark theme UI

## IMU Data Format
- Accelerometer: ±2000 mg
- Gyroscope: ±2.00 rad/s
- Magnetometer: ±50 uT
- 18 bytes total (9 int16 values)

## Timestamp Format
- 64-bit Unix timestamp
- Microsecond precision
- UTC time zone

## Known Issues
1. Font fallback may occur if Inter font not installed
2. Some BLE devices may not be detected on first scan
3. Need to restart app if connection lost unexpectedly

## Troubleshooting
1. Device not found:
   - Try scanning multiple times
   - Check device is powered on
   - Verify device name is visible

2. Connection failed:
   - Ensure device is in range
   - Restart device and try again
   - Check device supports required services

3. Data errors:
   - Verify sensor calibration
   - Check for interference
   - Ensure stable connection

## Development
- Python 3.10+ required
- Uses customtkinter for modern UI
- Bleak for BLE communication
- Asyncio for async operations

## Contributing
1. Fork repository
2. Create feature branch
3. Submit pull request

## License
MIT License
