import struct

class IMUData:
    """Model class representing IMU sensor data"""
    
    def __init__(self, accel_x=0, accel_y=0, accel_z=0, 
                 gyro_x=0, gyro_y=0, gyro_z=0,
                 mag_x=0, mag_y=0, mag_z=0, raw_data=None):
        # Accelerometer data
        self.accel = {
            'x': accel_x,
            'y': accel_y,
            'z': accel_z
        }
        
        # Gyroscope data
        self.gyro = {
            'x': gyro_x,
            'y': gyro_y,
            'z': gyro_z
        }
        
        # Magnetometer data
        self.mag = {
            'x': mag_x,
            'y': mag_y,
            'z': mag_z
        }
        
        # Raw binary data
        self.raw_data = raw_data
        
    @classmethod
    def from_bytes(cls, data):
        """Create IMUData object from byte array"""
        if not data or len(data) != 18:  # 9 int16 values
            return None
            
        try:
            values = struct.unpack('<9h', data)
            return cls(
                accel_x=values[0], accel_y=values[1], accel_z=values[2],
                gyro_x=values[3], gyro_y=values[4], gyro_z=values[5],
                mag_x=values[6], mag_y=values[7], mag_z=values[8],
                raw_data=data
            )
        except Exception as e:
            print(f"Error parsing IMU data: {e}")
            return None
            
    def to_hex_string(self):
        """Convert raw data to hex string representation"""
        if not self.raw_data:
            return ""
        return ' '.join(f'{b:02x}' for b in self.raw_data)
        
    def get_debug_text(self):
        """Get formatted debug text"""
        hex_str = self.to_hex_string()
        debug_text = f"Raw data ({len(self.raw_data)} bytes):\n{hex_str}\n\n"
        debug_text += f"Parsed values:\n"
        debug_text += f"Accel: ({self.accel['x']}, {self.accel['y']}, {self.accel['z']})\n"
        debug_text += f"Gyro: ({self.gyro['x']}, {self.gyro['y']}, {self.gyro['z']})\n"
        debug_text += f"Mag: ({self.mag['x']}, {self.mag['y']}, {self.mag['z']})"
        return debug_text