class AppConfig:
    """Configuration settings for the BLE Monitor application"""

    # Application settings
    APP_VERSION = "1.0.0"
    
    # Display scaling
    DISPLAY_SCALING = 0.9
    WINDOW_SCALING = 0.9

    # Window settings
    WINDOW_TITLE = "BLE Monitor"
    WINDOW_WIDTH = 1700
    WINDOW_HEIGHT = 900
    WINDOW_MAXIMIZED = True
    WINDOW_PADDING = 24

    # Info Panel dimensions
    INFO_PANEL_WIDTH = 1636
    INFO_PANEL_HEIGHT = 116

    # Theme colors
    APPEARANCE_MODE = "dark"
    BACKGROUND_COLOR = "#1F1F1F"
    PANEL_COLOR = "#2B2D30"
    BORDER_COLOR = "#373737"
    BUTTON_COLOR = "#0078D4"
    BUTTON_HOVER_COLOR = "#0063AD"  
    DISCONNECT_COLOR = "darkred"
    DISCONNECT_HOVER_COLOR = "#8B0000"
    TEXT_COLOR = "white"
    LABEL_COLOR = "#DEDEDE"
    TEXTBOX_COLOR = "#373737"
    FRAME_BG = "#5D5D5D"

    # Typography
    FONT_FAMILY = "Inter"
    FONT_SIZE_HEADER = 16
    FONT_SIZE_NORMAL = 12
    
    FONT_WEIGHT_NORMAL = "normal"
    FONT_WEIGHT_BOLD = "bold"
    
    HEADER_FONT = (FONT_FAMILY + " Bold", FONT_SIZE_HEADER)
    LABEL_FONT = (FONT_FAMILY, FONT_SIZE_NORMAL)
    VALUE_FONT = (FONT_FAMILY + " Bold", FONT_SIZE_NORMAL)
    TEXT_FONT = (FONT_FAMILY, FONT_SIZE_NORMAL)
    BUTTON_FONT = (FONT_FAMILY, FONT_SIZE_NORMAL)
    
    # Component styling
    BORDER_WIDTH = 1
    CORNER_RADIUS = 8
    BUTTON_CORNER_RADIUS = 8  
    
    # Button dimensions
    BUTTON_WIDTH = 112
    BUTTON_HEIGHT = 38

    # Value display
    VALUE_DISPLAY_HEIGHT = 30
    VALUE_DISPLAY_WIDTH = 100
