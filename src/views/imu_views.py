from src.views.base_imu_view import BaseIMUView

class IMU1View(BaseIMUView):
    """IMU1 View implementation"""
    def __init__(self, parent):
        super().__init__(parent, "IMU 1")
        

class IMU2View(BaseIMUView):
    """IMU2 View implementation"""  
    def __init__(self, parent):
        super().__init__(parent, "IMU 2")

    