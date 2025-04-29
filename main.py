import threading
import speedtest
import tkinter as tk
from ttkbootstrap import Style, Window
from ttkbootstrap.widgets import Meter, Frame, Label
from ttkbootstrap.constants import *

class NovaSpeedTestPro:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ NOVA SPEEDTEST PRO")
        self.root.geometry("1000x670")
        # self.root.resizable(False, False)
        
        # Ultra Modern Style
        self.style = Style(theme="superhero")
        self.style.configure("TButton", font=("Poppins", 12, "bold"), padding=10)
        
        # Main App Container
        self.main_container = Frame(root, bootstyle="dark")
        self.main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Header with Glow Effect
        self.header_frame = Frame(self.main_container, bootstyle="dark")
        self.header_frame.pack(fill=X, pady=(0, 20))
        
        self.header_label = Label(
            self.header_frame,
            text="⚡ NOVA SPEEDTEST PRO",
            font=("Poppins", 26, "bold"),
            bootstyle="light"
        )
        self.header_label.pack(side=LEFT)
        
        # Version Badge
        self.version_badge = Label(
            self.header_frame,
            text="v2.0 PREMIUM",
            font=("Poppins", 10, "bold"),
            bootstyle="success",
            padding=(10, 2)
        )
        self.version_badge.pack(side=RIGHT, padx=5)
        
        # Metrics Dashboard (Horizontal Layout)
        self.dashboard = Frame(self.main_container, bootstyle="dark")
        self.dashboard.pack(fill=X, pady=10)
        
        # Download Speed Card
        self.download_card = Frame(self.dashboard, bootstyle="dark")
        self.download_card.grid(row=0, column=0, padx=15, sticky="nsew")
        
        Label(
            self.download_card,
            text="DOWNLOAD",
            font=("Poppins", 14, "bold"),
            bootstyle="light"
        ).pack(pady=(0, 5))
        
        self.download_meter = Meter(
            self.download_card,
            bootstyle="success",
            subtext="Mbps",
            amountused=0,
            amounttotal=1000,
            metersize=200,
            metertype="semi",
            stripethickness=10,
            interactive=False,
            padding=20
        )
        self.download_meter.pack()
        
        self.download_value = Label(
            self.download_card,
            text="0.00 Mbps",
            font=("Poppins", 18, "bold"),
            bootstyle="success"
        )
        self.download_value.pack(pady=5)
        
        # Upload Speed Card
        self.upload_card = Frame(self.dashboard, bootstyle="dark")
        self.upload_card.grid(row=0, column=1, padx=15, sticky="nsew")
        
        Label(
            self.upload_card,
            text="UPLOAD",
            font=("Poppins", 14, "bold"),
            bootstyle="light"
        ).pack(pady=(0, 5))
        
        self.upload_meter = Meter(
            self.upload_card,
            bootstyle="info",
            subtext="Mbps",
            amountused=0,
            amounttotal=500,
            metersize=200,
            metertype="semi",
            stripethickness=10,
            interactive=False,
            padding=20
        )
        self.upload_meter.pack()
        
        self.upload_value = Label(
            self.upload_card,
            text="0.00 Mbps",
            font=("Poppins", 18, "bold"),
            bootstyle="info"
        )
        self.upload_value.pack(pady=5)
        
        # Ping & Jitter Card
        self.ping_card = Frame(self.dashboard, bootstyle="dark")
        self.ping_card.grid(row=0, column=2, padx=15, sticky="nsew")
        
        Label(
            self.ping_card,
            text="LATENCY",
            font=("Poppins", 14, "bold"),
            bootstyle="light"
        ).pack(pady=(0, 5))
        
        self.ping_display = Label(
            self.ping_card,
            text="--",
            font=("Poppins", 36, "bold"),
            bootstyle="warning"
        )
        self.ping_display.pack(pady=5)
        
        Label(
            self.ping_card,
            text="ms",
            font=("Poppins", 12),
            bootstyle="light"
        ).pack()
        
        # Start Test Button (Neon Style)
        self.button_frame = Frame(self.main_container, bootstyle="dark")
        self.button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(
            self.button_frame,
            text="🚀 START SPEED TEST",
            command=self.start_speedtest,
            bg="#6C5CE7",
            fg="white",
            font=("Poppins", 14, "bold"),
            bd=0,
            padx=30,
            pady=12,
            activebackground="#5649C0",
            activeforeground="white",
            relief="flat",
            highlightthickness=0,
            cursor="hand2"
        )
        self.start_btn.pack()
        
        # Status Bar (Glass Effect)
        self.status_bar = Frame(self.main_container, bootstyle="dark")
        self.status_bar.pack(fill=X, pady=(10, 0))
        
        self.status_label = Label(
            self.status_bar,
            text="Ready to test your internet speed",
            font=("Poppins", 10),
            bootstyle="inverse-dark",
            anchor="center",
            padding=10
        )
        self.status_label.pack(fill=X)

    def start_speedtest(self):
        self.start_btn.config(state=DISABLED, text="⏳ TESTING...", bg="#4B4B4B")
        self.status_label.config(text="Finding optimal server... Please wait")
        threading.Thread(target=self.run_speedtest, daemon=True).start()
    def animate_meter(self, meter, target_value, current_value=0, step=5):
        if current_value < target_value:
            meter.configure(amountused=current_value)
            current_value += step
            meter.after(10, lambda: self.animate_meter(meter, target_value, current_value, step))
        else:
            meter.configure(amountused=target_value)
    def run_speedtest(self):
        try:
            st = speedtest.Speedtest()
            self.status_label.config(text="🔍 Finding best server...")
            st.get_best_server()
            
            self.status_label.config(text="📥 Measuring download speed...")
            download_speed = st.download() / 1_000_000
            self.animate_meter(self.download_meter, download_speed)
            self.download_value.config(text=f"{download_speed:.2f} Mbps")
            
            self.status_label.config(text="📤 Measuring upload speed...")
            upload_speed = st.upload() / 1_000_000
            self.animate_meter(self.upload_meter, upload_speed)
            self.upload_value.config(text=f"{upload_speed:.2f} Mbps")
            
            ping_result = st.results.ping
            self.ping_display.config(text=f"{int(ping_result)}")
            
            self.status_label.config(text="✅ Test completed successfully!")
            
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}")
        finally:
            self.start_btn.config(state=NORMAL, text="🔄 RUN AGAIN", bg="#6C5CE7")

if __name__ == "__main__":
    root = Window(title="Nova SpeedTest Pro", themename="superhero")
    app = NovaSpeedTestPro(root)
    root.mainloop()