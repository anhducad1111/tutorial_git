import customtkinter as ctk
from src.config.app_config import AppConfig
from src.views.button_component import ButtonComponent
import asyncio

class DeviceListHeader(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._setup_layout()
        self._create_headers()

    def _setup_layout(self):
        self.pack(fill="x")
        self.grid_columnconfigure(0, weight=1)     # Name - phần còn lại
        self.grid_columnconfigure(1, minsize=200)  # Address - cố định
        self.grid_columnconfigure(2, minsize=120)   # RSSI - nhỏ nhất

    def _create_headers(self):
        headers = ["NAME", "ADDRESS", "RSSI"]
        for i, text in enumerate(headers):
            label = ctk.CTkLabel(
                self,
                text=text,
                font=("Inter Bold", 12),
                text_color="white"
            )
            label.grid(row=0, column=i, sticky="w", padx=15, pady=10)

class ScrollableDeviceFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.command = command
        self.selected_row = None
        self.rows = []
        self.devices = {}  # Dictionary để kiểm tra trùng lặp
        self._destroyed = False

    def add_device(self, name, address, rssi):
        if self._destroyed:
            return
            
        # Kiểm tra thiết bị đã tồn tại chưa
        if address in self.devices:
            return

        row = len(self.rows)
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
        frame.grid_columnconfigure(0, weight=1)     # Name - phần còn lại
        frame.grid_columnconfigure(1, minsize=200)  # Address - cố định
        frame.grid_columnconfigure(2, minsize=100)   # RSSI - nhỏ nhất

        device_info = {"name": name, "address": address, "rssi": rssi}
        
        # Tạo các cột thông tin
        texts = [name, address, str(rssi)]
        for col, text in enumerate(texts):
            label = ctk.CTkLabel(
                frame,
                text=text,
                font=("Inter Medium", 12),
                text_color="white"
            )
            label.grid(row=0, column=col, sticky="w", padx=15, pady=5)

        # Bind sự kiện click
        frame.bind("<Button-1>", lambda e: self._on_select(row, device_info))
        for widget in frame.winfo_children():
            widget.bind("<Button-1>", lambda e: self._on_select(row, device_info))

        self.rows.append(frame)
        self.devices[address] = device_info

    def _on_select(self, row, device_info):
        if self._destroyed:
            return
            
        if self.selected_row is not None:
            self.rows[self.selected_row].configure(fg_color="transparent")
        
        self.selected_row = row
        self.rows[row].configure(fg_color=("#3D3F41", "#3D3F41"))
        
        if self.command:
            self.command(device_info)

    def clear(self):
        if self._destroyed:
            return
            
        for row in self.rows:
            row.destroy()
        self.rows.clear()
        self.devices.clear()
        self.selected_row = None

    def destroy(self):
        self._destroyed = True
        super().destroy()

class ConnectionDialog(ctk.CTkToplevel):
    def __init__(self, parent, loop, ble_scanner, callback=None):
        super().__init__(parent)
        self.loop = loop
        self.ble_scanner = ble_scanner
        self.callback = callback
        self.selected_device = None
        self._destroyed = False
        self._setup_window(parent)
        self._create_main_layout()
        self.loop.create_task(self._start_scanning())

    def _setup_window(self, parent):
        self.overrideredirect(True)
        self.configure(fg_color=("#2B2D30", "#2B2D30"))
        self.geometry("569x443")
        self._center_window(parent)
        self._make_modal(parent)

    def _center_window(self, parent):
        x = parent.winfo_rootx() + (parent.winfo_width() - 700) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - 500) // 2
        self.geometry(f"+{x}+{y}")

    def _make_modal(self, parent):
        self.transient(parent)
        self.grab_set()

    def _create_main_layout(self):
        main_frame = self._create_border_frame(self)
        content = self._create_content_frame(main_frame)
        self._create_title(content)
        self._create_device_list(content)
        self._create_bottom_section(content)

    def _create_border_frame(self, parent):
        frame = ctk.CTkFrame(
            parent,
            fg_color=("#2B2D30", "#2B2D30"),
            border_color=("#777777", "#777777"),
            border_width=1,
            corner_radius=8
        )
        frame.pack(fill="both", expand=True, padx=2, pady=2)
        return frame

    def _create_content_frame(self, parent):
        content = ctk.CTkFrame(parent, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        return content

    def _create_title(self, parent):
        title_frame = ctk.CTkFrame(parent, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        title_frame.grid_columnconfigure(1, weight=1)

        header = ctk.CTkLabel(
            title_frame,
            text="Connection",
            font=("Inter Bold", 16),
            text_color="white"
        )
        header.grid(row=0, column=0, sticky="w")

        self.scan_btn = ButtonComponent(
            title_frame,
            "Scan Again",
            command=self._on_scan_again,
            width=100,
            height=32
        )
        self.scan_btn.grid(row=0, column=2, sticky="e")

    def _create_device_list(self, parent):
        container = ctk.CTkFrame(parent, fg_color="transparent", height=294)
        container.pack(fill="x", pady=(0, 15))
        container.pack_propagate(False)

        list_frame = self._create_border_frame(container)
        content = ctk.CTkFrame(list_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=5, pady=5)

        DeviceListHeader(content)
        
        self.device_list = ScrollableDeviceFrame(
            content,
            command=self._show_device_info,
            fg_color="transparent",
            corner_radius=0,
            width=516,
            height=215
        )
        self.device_list.pack(fill="both", expand=True)

    def _create_bottom_section(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x")
        frame.grid_columnconfigure(0, weight=1)

        self._create_info_section(frame)
        self._create_button_section(frame)

    def _create_info_section(self, parent):
        self.info_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.info_frame.grid(row=0, column=0, sticky="w")
        
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Inter Medium", 12),
            text_color="white"
        )
        self.info_label.pack(anchor="w")

    def _create_button_section(self, parent):
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.grid(row=0, column=1, sticky="e")

        self.cancel_btn = ButtonComponent(
            button_frame,
            "Cancel", 
            command=self.destroy,
            fg_color="transparent",
            hover_color="gray20"
        )
        self.cancel_btn.pack(side="left", padx=(0, 20))

        self.connect_btn = ButtonComponent(
            button_frame,
            "Connect",
            command=self._on_connect,
            state="disabled",
            fg_color="#0078D4",
            hover_color="#006CBE"
        )
        self.connect_btn.pack(side="left")

    def _show_device_info(self, device_info):
        if self._destroyed:
            return
            
        info_text = f"{device_info['name']}, {device_info['address']}, {device_info['rssi']}"
        self.info_label.configure(text=info_text)
        self.connect_btn.configure(state="normal")
        self.selected_device = device_info

    async def _start_scanning(self):
        if self._destroyed:
            return
            
        self.device_list.clear()
        self.scan_btn.configure(state="disabled", text="Scanning...")
        
        async def detection_callback(device, advertisement_data):
            if not self._destroyed and device.name:  # Only add devices with names
                self.after(0, lambda: self.device_list.add_device(
                    device.name,
                    device.address,
                    advertisement_data.rssi
                ))

        try:
            async with self.ble_scanner(detection_callback) as scanner:
                await asyncio.sleep(5)  # Scan for 5 seconds
                
            if not self._destroyed:
                self.scan_btn.configure(state="normal", text="Scan Again")
        except Exception as e:
            print(f"Scan error: {e}")  # Added for debugging
            if not self._destroyed:
                self.scan_btn.configure(state="normal", text="Scan Again")

    def _on_scan_again(self):
        if self._destroyed:
            return
            
        self.info_label.configure(text="")
        self.connect_btn.configure(state="disabled")
        self.selected_device = None
        self.loop.create_task(self._start_scanning())

    def _on_connect(self):
        if self._destroyed:
            return
            
        if self.selected_device and self.callback:
            self.callback(self.selected_device)
        self.destroy()

    def destroy(self):
        self._destroyed = True
        super().destroy()
