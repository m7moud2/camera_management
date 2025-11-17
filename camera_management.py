import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
import json
import os
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import io
import base64
from typing import Dict, List, Optional, Any
import threading
import time

# ==================== AI THEME COLORS ====================
COLORS = {
    'bg_dark': '#0a0e27',
    'bg_sidebar': '#151a35',
    'bg_card': '#1a1f3a',
    'bg_input': '#242b4a',
    'text_primary': '#ffffff',
    'text_secondary': '#a8b2d1',
    'accent_cyan': '#00d4ff',
    'accent_purple': '#9d4edd',
    'accent_green': '#06ffa5',
    'accent_red': '#ff6b6b',
    'accent_orange': '#ffa500',
    'accent_yellow': '#ffd700',
    'border': '#2d3561',
    'hover': '#2a3150',
    'success': '#10b981',
    'warning': '#f59e0b',
    'info': '#3b82f6',
}

# ==================== TRANSLATIONS ====================
TRANSLATIONS = {
    'en': {
        'app_title': 'AI Camera Management System',
        'dashboard': 'Dashboard',
        'cameras': 'All Cameras',
        'add_camera': 'Add Camera',
        'statistics': 'Analytics',
        'settings': 'Settings',
        'step_1': 'Basic Info',
        'step_2': 'Area Details',
        'step_3': 'Features',
        'step_4': 'Technical',
        'step_5': 'Review',
        'next': 'Next',
        'previous': 'Previous',
        'save': 'Save Camera',
        'edit': 'Edit',
        'delete': 'Delete',
        'search': 'Search',
        'filter': 'Filter',
        'source_id': 'Source ID',
        'brand': 'Brand',
        'rtsp_area': 'RTSP Area',
        'feature_1': 'Feature 1',
        'feature_2': 'Feature 2',
        'feature_3': 'Feature 3',
        'feature_4': 'Feature 4',
        'feature_5': 'Feature 5',
        'screenshot': 'Screenshot',
        'ip_user_pass': 'IP/User/Pass',
        'working_hours': 'Working Hours',
        'non_working_hours': 'Non-Working Hours',
        'layout_missing': 'Layout Missing',
        'serial_ws': 'Serial WS',
        'layout_file': 'Layout File',
        'total_cameras': 'Total Cameras',
        'active': 'Active',
        'inactive': 'Inactive',
        'error': 'Error',
        'success': 'Success',
        'warning': 'Warning',
        'confirm': 'Confirm',
        'yes': 'YES',
        'no': 'NO',
        'export': 'Export Excel',
        'import': 'Import Excel',
        'backup': 'Backup Data',
        'restore': 'Restore Data',
        'refresh': 'Refresh',
    },
    'ar': {
        'app_title': 'نظام إدارة الكاميرات بالذكاء الاصطناعي',
        'dashboard': 'لوحة التحكم',
        'cameras': 'جميع الكاميرات',
        'add_camera': 'إضافة كاميرا',
        'statistics': 'التحليلات',
        'settings': 'الإعدادات',
        'step_1': 'معلومات أساسية',
        'step_2': 'تفاصيل المنطقة',
        'step_3': 'المميزات',
        'step_4': 'معلومات تقنية',
        'step_5': 'المراجعة',
        'next': 'التالي',
        'previous': 'السابق',
        'save': 'حفظ الكاميرا',
        'edit': 'تعديل',
        'delete': 'حذف',
        'search': 'بحث',
        'filter': 'تصفية',
        'source_id': 'معرف المصدر',
        'brand': 'الماركة',
        'rtsp_area': 'منطقة RTSP',
        'feature_1': 'ميزة 1',
        'feature_2': 'ميزة 2',
        'feature_3': 'ميزة 3',
        'feature_4': 'ميزة 4',
        'feature_5': 'ميزة 5',
        'screenshot': 'لقطة شاشة',
        'ip_user_pass': 'IP/المستخدم/كلمة المرور',
        'working_hours': 'ساعات العمل',
        'non_working_hours': 'ساعات عدم العمل',
        'layout_missing': 'Layout المفقود',
        'serial_ws': 'رقم الورك ستيشن',
        'layout_file': 'ملف Layout',
        'total_cameras': 'إجمالي الكاميرات',
        'active': 'نشط',
        'inactive': 'غير نشط',
        'error': 'خطأ',
        'success': 'نجح',
        'warning': 'تحذير',
        'confirm': 'تأكيد',
        'yes': 'نعم',
        'no': 'لا',
        'export': 'تصدير Excel',
        'import': 'استيراد Excel',
        'backup': 'نسخ احتياطي',
        'restore': 'استعادة البيانات',
        'refresh': 'تحديث',
    }
}


class AICameraApp:
    """Professional AI Camera Management System with Advanced Features"""
    
    def __init__(self, root: tk.Tk, lang: str = 'en'):
        self.root = root
        self.lang = lang
        self.current_step = 1
        self.total_steps = 5
        
        self.root.title(self.t('app_title'))
        self._setup_window()
        
        # Data initialization
        self.cameras_data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []
        self.data_file = "cameras_database.json"
        self.backup_folder = "backups"
        self.load_data()
        
        # Form data
        self.form_data: Dict[str, Any] = {}
        self.entries: Dict[str, Any] = {}
        self.current_screenshot: Optional[str] = None
        self.editing_camera_id: Optional[str] = None
        self.current_page: str = 'dashboard'
        self.menu_buttons: Dict[str, tk.Button] = {}
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar()
        
        # Create backup folder
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)
        
        # Auto-save timer
        self.auto_save_enabled = True
        self.start_auto_save()
        
        self.setup_ui()
    
    def _setup_window(self) -> None:
        """Setup main window with responsive design"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg=COLORS['bg_dark'])
        self.root.minsize(1200, 700)
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def t(self, key: str) -> str:
        """Translation helper"""
        return TRANSLATIONS[self.lang].get(key, key)
    
    def load_data(self) -> None:
        """Load data with error handling and validation"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Validate data structure
                    if isinstance(data, list):
                        self.cameras_data = data
                        self.filtered_data = data.copy()
                    else:
                        raise ValueError("Invalid data format")
            else:
                self.cameras_data = []
                self.filtered_data = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.cameras_data = []
            self.filtered_data = []
            messagebox.showerror(
                self.t('error'),
                f"Failed to load database: {str(e)}\nStarting with empty database."
            )
    
    def save_data(self) -> bool:
        """Save data with backup"""
        try:
            # Create backup before saving
            if os.path.exists(self.data_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(
                    self.backup_folder, 
                    f"backup_{timestamp}.json"
                )
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    with open(backup_file, 'w', encoding='utf-8') as bf:
                        bf.write(f.read())
            
            # Save current data
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.cameras_data, f, ensure_ascii=False, indent=2)
            
            # Clean old backups (keep last 10)
            self._clean_old_backups()
            
            return True
        except Exception as e:
            messagebox.showerror(self.t('error'), f"Failed to save: {str(e)}")
            return False
    
    def _clean_old_backups(self) -> None:
        """Keep only last 10 backups"""
        try:
            backups = [f for f in os.listdir(self.backup_folder) 
                      if f.startswith("backup_") and f.endswith(".json")]
            backups.sort(reverse=True)
            
            for backup in backups[10:]:
                os.remove(os.path.join(self.backup_folder, backup))
        except Exception as e:
            print(f"Error cleaning backups: {e}")
    
    def start_auto_save(self) -> None:
        """Start auto-save timer (every 5 minutes)"""
        def auto_save_loop():
            while self.auto_save_enabled:
                time.sleep(300)  # 5 minutes
                if self.cameras_data:
                    try:
                        self.save_data()
                        print(f"Auto-save completed at {datetime.now()}")
                    except Exception as e:
                        print(f"Auto-save failed: {e}")
        
        thread = threading.Thread(target=auto_save_loop, daemon=True)
        thread.start()
    
    def setup_ui(self) -> None:
        """Setup main UI components"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        main_container.pack(fill='both', expand=True)
        
        # Create sidebar and content area
        self._create_sidebar(main_container)
        self._create_content_area(main_container)
        
        # Show dashboard by default
        self.switch_page('dashboard')
    
    def _create_sidebar(self, parent: tk.Frame) -> None:
        """Create enhanced sidebar with animations"""
        sidebar = tk.Frame(parent, bg=COLORS['bg_sidebar'], width=280)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Logo section
        self._create_logo(sidebar)
        
        # Separator
        tk.Frame(sidebar, bg=COLORS['border'], height=2).pack(
            fill='x', pady=20, padx=20
        )
        
        # Menu section
        self._create_menu(sidebar)
        
        # Spacer
        tk.Frame(sidebar, bg=COLORS['bg_sidebar']).pack(fill='both', expand=True)
        
        # Status section
        self._create_sidebar_status(sidebar)
        
        # Footer
        self._create_sidebar_footer(sidebar)
    
    def _create_logo(self, parent: tk.Frame) -> None:
        """Create animated logo section"""
        logo_frame = tk.Frame(parent, bg=COLORS['bg_sidebar'])
        logo_frame.pack(pady=30)
        
        # Animated icon
        icon_label = tk.Label(
            logo_frame,
            text="◉",
            font=("Arial", 52, "bold"),
            bg=COLORS['bg_sidebar'],
            fg=COLORS['accent_cyan']
        )
        icon_label.pack()
        
        # Title
        tk.Label(
            logo_frame,
            text=self.t('app_title'),
            font=("Segoe UI", 13, "bold"),
            bg=COLORS['bg_sidebar'],
            fg=COLORS['text_primary'],
            wraplength=240
        ).pack(pady=(15, 0))
        
        # Subtitle
        tk.Label(
            logo_frame,
            text="◉ Powered by AI Technology",
            font=("Segoe UI", 9),
            bg=COLORS['bg_sidebar'],
            fg=COLORS['accent_cyan']
        ).pack(pady=(5, 0))
        
        # Animate icon
        self._animate_icon(icon_label)
    
    def _animate_icon(self, label: tk.Label) -> None:
        """Subtle icon animation"""
        colors = [COLORS['accent_cyan'], COLORS['accent_purple'], 
                 COLORS['accent_green'], COLORS['accent_purple']]
        current_color = [0]
        
        def animate():
            if label.winfo_exists():
                label.config(fg=colors[current_color[0]])
                current_color[0] = (current_color[0] + 1) % len(colors)
                label.after(2000, animate)
        
        animate()
    
    def _create_menu(self, parent: tk.Frame) -> None:
        """Create menu with icons"""
        menu_items = [
            ('dashboard', '◉', self.t('dashboard'), 'Dashboard view'),
            ('cameras', '◉', self.t('cameras'), 'View all cameras'),
            ('add_camera', '◉', self.t('add_camera'), 'Add new camera'),
            ('statistics', '◉', self.t('statistics'), 'View analytics'),
        ]
        
        for page_id, icon, text, tooltip in menu_items:
            btn = self._create_menu_button(parent, page_id, icon, text)
            self.menu_buttons[page_id] = btn
            self._create_tooltip(btn, tooltip)
    
    def _create_menu_button(self, parent: tk.Frame, page_id: str, 
                           icon: str, text: str) -> tk.Button:
        """Create animated menu button"""
        btn = tk.Button(
            parent,
            text=f"{icon}  {text}",
            command=lambda: self.switch_page(page_id),
            bg=COLORS['bg_sidebar'],
            fg=COLORS['text_secondary'],
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            cursor='hand2',
            anchor='w',
            padx=25,
            pady=15,
            borderwidth=0,
            activebackground=COLORS['hover'],
            activeforeground=COLORS['accent_cyan']
        )
        btn.pack(fill='x', pady=3, padx=12)
        
        # Bind hover events
        btn.bind('<Enter>', lambda e: self._on_menu_enter(btn, page_id))
        btn.bind('<Leave>', lambda e: self._on_menu_leave(btn, page_id))
        
        return btn
    
    def _create_tooltip(self, widget: tk.Widget, text: str) -> None:
        """Create tooltip for widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                bg=COLORS['bg_card'],
                fg=COLORS['text_primary'],
                relief='solid',
                borderwidth=1,
                font=("Segoe UI", 9),
                padx=8,
                pady=4
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def _on_menu_enter(self, button: tk.Button, page_id: str) -> None:
        """Menu button hover effect"""
        if page_id != self.current_page:
            button.config(bg=COLORS['hover'], fg=COLORS['accent_cyan'])
    
    def _on_menu_leave(self, button: tk.Button, page_id: str) -> None:
        """Menu button leave effect"""
        if page_id != self.current_page:
            button.config(bg=COLORS['bg_sidebar'], fg=COLORS['text_secondary'])
    
    def _create_sidebar_status(self, parent: tk.Frame) -> None:
        """Create status indicators"""
        status_frame = tk.Frame(parent, bg=COLORS['bg_card'])
        status_frame.pack(fill='x', pady=15, padx=15)
        
        # Calculate statistics
        total = len(self.cameras_data)
        active = sum(1 for c in self.cameras_data 
                    if c.get('working_hours') == 'YES')
        errors = sum(1 for c in self.cameras_data 
                    if c.get('layout_missing') == 'Error')
        
        stats = [
            ('Total', total, COLORS['accent_cyan']),
            ('Active', active, COLORS['accent_green']),
            ('Errors', errors, COLORS['accent_red'])
        ]
        
        for label, value, color in stats:
            row = tk.Frame(status_frame, bg=COLORS['bg_card'])
            row.pack(fill='x', pady=5, padx=10)
            
            tk.Label(
                row,
                text=label,
                font=("Segoe UI", 10),
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary']
            ).pack(side='left')
            
            tk.Label(
                row,
                text=f"● {value}",
                font=("Segoe UI", 11, "bold"),
                bg=COLORS['bg_card'],
                fg=color
            ).pack(side='right')
    
    def _create_sidebar_footer(self, parent: tk.Frame) -> None:
        """Create sidebar footer"""
        footer = tk.Frame(parent, bg=COLORS['bg_sidebar'])
        footer.pack(fill='x', pady=15)
        
        tk.Label(
            footer,
            text=f"© 2024 AI Camera System",
            font=("Segoe UI", 8),
            bg=COLORS['bg_sidebar'],
            fg=COLORS['text_secondary']
        ).pack()
        
        tk.Label(
            footer,
            text=f"Version 2.0.0",
            font=("Segoe UI", 8),
            bg=COLORS['bg_sidebar'],
            fg=COLORS['accent_cyan']
        ).pack()
    
    def _create_content_area(self, parent: tk.Frame) -> None:
        """Create main content area"""
        self.content_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def switch_page(self, page: str) -> None:
        """Switch between pages with animation"""
        self.current_page = page
        
        # Update menu buttons
        for btn_id, btn in self.menu_buttons.items():
            if btn_id == page:
                btn.config(
                    bg=COLORS['accent_cyan'], 
                    fg=COLORS['bg_dark'],
                    font=("Segoe UI", 12, "bold")
                )
            else:
                btn.config(
                    bg=COLORS['bg_sidebar'], 
                    fg=COLORS['text_secondary'],
                    font=("Segoe UI", 12, "bold")
                )
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show selected page
        if page == 'dashboard':
            self.show_dashboard()
        elif page == 'cameras':
            self.show_cameras()
        elif page == 'add_camera':
            if not self.editing_camera_id:
                self._reset_form()
            self.show_wizard()
        elif page == 'statistics':
            self.show_statistics()
    
    def _reset_form(self) -> None:
        """Reset form data"""
        self.current_step = 1
        self.form_data = {}
        self.entries = {}
        self.current_screenshot = None
        self.editing_camera_id = None
    
    def _create_scrollable_frame(self) -> tuple:
        """Create scrollable frame with custom scrollbar"""
        canvas = tk.Canvas(
            self.content_frame, 
            bg=COLORS['bg_dark'], 
            highlightthickness=0
        )
        
        # Standard scrollbar
        scrollbar = ttk.Scrollbar(
            self.content_frame, 
            orient="vertical", 
            command=canvas.yview
        )
        
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_mousewheel_linux(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
        
        # Bind mouse wheel for different platforms
        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/Mac
        canvas.bind_all("<Button-4>", _on_mousewheel_linux)  # Linux scroll up
        canvas.bind_all("<Button-5>", _on_mousewheel_linux)  # Linux scroll down
        
        return canvas, scrollbar, scrollable_frame
    
    def show_dashboard(self) -> None:
        """Show enhanced dashboard"""
        canvas, scrollbar, scrollable_frame = self._create_scrollable_frame()
        
        # Header
        self._create_page_header(
            scrollable_frame, 
            'dashboard', 
            '◉ Real-time System Monitoring'
        )
        
        # Statistics cards
        self._create_dashboard_stats(scrollable_frame)
        
        # Charts section
        self._create_dashboard_charts(scrollable_frame)
        
        # Recent cameras
        self._create_recent_cameras_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_page_header(self, parent: tk.Frame, title_key: str, 
                           subtitle: str = '') -> None:
        """Create page header with gradient effect"""
        header = tk.Frame(parent, bg=COLORS['bg_dark'])
        header.pack(fill='x', padx=40, pady=30)
        
        # Title
        title_label = tk.Label(
            header,
            text=self.t(title_key),
            font=("Segoe UI", 32, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary']
        )
        title_label.pack(side='left')
        
        # Subtitle
        if subtitle:
            tk.Label(
                header,
                text=subtitle,
                font=("Segoe UI", 14),
                bg=COLORS['bg_dark'],
                fg=COLORS['accent_cyan']
            ).pack(side='left', padx=20)
        
        # Refresh button
        refresh_btn = tk.Button(
            header,
            text="⟳ " + self.t('refresh'),
            command=lambda: self.switch_page(self.current_page),
            bg=COLORS['accent_purple'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 11, "bold"),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        refresh_btn.pack(side='right')
    
    def _create_dashboard_stats(self, parent: tk.Frame) -> None:
        """Create animated statistics cards"""
        stats_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        stats_frame.pack(fill='x', padx=40, pady=20)
        
        # Calculate statistics
        total = len(self.cameras_data)
        active = sum(1 for c in self.cameras_data if c.get('working_hours') == 'YES')
        inactive = total - active
        errors = sum(1 for c in self.cameras_data if c.get('layout_missing') == 'Error')
        
        stats = [
            (self.t('total_cameras'), str(total), '◉', COLORS['accent_cyan'], 
             'Total registered cameras'),
            (self.t('active'), str(active), '●', COLORS['accent_green'], 
             'Currently active'),
            (self.t('inactive'), str(inactive), '○', COLORS['accent_orange'], 
             'Not working'),
            ('With Errors', str(errors), '⚠', COLORS['accent_red'], 
             'Need attention')
        ]
        
        for i, (title, value, icon, color, desc) in enumerate(stats):
            self._create_animated_stat_card(
                stats_frame, i, title, value, icon, color, desc
            )
    
    def _create_animated_stat_card(self, parent: tk.Frame, column: int, 
                                   title: str, value: str, icon: str, 
                                   color: str, description: str) -> None:
        """Create animated statistic card"""
        card = tk.Frame(
            parent, 
            bg=COLORS['bg_card'],
            highlightbackground=color,
            highlightthickness=2
        )
        card.grid(row=0, column=column, sticky='nsew', padx=8, pady=8)
        parent.grid_columnconfigure(column, weight=1, uniform="stats")
        
        # Icon
        icon_label = tk.Label(
            card, 
            text=icon, 
            font=("Arial", 40, "bold"),
            bg=COLORS['bg_card'], 
            fg=color
        )
        icon_label.pack(pady=(25, 10))
        
        # Value
        value_label = tk.Label(
            card, 
            text=value, 
            font=("Segoe UI", 36, "bold"),
            bg=COLORS['bg_card'], 
            fg=COLORS['text_primary']
        )
        value_label.pack()
        
        # Title
        tk.Label(
            card, 
            text=title, 
            font=("Segoe UI", 13, "bold"),
            bg=COLORS['bg_card'], 
            fg=COLORS['text_secondary']
        ).pack(pady=(5, 0))
        
        # Description
        tk.Label(
            card, 
            text=description, 
            font=("Segoe UI", 9),
            bg=COLORS['bg_card'], 
            fg=COLORS['text_secondary']
        ).pack(pady=(2, 25))
        
        # Hover effect
        def on_enter(e):
            card.config(highlightthickness=3)
        
        def on_leave(e):
            card.config(highlightthickness=2)
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
    
    def _create_dashboard_charts(self, parent: tk.Frame) -> None:
        """Create charts section"""
        charts_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        charts_frame.pack(fill='x', padx=40, pady=20)
        
        # Brand distribution
        brand_card = self._create_chart_card(
            charts_frame, 
            "◉ Cameras by Brand",
            0, 0
        )
        self._create_brand_chart(brand_card)
        
        # Status distribution
        status_card = self._create_chart_card(
            charts_frame,
            "◉ Status Distribution", 
            0, 1
        )
        self._create_status_chart(status_card)
    
    def _create_chart_card(self, parent: tk.Frame, title: str, 
                          row: int, col: int) -> tk.Frame:
        """Create chart container card"""
        card = tk.Frame(
            parent,
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=2
        )
        card.grid(row=row, column=col, sticky='nsew', padx=8, pady=8)
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 18, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_cyan']
        ).pack(anchor='w', padx=25, pady=20)
        
        return card
    
    def _create_brand_chart(self, parent: tk.Frame) -> None:
        """Create brand distribution chart"""
        brands = {}
        for camera in self.cameras_data:
            brand = camera.get('brand', 'Unknown')
            if brand:
                brands[brand] = brands.get(brand, 0) + 1
        
        chart_frame = tk.Frame(parent, bg=COLORS['bg_card'])
        chart_frame.pack(fill='both', expand=True, padx=25, pady=(0, 25))
        
        if brands:
            total = sum(brands.values())
            colors = [COLORS['accent_cyan'], COLORS['accent_purple'], 
                     COLORS['accent_green'], COLORS['accent_orange'],
                     COLORS['accent_yellow']]
            
            for i, (brand, count) in enumerate(sorted(brands.items(), 
                                                     key=lambda x: x[1], 
                                                     reverse=True)[:5]):
                self._create_bar_item(chart_frame, brand, count, total, 
                                     colors[i % len(colors)])
    
    def _create_bar_item(self, parent: tk.Frame, label: str, 
                        value: int, total: int, color: str) -> None:
        """Create horizontal bar chart item"""
        item_frame = tk.Frame(parent, bg=COLORS['bg_card'])
        item_frame.pack(fill='x', pady=5)
        
        # Label
        tk.Label(
            item_frame,
            text=f"{label}",
            font=("Segoe UI", 11),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            width=12,
            anchor='w'
        ).pack(side='left')
        
        # Progress bar container
        bar_container = tk.Frame(item_frame, bg=COLORS['bg_input'], height=25)
        bar_container.pack(side='left', fill='x', expand=True, padx=10)
        
        # Calculate percentage
        percentage = (value / total * 100) if total > 0 else 0
        
        # Progress bar
        bar = tk.Frame(
            bar_container, 
            bg=color, 
            width=int(percentage * 2),
            height=25
        )
        bar.place(x=0, y=0, relheight=1)
        
        # Value label
        tk.Label(
            item_frame,
            text=f"{value} ({percentage:.1f}%)",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS['bg_card'],
            fg=color,
            width=12
        ).pack(side='right')
    
    def _create_status_chart(self, parent: tk.Frame) -> None:
        """Create status distribution chart"""
        active = sum(1 for c in self.cameras_data if c.get('working_hours') == 'YES')
        inactive = sum(1 for c in self.cameras_data if c.get('working_hours') == 'NO')
        unknown = len(self.cameras_data) - active - inactive
        
        chart_frame = tk.Frame(parent, bg=COLORS['bg_card'])
        chart_frame.pack(fill='both', expand=True, padx=25, pady=(0, 25))
        
        total = len(self.cameras_data)
        
        if total > 0:
            self._create_bar_item(chart_frame, 'Active', active, total, 
                                 COLORS['accent_green'])
            self._create_bar_item(chart_frame, 'Inactive', inactive, total, 
                                 COLORS['accent_orange'])
            self._create_bar_item(chart_frame, 'Unknown', unknown, total, 
                                 COLORS['text_secondary'])
    
    def _create_recent_cameras_section(self, parent: tk.Frame) -> None:
        """Create recent cameras table"""
        recent_frame = tk.Frame(
            parent,
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=2
        )
        recent_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Header
        header = tk.Frame(recent_frame, bg=COLORS['bg_card'])
        header.pack(fill='x', padx=30, pady=20)
        
        tk.Label(
            header,
            text="◉ Recent Cameras",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(side='left')
        
        tk.Button(
            header,
            text="View All →",
            command=lambda: self.switch_page('cameras'),
            bg=COLORS['accent_cyan'],
            fg=COLORS['bg_dark'],
            font=("Segoe UI", 11, "bold"),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side='right')
        
        # Table
        table_frame = tk.Frame(recent_frame, bg=COLORS['bg_card'])
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        tree = self._create_treeview(
            table_frame,
            "Dashboard",
            ("source_id", "brand", "rtsp_area", "working_hours", "layout_missing"),
            {
                "source_id": "Source ID",
                "brand": "Brand",
                "rtsp_area": "RTSP Area",
                "working_hours": "Status",
                "layout_missing": "Layout"
            },
            height=8
        )
        
        # Add recent data
        for camera in self.cameras_data[-10:][::-1]:
            tree.insert('', 'end', values=(
                camera.get('source_id', ''),
                camera.get('brand', ''),
                camera.get('rtsp_area', ''),
                camera.get('working_hours', ''),
                camera.get('layout_missing', '')
            ))
        
        tree.bind('<Double-Button-1>', lambda e: self.edit_from_table(tree))
    
    def _create_treeview(self, parent: tk.Frame, style_prefix: str,
                        columns: tuple, headers: dict, height: int = 10) -> ttk.Treeview:
        """Create styled treeview"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure treeview style
        style.configure(
            f"{style_prefix}.Treeview",
            background=COLORS['bg_input'],
            foreground=COLORS['text_primary'],
            fieldbackground=COLORS['bg_input'],
            font=("Segoe UI", 11),
            rowheight=40,
            borderwidth=0
        )
        
        style.configure(
            f"{style_prefix}.Treeview.Heading",
            background=COLORS['bg_sidebar'],
            foreground=COLORS['accent_cyan'],
            font=("Segoe UI", 12, "bold"),
            borderwidth=0,
            relief='flat'
        )
        
        style.map(
            f'{style_prefix}.Treeview',
            background=[('selected', COLORS['accent_cyan'])],
            foreground=[('selected', COLORS['bg_dark'])]
        )
        
        # Create treeview
        tree = ttk.Treeview(
            parent,
            columns=columns,
            show='headings',
            height=height,
            style=f"{style_prefix}.Treeview"
        )
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=150, anchor='center', minwidth=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        return tree
    
    def show_cameras(self) -> None:
        """Show cameras page with search and filter"""
        canvas, scrollbar, scrollable_frame = self._create_scrollable_frame()
        
        # Header with search
        self._create_cameras_header(scrollable_frame)
        
        # Search and filter bar
        self._create_search_filter_bar(scrollable_frame)
        
        # Cameras table
        self._create_cameras_table(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_cameras_header(self, parent: tk.Frame) -> None:
        """Create cameras page header"""
        header = tk.Frame(parent, bg=COLORS['bg_dark'])
        header.pack(fill='x', padx=40, pady=30)
        
        # Title
        tk.Label(
            header,
            text="◉ " + self.t('cameras'),
            font=("Segoe UI", 32, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary']
        ).pack(side='left')
        
        # Action buttons
        btn_frame = tk.Frame(header, bg=COLORS['bg_dark'])
        btn_frame.pack(side='right')
        
        buttons = [
            ('Export', self.export_to_excel, COLORS['accent_green'], '⬇'),
            ('Import', self.import_from_excel, COLORS['accent_orange'], '⬆'),
            ('Edit', self.edit_selected_camera, COLORS['accent_purple'], '✎'),
            ('Delete', self.delete_selected_camera, COLORS['accent_red'], '✕')
        ]
        
        for text, command, color, icon in buttons:
            self._create_action_button(btn_frame, f"{icon} {text}", command, color)
    
    def _create_action_button(self, parent: tk.Frame, text: str,
                             command, color: str) -> None:
        """Create styled action button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=COLORS['text_primary'],
            font=("Segoe UI", 11, "bold"),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            borderwidth=0,
            activebackground=color,
            activeforeground=COLORS['text_primary']
        )
        btn.pack(side='left', padx=5)
        
        # Hover effect
        def on_enter(e):
            btn.config(bg=self._lighten_color(color))
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
    
    def _lighten_color(self, color: str) -> str:
        """Lighten hex color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def _create_search_filter_bar(self, parent: tk.Frame) -> None:
        """Create search and filter bar"""
        search_frame = tk.Frame(
            parent,
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=2
        )
        search_frame.pack(fill='x', padx=40, pady=(0, 20))
        
        inner_frame = tk.Frame(search_frame, bg=COLORS['bg_card'])
        inner_frame.pack(fill='x', padx=25, pady=20)
        
        # Search box
        search_container = tk.Frame(inner_frame, bg=COLORS['bg_card'])
        search_container.pack(side='left', fill='x', expand=True)
        
        tk.Label(
            search_container,
            text="🔍",
            font=("Arial", 16),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_cyan']
        ).pack(side='left', padx=(0, 10))
        
        search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=("Segoe UI", 12),
            bg=COLORS['bg_input'],
            fg=COLORS['text_primary'],
            relief='flat',
            insertbackground=COLORS['accent_cyan']
        )
        search_entry.pack(side='left', fill='x', expand=True, ipady=10, ipadx=15)
        search_entry.insert(0, "Search by Source ID, Brand, or Area...")
        
        # Bind search events
        def on_focus_in(e):
            if search_entry.get() == "Search by Source ID, Brand, or Area...":
                search_entry.delete(0, 'end')
                search_entry.config(fg=COLORS['text_primary'])
        
        def on_focus_out(e):
            if not search_entry.get():
                search_entry.insert(0, "Search by Source ID, Brand, or Area...")
                search_entry.config(fg=COLORS['text_secondary'])
        
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        search_entry.bind('<KeyRelease>', lambda e: self._apply_search_filter())
        
        # Filter dropdown
        filter_container = tk.Frame(inner_frame, bg=COLORS['bg_card'])
        filter_container.pack(side='right', padx=(20, 0))
        
        tk.Label(
            filter_container,
            text="Filter:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(side='left', padx=(0, 10))
        
        filter_combo = ttk.Combobox(
            filter_container,
            textvariable=self.filter_var,
            values=['All', 'Active', 'Inactive', 'With Errors', 'Teller', 'Safe', 'CS'],
            state='readonly',
            font=("Segoe UI", 11),
            width=15
        )
        filter_combo.set('All')
        filter_combo.pack(side='left')
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self._apply_search_filter())
        
        # Clear button
        tk.Button(
            inner_frame,
            text="✕ Clear",
            command=self._clear_search_filter,
            bg=COLORS['bg_sidebar'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 10, "bold"),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=10
        ).pack(side='right', padx=(10, 0))
    
    def _apply_search_filter(self) -> None:
        """Apply search and filter"""
        search_text = self.search_var.get().lower()
        filter_value = self.filter_var.get()
        
        # Reset if search is placeholder
        if search_text == "search by source id, brand, or area...":
            search_text = ""
        
        # Filter data
        self.filtered_data = self.cameras_data.copy()
        
        # Apply search
        if search_text:
            self.filtered_data = [
                c for c in self.filtered_data
                if search_text in str(c.get('source_id', '')).lower() or
                   search_text in str(c.get('brand', '')).lower() or
                   search_text in str(c.get('rtsp_area', '')).lower()
            ]
        
        # Apply filter
        if filter_value == 'Active':
            self.filtered_data = [c for c in self.filtered_data 
                                 if c.get('working_hours') == 'YES']
        elif filter_value == 'Inactive':
            self.filtered_data = [c for c in self.filtered_data 
                                 if c.get('working_hours') == 'NO']
        elif filter_value == 'With Errors':
            self.filtered_data = [c for c in self.filtered_data 
                                 if c.get('layout_missing') == 'Error']
        elif filter_value in ['Teller', 'Safe', 'CS']:
            self.filtered_data = [c for c in self.filtered_data 
                                 if c.get('brand') == filter_value]
        
        # Refresh table
        self.show_cameras()
    
    def _clear_search_filter(self) -> None:
        """Clear search and filter"""
        self.search_var.set('')
        self.filter_var.set('All')
        self.filtered_data = self.cameras_data.copy()
        self.show_cameras()
    
    def _create_cameras_table(self, parent: tk.Frame) -> None:
        """Create cameras table with pagination"""
        table_container = tk.Frame(
            parent,
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=2
        )
        table_container.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Table header
        table_header = tk.Frame(table_container, bg=COLORS['bg_card'])
        table_header.pack(fill='x', padx=30, pady=20)
        
        tk.Label(
            table_header,
            text=f"◉ Showing {len(self.filtered_data)} cameras",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(side='left')
        
        # Table frame
        table_frame = tk.Frame(table_container, bg=COLORS['bg_card'])
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Create treeview
        self.camera_tree = self._create_treeview(
            table_frame,
            "Cameras",
            ("source_id", "brand", "rtsp_area", "features", "working_hours", 
             "non_working_hours", "layout_missing"),
            {
                "source_id": "Source ID",
                "brand": "Brand",
                "rtsp_area": "RTSP Area",
                "features": "Features",
                "working_hours": "Working",
                "non_working_hours": "Non-Working",
                "layout_missing": "Layout"
            },
            height=15
        )
        
        # Populate table
        for camera in self.filtered_data:
            features = []
            for i in range(1, 6):
                feat = camera.get(f'feature_{i}', '')
                if feat:
                    features.append(feat)
            features_str = ', '.join(features[:2]) if features else '-'
            
            self.camera_tree.insert('', 'end', values=(
                camera.get('source_id', ''),
                camera.get('brand', ''),
                camera.get('rtsp_area', ''),
                features_str,
                camera.get('working_hours', ''),
                camera.get('non_working_hours', ''),
                camera.get('layout_missing', '')
            ))
        
        # Bind double-click
        self.camera_tree.bind('<Double-Button-1>', 
                             lambda e: self.edit_from_table(self.camera_tree))
    
    def show_statistics(self) -> None:
        """Show advanced statistics"""
        canvas, scrollbar, scrollable_frame = self._create_scrollable_frame()
        
        self._create_page_header(scrollable_frame, 'statistics', 
                               '◉ Comprehensive Analytics')
        
        # Statistics grid
        stats_grid = tk.Frame(scrollable_frame, bg=COLORS['bg_dark'])
        stats_grid.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Brand statistics
        self._create_brand_statistics(stats_grid, 0, 0)
        
        # Area statistics
        self._create_area_statistics(stats_grid, 0, 1)
        
        # Feature statistics
        self._create_feature_statistics(stats_grid, 1, 0, colspan=2)
        
        canvas.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_brand_statistics(self, parent: tk.Frame, row: int, col: int) -> None:
        """Create brand statistics card"""
        card = tk.Frame(
            parent,
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=2
        )
        card.grid(row=row, column=col, sticky='nsew', padx=10, pady=10)
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
        tk.Label(
            card,
            text="◉ Cameras by Brand",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_cyan']
        ).pack(anchor='w', padx=30, pady=20)
        
        brands = {}
        for camera in self.cameras_data:
            brand = camera.get('brand', 'Unknown')
            if brand:
                brands[brand] = brands.get(brand, 0) + 1
        
        content_frame = tk.Frame(card, bg=COLORS['bg_card'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        colors = [COLORS['accent_green'], COLORS['accent_cyan'], 
                 COLORS['accent_purple'], COLORS['accent_orange']]
        
        for i, (brand, count) in enumerate(sorted(brands.items(), 
                                                  key=lambda x: x[1], 
                                                  reverse=True)):
            self._create_stat_row(content_frame, brand, count, 
                                colors[i % len(colors)])
    
    def _create_area_statistics(self, parent: tk.Frame, row: int, col: int) -> None:
        """Create area statistics card"""
        card = tk.Frame(
            parent,
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=2
        )
        card.grid(row=row, column=col, sticky='nsew', padx=10, pady=10)
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        
        tk.Label(
            card,
            text="◉ Cameras by Area",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_cyan']
        ).pack(anchor='w', padx=30, pady=20)
        
        areas = {}
        for camera in self.cameras_data:
            area = camera.get('rtsp_area', 'Unknown')
            if area:
                areas[area] = areas.get(area, 0) + 1
        
        content_frame = tk.Frame(card, bg=COLORS['bg_card'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        colors = [COLORS['accent_cyan'], COLORS['accent_green'], 
                 COLORS['accent_purple'], COLORS['accent_orange']]
        
        for i, (area, count) in enumerate(sorted(areas.items(), 
                                                key=lambda x: x[1], 
                                                reverse=True)[:10]):
            self._create_stat_row(content_frame, area, count, 
                                colors[i % len(colors)])
    
    def _create_feature_statistics(self, parent: tk.Frame, row: int, 
                                   col: int, colspan: int = 1) -> None:
        """Create feature statistics card"""
        card = tk.Frame(
            parent,
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=2
        )
        card.grid(row=row, column=col, columnspan=colspan, 
                 sticky='nsew', padx=10, pady=10)
        parent.grid_rowconfigure(row, weight=1)
        
        tk.Label(
            card,
            text="◉ Feature Distribution",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_cyan']
        ).pack(anchor='w', padx=30, pady=20)
        
        features = {}
        for camera in self.cameras_data:
            for i in range(1, 6):
                feat = camera.get(f'feature_{i}', '')
                if feat:
                    features[feat] = features.get(feat, 0) + 1
        
        content_frame = tk.Frame(card, bg=COLORS['bg_card'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        colors = [COLORS['accent_green'], COLORS['accent_cyan'], 
                 COLORS['accent_purple'], COLORS['accent_orange'],
                 COLORS['accent_yellow']]
        
        for i, (feat, count) in enumerate(sorted(features.items(), 
                                                key=lambda x: x[1], 
                                                reverse=True)):
            self._create_stat_row(content_frame, feat, count, 
                                colors[i % len(colors)])
    
    def _create_stat_row(self, parent: tk.Frame, label: str, 
                        value: int, color: str) -> None:
        """Create statistics row"""
        row = tk.Frame(parent, bg=COLORS['bg_input'])
        row.pack(fill='x', pady=4)
        
        tk.Label(
            row,
            text=label,
            font=("Segoe UI", 12),
            bg=COLORS['bg_input'],
            fg=COLORS['text_primary'],
            anchor='w'
        ).pack(side='left', padx=20, pady=12, fill='x', expand=True)
        
        tk.Label(
            row,
            text=f"● {value}",
            font=("Segoe UI", 13, "bold"),
            bg=COLORS['bg_input'],
            fg=color
        ).pack(side='right', padx=20, pady=12)
    
    def show_wizard(self) -> None:
        """Show multi-step wizard"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        canvas, scrollbar, scrollable_frame = self._create_scrollable_frame()
        
        self._create_wizard_header(scrollable_frame)
        
        wizard_content = tk.Frame(scrollable_frame, bg=COLORS['bg_dark'])
        wizard_content.pack(fill='both', expand=True, padx=50, pady=30)
        
        self.show_camera_form(wizard_content)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_wizard_header(self, parent: tk.Frame) -> None:
        """Create wizard header with progress"""
        header = tk.Frame(parent, bg=COLORS['bg_dark'])
        header.pack(fill='x', padx=40, pady=30)
        
        title = ("◉ Edit Camera" if self.editing_camera_id 
                else "◉ " + self.t('add_camera'))
        
        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 28, "bold"),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_primary']
        ).pack(anchor='w', pady=(0, 25))
        
        # Progress indicator
        self._create_steps_indicator(header)
    
    def _create_steps_indicator(self, parent: tk.Frame) -> None:
        """Create animated progress steps"""
        steps_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        steps_frame.pack(fill='x')
        
        step_names = [
            ('1', 'Basic Info'),
            ('2', 'Area Details'),
            ('3', 'Features'),
            ('4', 'Technical'),
            ('5', 'Review')
        ]
        
        for i, (num, name) in enumerate(step_names, 1):
            step_container = tk.Frame(steps_frame, bg=COLORS['bg_dark'])
            step_container.pack(side='left', padx=8)
            
            # Determine colors
            if i < self.current_step:
                bg_color = COLORS['accent_green']
                icon_text = "✓"
                name_color = COLORS['accent_green']
            elif i == self.current_step:
                bg_color = COLORS['accent_cyan']
                icon_text = num
                name_color = COLORS['accent_cyan']
            else:
                bg_color = COLORS['bg_card']
                icon_text = num
                name_color = COLORS['text_secondary']
            
            # Step circle
            step_icon = tk.Label(
                step_container,
                text=icon_text,
                font=("Segoe UI", 14, "bold"),
                bg=bg_color,
                fg=COLORS['text_primary'],
                width=3,
                height=1
            )
            step_icon.pack(pady=6)
            
            # Step name
            tk.Label(
                step_container,
                text=name,
                font=("Segoe UI", 10, "bold" if i == self.current_step else "normal"),
                bg=COLORS['bg_dark'],
                fg=name_color
            ).pack()
            
            # Connection line
            if i < len(step_names):
                line = tk.Frame(
                    steps_frame,
                    bg=COLORS['accent_green'] if i < self.current_step else COLORS['bg_card'],
                    height=3,
                    width=40
                )
                line.pack(side='left', pady=(20, 0))
    
    def show_camera_form(self, parent: tk.Frame) -> None:
        """Display current step form"""
        # Clear previous form
        for widget in parent.winfo_children():
            widget.destroy()
        
        form_card = tk.Frame(
            parent,
            bg=COLORS['bg_card'],
            highlightbackground=COLORS['border'],
            highlightthickness=2
        )
        form_card.pack(fill='both', expand=True)
        
        step_titles = {
            1: '◉ ' + self.t('step_1'),
            2: '◉ ' + self.t('step_2'),
            3: '◉ ' + self.t('step_3'),
            4: '◉ ' + self.t('step_4'),
            5: '◉ ' + self.t('step_5')
        }
        
        tk.Label(
            form_card,
            text=step_titles.get(self.current_step, 'Step'),
            font=("Segoe UI", 24, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_cyan']
        ).pack(anchor='w', padx=35, pady=(35, 25))
        
        fields_frame = tk.Frame(form_card, bg=COLORS['bg_card'])
        fields_frame.pack(fill='both', expand=True, padx=35, pady=(0, 25))
        
        # Clear previous entries for this step
        self.entries = {}
        
        step_methods = {
            1: self.show_step1_fields,
            2: self.show_step2_fields,
            3: self.show_step3_fields,
            4: self.show_step4_fields,
            5: self.show_step5_review
        }
        
        step_method = step_methods.get(self.current_step)
        if step_method:
            step_method(fields_frame)
        
        self._create_navigation_buttons(form_card)
    
    def _create_navigation_buttons(self, parent: tk.Frame) -> None:
        """Create wizard navigation buttons"""
        nav_frame = tk.Frame(parent, bg=COLORS['bg_card'])
        nav_frame.pack(fill='x', padx=35, pady=(25, 35))
        
        if self.current_step > 1:
            prev_btn = tk.Button(
                nav_frame,
                text="◀ " + self.t('previous'),
                command=self.prev_step,
                bg=COLORS['bg_sidebar'],
                fg=COLORS['text_primary'],
                font=("Segoe UI", 12, "bold"),
                relief='flat',
                cursor='hand2',
                padx=30,
                pady=15,
                borderwidth=0
            )
            prev_btn.pack(side='left', padx=8)
        
        if self.current_step < self.total_steps:
            next_btn = tk.Button(
                nav_frame,
                text=self.t('next') + " ▶",
                command=self.next_step,
                bg=COLORS['accent_cyan'],
                fg=COLORS['bg_dark'],
                font=("Segoe UI", 12, "bold"),
                relief='flat',
                cursor='hand2',
                padx=30,
                pady=15,
                borderwidth=0
            )
            next_btn.pack(side='right', padx=8)
        else:
            save_btn = tk.Button(
                nav_frame,
                text="✓ " + self.t('save'),
                command=self.save_camera,
                bg=COLORS['accent_green'],
                fg=COLORS['text_primary'],
                font=("Segoe UI", 12, "bold"),
                relief='flat',
                cursor='hand2',
                padx=35,
                pady=15,
                borderwidth=0
            )
            save_btn.pack(side='right', padx=8)
    
    def create_form_field(self, parent: tk.Frame, label: str, key: str,
                         row: int, col: int = 0, colspan: int = 1,
                         field_type: str = 'entry', 
                         options: Optional[List[str]] = None) -> None:
        """Create form field with validation"""
        field_container = tk.Frame(parent, bg=COLORS['bg_card'])
        field_container.grid(row=row, column=col, columnspan=colspan, 
                           sticky='ew', padx=12, pady=12)
        
        label_frame = tk.Frame(field_container, bg=COLORS['bg_card'])
        label_frame.pack(anchor='w', pady=(0, 8))
        
        tk.Label(
            label_frame,
            text=label,
            font=("Segoe UI", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(side='left')
        
        # Required indicator
        if key in ['source_id', 'brand']:
            tk.Label(
                label_frame,
                text=" *",
                font=("Segoe UI", 12, "bold"),
                bg=COLORS['bg_card'],
                fg=COLORS['accent_red']
            ).pack(side='left')
        
        if field_type == 'entry':
            self._create_entry_field(field_container, key)
        elif field_type == 'combobox':
            self._create_combobox_field(field_container, key, options or [])
        elif field_type == 'text':
            self._create_text_field(field_container, key)
    
    def _create_entry_field(self, parent: tk.Frame, key: str) -> None:
        """Create entry field with styling"""
        entry_frame = tk.Frame(parent, bg=COLORS['bg_input'])
        entry_frame.pack(fill='x')
        
        entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 12),
            bg=COLORS['bg_input'],
            fg=COLORS['text_primary'],
            relief='flat',
            insertbackground=COLORS['accent_cyan'],
            borderwidth=0
        )
        entry.pack(fill='x', ipady=10, ipadx=15)
        self.entries[key] = entry
        
        if self.editing_camera_id and key in self.form_data:
            entry.insert(0, str(self.form_data.get(key, '')))
    
    def _create_combobox_field(self, parent: tk.Frame, key: str,
                              options: List[str]) -> None:
        """Create combobox field"""
        combo = ttk.Combobox(
            parent,
            values=options,
            font=("Segoe UI", 12),
            state='readonly'
        )
        combo.pack(fill='x', ipady=10)
        self.entries[key] = combo
        
        if self.editing_camera_id and key in self.form_data:
            value = str(self.form_data.get(key, ''))
            if value in options:
                combo.set(value)
            elif options:
                combo.set(options[0])
    
    def _create_text_field(self, parent: tk.Frame, key: str) -> None:
        """Create multiline text field"""
        text_frame = tk.Frame(parent, bg=COLORS['bg_input'])
        text_frame.pack(fill='both', expand=True)
        
        text = tk.Text(
            text_frame,
            font=("Segoe UI", 12),
            bg=COLORS['bg_input'],
            fg=COLORS['text_primary'],
            relief='flat',
            height=4,
            insertbackground=COLORS['accent_cyan'],
            borderwidth=0,
            wrap='word'
        )
        text.pack(fill='both', expand=True, ipady=10, ipadx=15)
        self.entries[key] = text
        
        if self.editing_camera_id and key in self.form_data:
            text.insert('1.0', str(self.form_data.get(key, '')))
    
    def show_step1_fields(self, parent: tk.Frame) -> None:
        """Step 1: Basic Information"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        self.create_form_field(parent, self.t('source_id'), 
                             'source_id', 0, 0)
        
        self.create_form_field(parent, self.t('brand'), 'brand', 0, 1,
                             field_type='combobox',
                             options=['', 'Teller', 'Safe', 'CS', 'UB', 'Other'])
        
        self.create_form_field(parent, self.t('ip_user_pass'), 
                             'ip_user_pass', 1, 0, colspan=2, 
                             field_type='text')
    
    def show_step2_fields(self, parent: tk.Frame) -> None:
        """Step 2: Area Details"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        self.create_form_field(parent, self.t('rtsp_area'), 
                             'rtsp_area', 0, 0, colspan=2)
        
        hours_options = ['', 'YES', 'NO']
        self.create_form_field(parent, self.t('working_hours'), 
                             'working_hours', 1, 0,
                             field_type='combobox', options=hours_options)
        
        self.create_form_field(parent, self.t('non_working_hours'), 
                             'non_working_hours', 1, 1,
                             field_type='combobox', options=hours_options)
    
    def show_step3_fields(self, parent: tk.Frame) -> None:
        """Step 3: Features"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        feature_options = [
            '', 'SMT', 'EMP', 'Left Obj', 'UB', 'Teller SMT',
            'Teller Left Obj', 'Waiting Area', 'Waiting Area Left Obj'
        ]
        
        for i in range(1, 6):
            row = (i - 1) // 2
            col = (i - 1) % 2
            
            self.create_form_field(
                parent, 
                f"{self.t('feature_1').replace('1', str(i))}", 
                f'feature_{i}', 
                row, col,
                field_type='combobox',
                options=feature_options
            )
    
    def show_step4_fields(self, parent: tk.Frame) -> None:
        """Step 4: Technical Details"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Screenshot uploader
        self._create_screenshot_uploader(parent)
        
        # Layout missing
        layout_options = ['', 'Error', 'YES', 'NO']
        self.create_form_field(parent, self.t('layout_missing'), 
                             'layout_missing', 1, 0,
                             field_type='combobox', options=layout_options)
        
        # Serial WS
        self.create_form_field(parent, self.t('serial_ws'), 
                             'serial_ws', 1, 1)
        
        # Layout File
        layout_file_options = ['', 'YES', 'NO']
        self.create_form_field(parent, self.t('layout_file'), 
                             'layout_file', 2, 0,
                             field_type='combobox', options=layout_file_options)
    
    def _create_screenshot_uploader(self, parent: tk.Frame) -> None:
        """Create screenshot upload section"""
        screenshot_frame = tk.Frame(parent, bg=COLORS['bg_card'])
        screenshot_frame.grid(row=0, column=0, columnspan=2, 
                            sticky='ew', padx=12, pady=20)
        
        tk.Label(
            screenshot_frame,
            text="📷 " + self.t('screenshot'),
            font=("Segoe UI", 13, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(anchor='w', pady=(0, 12))
        
        button_frame = tk.Frame(screenshot_frame, bg=COLORS['bg_card'])
        button_frame.pack(fill='x', pady=(0, 12))
        
        tk.Button(
            button_frame,
            text="⬆ Upload Image",
            command=self.upload_screenshot,
            bg=COLORS['accent_purple'],
            fg=COLORS['text_primary'],
            font=("Segoe UI", 11, "bold"),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12
        ).pack(side='left')
        
        if self.current_screenshot:
            tk.Button(
                button_frame,
                text="✕ Remove",
                command=self.remove_screenshot,
                bg=COLORS['accent_red'],
                fg=COLORS['text_primary'],
                font=("Segoe UI", 11, "bold"),
                relief='flat',
                cursor='hand2',
                padx=15,
                pady=12
            ).pack(side='left', padx=(10, 0))
        
        # Create preview label
        preview_text = "No image uploaded"
        if self.current_screenshot:
            preview_text = ""
        elif self.editing_camera_id and self.form_data.get('screenshot'):
            preview_text = ""
            self.current_screenshot = self.form_data.get('screenshot')
        
        self.screenshot_preview = tk.Label(
            screenshot_frame,
            bg=COLORS['bg_input'],
            text=preview_text,
            fg=COLORS['text_secondary'],
            font=("Segoe UI", 11),
            height=10
        )
        self.screenshot_preview.pack(fill='x')
        
        # Display existing screenshot if available
        if self.current_screenshot:
            self.display_screenshot(self.current_screenshot)
    
    def show_step5_review(self, parent: tk.Frame) -> None:
        """Step 5: Review all data"""
        review_container = tk.Frame(parent, bg=COLORS['bg_input'])
        review_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            review_container,
            text="◉ Review Your Data",
            font=("Segoe UI", 18, "bold"),
            bg=COLORS['bg_input'],
            fg=COLORS['accent_cyan']
        ).pack(anchor='w', padx=30, pady=30)
        
        self.collect_form_data()
        
        review_text = tk.Text(
            review_container,
            font=("Segoe UI", 12),
            bg=COLORS['bg_input'],
            fg=COLORS['text_primary'],
            relief='flat',
            height=20,
            wrap='word',
            padx=20,
            pady=20
        )
        review_text.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Display all form data
        field_labels = {
            'source_id': 'Source ID',
            'brand': 'Brand',
            'rtsp_area': 'RTSP Area',
            'ip_user_pass': 'IP/User/Pass',
            'working_hours': 'Working Hours',
            'non_working_hours': 'Non-Working Hours',
            'feature_1': 'Feature 1',
            'feature_2': 'Feature 2',
            'feature_3': 'Feature 3',
            'feature_4': 'Feature 4',
            'feature_5': 'Feature 5',
            'layout_missing': 'Layout Missing',
            'serial_ws': 'Serial WS',
            'layout_file': 'Layout File',
            'screenshot': 'Screenshot'
        }
        
        for key, label in field_labels.items():
            value = self.form_data.get(key, '')
            if key == 'screenshot' and value:
                review_text.insert('end', f"📷 {label}: [Image Attached]\n\n")
            elif value:
                review_text.insert('end', f"● {label}: {value}\n\n")
        
        review_text.config(state='disabled')
    
    def upload_screenshot(self) -> None:
        """Upload and process screenshot"""
        file_path = filedialog.askopenfilename(
            title="Select Screenshot",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            try:
                img = Image.open(file_path)
                img.thumbnail((500, 300), Image.Resampling.LANCZOS)
                
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                self.current_screenshot = img_str
                self.display_screenshot(img_str)
                
                messagebox.showinfo(self.t('success'), 
                                  "✓ Image uploaded successfully!")
            except Exception as e:
                messagebox.showerror(self.t('error'), 
                                   f"Failed to load image: {str(e)}")
    
    def remove_screenshot(self) -> None:
        """Remove uploaded screenshot"""
        self.current_screenshot = None
        self.form_data['screenshot'] = None
        
        # Recreate the wizard to update UI
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.show_wizard()
    
    def display_screenshot(self, img_base64: str) -> None:
        """Display screenshot preview"""
        try:
            img_data = base64.b64decode(img_base64)
            img = Image.open(io.BytesIO(img_data))
            img.thumbnail((500, 300), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            self.screenshot_preview.config(image=photo, text="")
            self.screenshot_preview.image = photo
        except Exception as e:
            print(f"Error displaying screenshot: {e}")
            self.screenshot_preview.config(
                text="Error loading image",
                fg=COLORS['accent_red']
            )
    
    def collect_form_data(self) -> None:
        """Collect all form data"""
        for key, widget in self.entries.items():
            try:
                if isinstance(widget, tk.Entry):
                    self.form_data[key] = widget.get().strip()
                elif isinstance(widget, ttk.Combobox):
                    self.form_data[key] = widget.get().strip()
                elif isinstance(widget, tk.Text):
                    self.form_data[key] = widget.get('1.0', 'end-1c').strip()
            except:
                pass
        
        if self.current_screenshot:
            self.form_data['screenshot'] = self.current_screenshot
    
    def next_step(self) -> None:
        """Move to next step"""
        self.collect_form_data()
        
        # Validate current step
        if self.current_step == 1:
            if not self.form_data.get('source_id'):
                messagebox.showerror(
                    self.t('error'),
                    f"❌ {self.t('source_id')} is required!"
                )
                return
        
        if self.current_step < self.total_steps:
            self.current_step += 1
            # Recreate the wizard to show next step
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            self.show_wizard()
    
    def prev_step(self) -> None:
        """Move to previous step"""
        self.collect_form_data()
        
        if self.current_step > 1:
            self.current_step -= 1
            # Recreate the wizard to show previous step
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            self.show_wizard()
    
    def save_camera(self) -> None:
        """Save camera data"""
        self.collect_form_data()
        
        # Validate required fields
        if not self.form_data.get('source_id'):
            messagebox.showerror(
                self.t('error'),
                f"❌ {self.t('source_id')} is required!"
            )
            return
        
        # Add timestamps
        self.form_data['created_at'] = datetime.now().isoformat()
        self.form_data['updated_at'] = datetime.now().isoformat()
        
        if self.editing_camera_id:
            self._update_camera()
        else:
            self._add_new_camera()
        
        if self.save_data():
            messagebox.showinfo(
                self.t('success'),
                "✓ Camera saved successfully!"
            )
            self.filtered_data = self.cameras_data.copy()
            self.switch_page('cameras')
    
    def _update_camera(self) -> None:
        """Update existing camera"""
        for i, camera in enumerate(self.cameras_data):
            if camera.get('id') == self.editing_camera_id:
                self.form_data['id'] = self.editing_camera_id
                self.form_data['created_at'] = camera.get('created_at')
                self.cameras_data[i] = self.form_data
                break
    
    def _add_new_camera(self) -> None:
        """Add new camera"""
        max_id = 0
        for camera in self.cameras_data:
            try:
                cam_id = int(camera.get('id', 0))
                max_id = max(max_id, cam_id)
            except (ValueError, TypeError):
                pass
        
        self.form_data['id'] = str(max_id + 1)
        self.cameras_data.append(self.form_data)
    
    def edit_selected_camera(self) -> None:
        """Edit selected camera from table"""
        if not hasattr(self, 'camera_tree'):
            messagebox.showwarning(
                self.t('warning'),
                "⚠ No camera table available"
            )
            return
        
        selection = self.camera_tree.selection()
        if not selection:
            messagebox.showwarning(
                self.t('warning'),
                "⚠ Please select a camera to edit"
            )
            return
        
        item = self.camera_tree.item(selection[0])
        source_id = item['values'][0]
        self._edit_camera_by_source(source_id)
    
    def edit_from_table(self, tree: ttk.Treeview) -> None:
        """Edit camera from double-click"""
        selection = tree.selection()
        if not selection:
            return
        
        item = tree.item(selection[0])
        source_id = item['values'][0]
        self._edit_camera_by_source(source_id)
    
    def _edit_camera_by_source(self, source_id: str) -> None:
        """Edit camera by source ID"""
        for camera in self.cameras_data:
            if str(camera.get('source_id')) == str(source_id):
                # Store all camera data
                self.form_data = camera.copy()
                self.editing_camera_id = camera.get('id')
                self.current_screenshot = camera.get('screenshot')
                self.current_step = 1
                
                # Switch to add_camera page without resetting
                self.current_page = 'add_camera'
                
                # Update menu buttons
                for btn_id, btn in self.menu_buttons.items():
                    if btn_id == 'add_camera':
                        btn.config(
                            bg=COLORS['accent_cyan'], 
                            fg=COLORS['bg_dark'],
                            font=("Segoe UI", 12, "bold")
                        )
                    else:
                        btn.config(
                            bg=COLORS['bg_sidebar'], 
                            fg=COLORS['text_secondary'],
                            font=("Segoe UI", 12, "bold")
                        )
                
                # Clear content and show wizard
                for widget in self.content_frame.winfo_children():
                    widget.destroy()
                
                self.show_wizard()
                break
    
    def delete_selected_camera(self) -> None:
        """Delete selected camera"""
        if not hasattr(self, 'camera_tree'):
            messagebox.showwarning(
                self.t('warning'),
                "⚠ No camera table available"
            )
            return
        
        selection = self.camera_tree.selection()
        if not selection:
            messagebox.showwarning(
                self.t('warning'),
                "⚠ Please select a camera to delete"
            )
            return
        
        if not messagebox.askyesno(
            self.t('confirm'),
            "⚠ Are you sure you want to delete this camera?"
        ):
            return
        
        item = self.camera_tree.item(selection[0])
        source_id = item['values'][0]
        
        self.cameras_data = [
            c for c in self.cameras_data 
            if str(c.get('source_id')) != str(source_id)
        ]
        
        if self.save_data():
            messagebox.showinfo(
                self.t('success'),
                "✓ Camera deleted successfully!"
            )
            self.filtered_data = self.cameras_data.copy()
            self.show_cameras()
    
    def export_to_excel(self) -> None:
        """Export data to Excel"""
        if not self.cameras_data:
            messagebox.showwarning(
                self.t('warning'),
                "⚠ No data to export"
            )
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Save Excel File",
            initialfile=f"cameras_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        if file_path:
            try:
                df = pd.DataFrame(self.cameras_data)
                
                # Remove internal columns
                columns_to_remove = ['screenshot', 'id', 'created_at', 'updated_at']
                for col in columns_to_remove:
                    if col in df.columns:
                        df = df.drop(col, axis=1)
                
                # Reorder columns
                priority_cols = [
                    'source_id', 'brand', 'rtsp_area',
                    'feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5',
                    'working_hours', 'non_working_hours', 'layout_missing',
                    'serial_ws', 'layout_file', 'ip_user_pass'
                ]
                
                available_cols = [col for col in priority_cols if col in df.columns]
                other_cols = [col for col in df.columns if col not in priority_cols]
                df = df[available_cols + other_cols]
                
                df.to_excel(file_path, index=False, engine='openpyxl')
                
                messagebox.showinfo(
                    self.t('success'),
                    f"✓ Data exported successfully!\n\n{file_path}"
                )
            except Exception as e:
                messagebox.showerror(
                    self.t('error'),
                    f"❌ Export failed: {str(e)}"
                )
    
    def import_from_excel(self) -> None:
        """Import data from Excel"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ],
            title="Select Excel File"
        )
        
        if file_path:
            try:
                df = pd.read_excel(file_path)
                df = df.fillna('')
                
                imported_data = df.to_dict('records')
                
                imported_count = 0
                for record in imported_data:
                    if record.get('source_id'):
                        max_id = max(
                            [int(c.get('id', 0)) for c in self.cameras_data] + [0]
                        )
                        record['id'] = str(max_id + imported_count + 1)
                        record['created_at'] = datetime.now().isoformat()
                        record['updated_at'] = datetime.now().isoformat()
                        
                        self.cameras_data.append(record)
                        imported_count += 1
                
                if imported_count > 0:
                    self.save_data()
                    messagebox.showinfo(
                        self.t('success'),
                        f"✓ Successfully imported {imported_count} cameras!"
                    )
                    self.filtered_data = self.cameras_data.copy()
                    self.show_cameras()
                else:
                    messagebox.showwarning(
                        self.t('warning'),
                        "⚠ No valid cameras found in the file"
                    )
                    
            except Exception as e:
                messagebox.showerror(
                    self.t('error'),
                    f"❌ Import failed: {str(e)}"
                )


def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Try to set icon
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Initialize app
    app = AICameraApp(root, lang='en')  # Change to 'ar' for Arabic
    
    # Handle window closing
    def on_closing():
        app.auto_save_enabled = False
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()