from abc import ABC, abstractmethod

class IMUViewInterface(ABC):
    """Interface for IMU data display views"""
    
    @abstractmethod
    def update_accel(self, x, y, z):
        """Update accelerometer values"""
        pass
        
    @abstractmethod
    def update_gyro(self, x, y, z):
        """Update gyroscope values"""
        pass
        
    @abstractmethod
    def update_magn(self, x, y, z):
        """Update magnetometer values"""
        pass
        
    @abstractmethod
    def update_debug_text(self, text):
        """Update debug text display"""
        pass
    
    @abstractmethod
    def set_button_states(self, enabled):
        """Enable/disable buttons"""
        pass

class ConnectionViewInterface(ABC):
    """Interface for connection-related UI"""
    
    @abstractmethod
    def update_connection_status(self, connected, device_info=None, message=""):
        """Update connection status display"""
        pass
    
    @abstractmethod
    def clear_displays(self):
        """Clear all displays"""
        pass

class TimestampViewInterface(ABC):
    """Interface for timestamp display"""
    
    @abstractmethod
    def update_timestamp_display(self, formatted_text):
        """Update timestamp display with formatted text"""
        pass
    
    @abstractmethod
    def set_button_states(self, enabled):
        """Enable/disable timestamp buttons"""
        pass

class ConnectionStatusViewInterface(ABC):
    """Interface for connection status dialog"""
    
    @abstractmethod
    def show_connecting(self):
        """Show connecting state"""
        pass
        
    @abstractmethod
    def show_connected(self, device_info):
        """Show connected state with device info"""
        pass
        
    @abstractmethod
    def show_failed(self):
        """Show connection failed state"""
        pass
        
    @abstractmethod
    def on_ok_clicked(self, callback):
        """Set callback for when OK button is clicked"""
        pass

class ConnectionDialogInterface(ABC):
    """Interface for connection dialog"""
    
    @abstractmethod
    def show_scanning(self):
        """Show scanning state"""
        pass
    
    @abstractmethod
    def add_device(self, name, address, rssi):
        """Add a discovered device to the list"""
        pass
    
    @abstractmethod
    def show_scan_complete(self, device_count):
        """Show scan completion state"""
        pass
    
    @abstractmethod
    def on_device_selected(self, callback):
        """Set callback for when a device is selected"""
        pass
    
    @abstractmethod
    def on_connect_clicked(self, callback):
        """Set callback for when connect button is clicked"""
        pass
