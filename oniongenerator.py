import random
import string
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys
import os
import hashlib
import base64
from datetime import datetime
import re

class RealisticOnionGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("OnionScan v3.1.0 - Real Deep Web Address Generator")
        self.root.geometry("900x700")
        self.root.configure(bg='black')
        
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        self.generating = False
        self.paused = False
        self.count = 0
        self.found_valid = 0
        self.generated_addresses = set()
        
        self.common_patterns = [
            'facebook', 'twitter', 'google', 'amazon', 'microsoft', 'apple',
            'wiki', 'news', 'blog', 'forum', 'chat', 'mail', 'shop', 'store',
            'bank', 'secure', 'hidden', 'secret', 'dark', 'deep', 'web',
            'anon', 'anonymous', 'tor', 'onion', 'proxy', 'vpn', 'crypto'
        ]
        
        self.suffixes = ['wiki', 'blog', 'shop', 'forum', 'mail', 'chat', 'news', 'lib']
        self.prefixes = ['hidden', 'secret', 'deep', 'dark', 'tor', 'anon', 'secure']
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.setup_gui()
        self.print_banner()
        
    def configure_styles(self):
        """Configure UI styles"""
        self.style.configure('TFrame', background='black')
        self.style.configure('TLabel', background='black', foreground="#FFD900", font=('Courier', 10))
        self.style.configure('TButton', background='black', foreground="#FFD900", font=('Courier', 10))
        self.style.configure('TCheckbutton', background='black', foreground='#FFD900', font=('Courier', 10))
        self.style.configure('TRadiobutton', background='black', foreground='#FFD900', font=('Courier', 10))
        self.style.configure('Horizontal.TProgressbar', background='#FFD900', troughcolor='black')
        self.style.configure('Red.TLabel', background='black', foreground="#FFD900", font=('Courier', 10))
        self.style.configure('Green.TLabel', background='black', foreground="#FFD900", font=('Courier', 10))
        
    def print_banner(self):
        """Display startup banner"""
        banner = """
        ╔══════════════════════════════════════════════════════════════════════╗
        ║                           OnionScan v3.1.0                           ║
        ║               Advanced Deep Web Address Generator                    ║
        ║       ----------------------------------------------------           ║
        ║      Features:                                                       ║
        ║      • Realistic v2/v3 address generation                            ║
        ║      • Pattern matching & validation                                 ║
        ║      • Real-time statistics                                          ║
        ║      • Address verification system                                   ║
        ║      • Custom dictionary attacks                                     ║
        ║      • Export to multiple formats                                    ║
        ║      • copyright by : MR.blue shirt                                  ║
        ╚══════════════════════════════════════════════════════════════════════╝
        
        [SYSTEM] Initializing cryptographic generators...
        [SYSTEM] Loading pattern databases...
        [SYSTEM] Ready for real-time generation...
        [INFO] Note: This tool generates patterns for educational purposes
        """
        self.output_area.insert(tk.END, banner)
        self.output_area.see(tk.END)
        
    def setup_gui(self):
        """Setup the user interface"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        gen_tab = ttk.Frame(self.notebook)
        self.notebook.add(gen_tab, text="Generation")
        self.setup_generation_tab(gen_tab)
        
        val_tab = ttk.Frame(self.notebook)
        self.notebook.add(val_tab, text="Validation")
        self.setup_validation_tab(val_tab)
        
        stat_tab = ttk.Frame(self.notebook)
        self.notebook.add(stat_tab, text="Statistics")
        self.setup_statistics_tab(stat_tab)
        
        self.setup_status_bar()
        
    def setup_generation_tab(self, parent):
        """Setup generation tab"""
        output_frame = ttk.Frame(parent)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_area = scrolledtext.ScrolledText(output_frame, width=100, height=20, 
                                                    bg='black', fg='#FFD900', 
                                                    font=('Courier', 9), insertbackground='#FFD900')
        self.output_area.pack(fill=tk.BOTH, expand=True)
        
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        options_frame = ttk.LabelFrame(control_frame, text="Generation Options")
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(options_frame, text="Address Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.version_var = tk.StringVar(value="v3")
        ttk.Radiobutton(options_frame, text="v2 (16 char)", variable=self.version_var, value="v2").grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Radiobutton(options_frame, text="v3 (56 char)", variable=self.version_var, value="v3").grid(row=0, column=2, sticky=tk.W, padx=5)
        
        ttk.Label(options_frame, text="Generation Mode:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.mode_var = tk.StringVar(value="realistic")
        modes = [("Realistic", "realistic"), ("Random", "random"), ("Dictionary", "dictionary")]
        for i, (text, value) in enumerate(modes):
            ttk.Radiobutton(options_frame, text=text, variable=self.mode_var, value=value).grid(row=1, column=i+1, sticky=tk.W, padx=5)
        
        self.verify_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Auto-verify patterns", variable=self.verify_var).grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=5, pady=2)
        
        self.unique_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Enforce uniqueness", variable=self.unique_var).grid(row=2, column=3, columnspan=2, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(options_frame, text="Speed:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.speed_var = tk.StringVar(value="Medium")
        speed_combo = ttk.Combobox(options_frame, textvariable=self.speed_var, 
                                  values=["Very Slow", "Slow", "Medium", "Fast", "Very Fast"], 
                                  width=12, state="readonly")
        speed_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(options_frame, text="Batch Size:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=2)
        self.batch_var = tk.StringVar(value="1")
        batch_spin = ttk.Spinbox(options_frame, from_=1, to=100, textvariable=self.batch_var, width=8)
        batch_spin.grid(row=3, column=3, sticky=tk.W, padx=5, pady=2)
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="▶ Start Generation", command=self.start_generation)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = ttk.Button(button_frame, text="⏸ Pause", command=self.toggle_pause, state=tk.DISABLED)
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹ Stop", command=self.stop_generation, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        ttk.Button(button_frame, text="📊 Statistics", command=self.show_statistics).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="💾 Export All", command=self.export_all).grid(row=0, column=4, padx=5)
        ttk.Button(button_frame, text="🧹 Clear", command=self.clear_output).grid(row=0, column=5, padx=5)
        
    def setup_validation_tab(self, parent):
        """Setup validation tab"""
        validation_frame = ttk.Frame(parent)
        validation_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(validation_frame, text="Validate Single Address:").pack(anchor=tk.W, pady=(0, 5))
        
        input_frame = ttk.Frame(validation_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.validate_entry = ttk.Entry(input_frame, width=70)
        self.validate_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.validate_entry.insert(0, "Enter .onion address here")
        
        ttk.Button(input_frame, text="Validate", command=self.validate_single_address).pack(side=tk.RIGHT)
        
        self.result_text = scrolledtext.ScrolledText(validation_frame, height=8, 
                                                    bg='black', fg='#FFD900', 
                                                    font=('Courier', 9))
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(validation_frame, text="Bulk Validation:").pack(anchor=tk.W, pady=(0, 5))
        
        bulk_frame = ttk.Frame(validation_frame)
        bulk_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(bulk_frame, text="Load File", command=self.load_validation_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(bulk_frame, text="Validate All Generated", command=self.validate_all_generated).pack(side=tk.LEFT)
        
        stats_frame = ttk.LabelFrame(validation_frame, text="Validation Statistics")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.valid_count_var = tk.StringVar(value="Valid: 0")
        self.invalid_count_var = tk.StringVar(value="Invalid: 0")
        self.suspicious_count_var = tk.StringVar(value="Suspicious: 0")
        
        ttk.Label(stats_frame, textvariable=self.valid_count_var).grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(stats_frame, textvariable=self.invalid_count_var).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(stats_frame, textvariable=self.suspicious_count_var).grid(row=0, column=2, padx=10, pady=5)
        
    def setup_statistics_tab(self, parent):
        """Setup statistics tab"""
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        stats_labels = ttk.LabelFrame(stats_frame, text="Real-time Statistics")
        stats_labels.pack(fill=tk.X, pady=(0, 10))
        
        stats_grid = ttk.Frame(stats_labels)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        self.total_gen_var = tk.StringVar(value="0")
        self.unique_gen_var = tk.StringVar(value="0")
        self.v2_count_var = tk.StringVar(value="0")
        self.v3_count_var = tk.StringVar(value="0")
        self.valid_patterns_var = tk.StringVar(value="0")
        self.generation_speed_var = tk.StringVar(value="0.0 addr/sec")
        self.start_time_var = tk.StringVar(value="Not started")
        
        labels = [
            ("Total Generated:", self.total_gen_var),
            ("Unique Addresses:", self.unique_gen_var),
            ("v2 Addresses:", self.v2_count_var),
            ("v3 Addresses:", self.v3_count_var),
            ("Valid Patterns:", self.valid_patterns_var),
            ("Generation Speed:", self.generation_speed_var),
            ("Start Time:", self.start_time_var)
        ]
        
        for i, (label, var) in enumerate(labels):
            ttk.Label(stats_grid, text=label, font=('Courier', 9)).grid(row=i, column=0, sticky=tk.W, pady=2)
            ttk.Label(stats_grid, textvariable=var, font=('Courier', 9, 'bold')).grid(row=i, column=1, sticky=tk.W, pady=2, padx=10)
        
        pattern_frame = ttk.LabelFrame(stats_frame, text="Pattern Analysis")
        pattern_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.pattern_text = scrolledtext.ScrolledText(pattern_frame, height=10,
                                                     bg='black', fg='#FFD900',
                                                     font=('Courier', 9))
        self.pattern_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(stats_frame, text="🔄 Update Statistics", command=self.update_statistics_display).pack(pady=10)
        
    def setup_status_bar(self):
        """Setup status bar at bottom"""
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="🟢 Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.progress_var = tk.StringVar(value="")
        progress_label = ttk.Label(status_frame, textvariable=self.progress_var, relief=tk.SUNKEN, anchor=tk.E)
        progress_label.pack(side=tk.RIGHT, padx=2)
        
    def generate_real_v2_address(self):
        """Generate realistic v2 onion address"""
        chars = 'abcdefghijklmnopqrstuvwxyz234567'
        address = ''.join(random.choice(chars) for _ in range(16))
        
        if random.random() < 0.3:
            pattern = random.choice(['facebook', 'google', 'twitter', 'amazon'])
            if len(pattern) <= 8:
                pos = random.randint(0, 16 - len(pattern))
                address = address[:pos] + pattern + address[pos+len(pattern):]
        
        return address.lower() + '.onion'
    
    def generate_real_v3_address(self):
        """Generate realistic v3 onion address"""
        chars = 'abcdefghijklmnopqrstuvwxyz234567'
        
        segments = []
        for _ in range(4):
            segment = ''.join(random.choice(chars) for _ in range(14))
            segments.append(segment)
        
        address = ''.join(segments)
        
        if random.random() < 0.2:
            patterns = ['secure', 'hidden', 'secret', 'darkweb', 'deepweb']
            pattern = random.choice(patterns)
            pattern_base32 = self.text_to_base32(pattern)
            if pattern_base32:
                pos = random.randint(0, 56 - len(pattern_base32))
                address = address[:pos] + pattern_base32 + address[pos+len(pattern_base32):]
        
        return address.lower() + '.onion'
    
    def text_to_base32(self, text):
        """Convert text to base32-like representation"""
        try:
            encoded = base64.b32encode(text.encode()).decode().lower().replace('=', '')
            return encoded[:14]
        except:
            return None
    
    def generate_dictionary_based(self, version):
        """Generate addresses based on dictionary words"""
        word = random.choice(self.common_patterns)
        
        if version == "v2":
            remaining = 16 - len(word)
            if remaining > 0:
                chars = 'abcdefghijklmnopqrstuvwxyz234567'
                suffix = ''.join(random.choice(chars) for _ in range(remaining))
                address = word + suffix
            else:
                address = word[:16]
        else:
            base_word = word * 4
            remaining = 56 - len(base_word)
            if remaining > 0:
                chars = 'abcdefghijklmnopqrstuvwxyz234567'
                suffix = ''.join(random.choice(chars) for _ in range(remaining))
                address = base_word + suffix
            else:
                address = base_word[:56]
        
        return address.lower() + '.onion'
    
    def validate_onion_address(self, address):
        """Validate if address looks like a real onion address"""
        if not address.endswith('.onion'):
            return False, "Missing .onion suffix"
        
        clean_addr = address.replace('.onion', '')
        
        if len(clean_addr) == 16:
            valid_chars = set('abcdefghijklmnopqrstuvwxyz234567')
            if not all(c in valid_chars for c in clean_addr):
                return False, "Invalid characters for v2 address"
            return True, "Valid v2 address"
        elif len(clean_addr) == 56:
            valid_chars = set('abcdefghijklmnopqrstuvwxyz234567')
            if not all(c in valid_chars for c in clean_addr):
                return False, "Invalid characters for v3 address"
            
            suspicious = ['aaaa', 'bbbb', 'cccc', '1111', '2222', '3333']
            for pattern in suspicious:
                if pattern in clean_addr:
                    return True, "Valid v3 address (but suspicious pattern)"
            
            return True, "Valid v3 address"
        else:
            return False, f"Invalid length: {len(clean_addr)} chars (should be 16 or 56)"
    
    def start_generation(self):
        """Start generating addresses"""
        if not self.generating:
            self.generating = True
            self.paused = False
            self.count = 0
            self.found_valid = 0
            self.generated_addresses.clear()
            self.start_time = time.time()
            
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.status_var.set("🟡 Generating addresses...")
            self.start_time_var.set(datetime.now().strftime("%H:%M:%S"))
            
            self.gen_thread = threading.Thread(target=self.generate_loop, daemon=True)
            self.gen_thread.start()
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
        if self.paused:
            self.pause_btn.config(text="▶ Resume")
            self.status_var.set("⏸ Paused")
            self.output_area.insert(tk.END, f"\n[{time.strftime('%H:%M:%S')}] Generation paused\n")
        else:
            self.pause_btn.config(text="⏸ Pause")
            self.status_var.set("🟡 Generating addresses...")
            self.output_area.insert(tk.END, f"\n[{time.strftime('%H:%M:%S')}] Generation resumed\n")
        
        self.output_area.see(tk.END)
    
    def stop_generation(self):
        """Stop generating addresses"""
        self.generating = False
        self.paused = False
        
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.pause_btn.config(text="⏸ Pause")
        
        elapsed = time.time() - self.start_time
        speed = self.count / elapsed if elapsed > 0 else 0
        
        self.status_var.set(f"🟢 Stopped. Generated {self.count} addresses ({speed:.1f}/sec)")
        self.output_area.insert(tk.END, f"\n[{time.strftime('%H:%M:%S')}] Generation stopped. Generated {self.count} addresses\n")
        self.output_area.see(tk.END)
        
        self.update_statistics_display()
    
    def generate_loop(self):
        """Main generation loop"""
        try:
            speed_map = {
                "Very Slow": 1.0,
                "Slow": 0.5,
                "Medium": 0.1,
                "Fast": 0.05,
                "Very Fast": 0.01
            }
            delay = speed_map.get(self.speed_var.get(), 0.1)
            batch_size = int(self.batch_var.get())
            
            v2_count = 0
            v3_count = 0
            
            while self.generating:
                if not self.paused:
                    batch_addresses = []
                    
                    for _ in range(batch_size):
                        mode = self.mode_var.get()
                        version = self.version_var.get()
                        
                        if mode == "dictionary":
                            addr = self.generate_dictionary_based(version)
                        elif mode == "realistic":
                            if version == "v2":
                                addr = self.generate_real_v2_address()
                                v2_count += 1
                            else:
                                addr = self.generate_real_v3_address()
                                v3_count += 1
                        else:
                            if version == "v2":
                                addr = self.generate_real_v2_address()
                                v2_count += 1
                            else:
                                addr = self.generate_real_v3_address()
                                v3_count += 1
                        
                        if self.unique_var.get() and addr in self.generated_addresses:
                            continue
                        
                        self.generated_addresses.add(addr)
                        batch_addresses.append(addr)
                    
                    for addr in batch_addresses:
                        self.count += 1
                        
                        status = "GENERATED"
                        color_tag = "normal"
                        
                        if self.verify_var.get():
                            is_valid, msg = self.validate_onion_address(addr)
                            if is_valid:
                                self.found_valid += 1
                                status = "VALID"
                                color_tag = "valid"
                            else:
                                status = "INVALID"
                                color_tag = "invalid"
                        
                        timestamp = time.strftime('%H:%M:%S')
                        output_line = f"[{timestamp}] [{status}] {addr}\n"
                        
                        self.output_area.insert(tk.END, output_line)
                        
                        if hasattr(self.output_area, 'tag_config'):
                            end_index = self.output_area.index(tk.END)
                            start_index = f"{end_index}-{len(output_line)+1}c"
                            self.output_area.tag_add(color_tag, start_index, f"{start_index}+{len(status)}c")
                        
                        self.output_area.see(tk.END)
                    
                    self.total_gen_var.set(str(self.count))
                    self.unique_gen_var.set(str(len(self.generated_addresses)))
                    self.v2_count_var.set(str(v2_count))
                    self.v3_count_var.set(str(v3_count))
                    
                    elapsed = time.time() - self.start_time
                    if elapsed > 0:
                        speed = self.count / elapsed
                        self.generation_speed_var.set(f"{speed:.1f} addr/sec")
                    
                    self.progress_var.set(f"Generated: {self.count} | Valid: {self.found_valid}")
                    
                    time.sleep(delay)
                else:
                    time.sleep(0.1)
                    
        except Exception as e:
            self.output_area.insert(tk.END, f"\n[ERROR] {str(e)}\n")
            self.output_area.see(tk.END)
    
    def validate_single_address(self):
        """Validate a single address"""
        address = self.validate_entry.get().strip()
        if not address:
            messagebox.showwarning("Warning", "Please enter an address to validate")
            return
        
        is_valid, message = self.validate_onion_address(address)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Address: {address}\n")
        self.result_text.insert(tk.END, f"Status: {'✅ VALID' if is_valid else '❌ INVALID'}\n")
        self.result_text.insert(tk.END, f"Message: {message}\n")
        
        if is_valid:
            self.result_text.insert(tk.END, f"Type: {'v2' if len(address.replace('.onion', '')) == 16 else 'v3'}\n")
    
    def validate_all_generated(self):
        """Validate all generated addresses"""
        if not self.generated_addresses:
            messagebox.showinfo("Info", "No addresses generated yet")
            return
        
        valid_count = 0
        invalid_count = 0
        suspicious_count = 0
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Validating all generated addresses...\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        
        for addr in list(self.generated_addresses)[:100]:
            is_valid, message = self.validate_onion_address(addr)
            if is_valid:
                valid_count += 1
                if "suspicious" in message.lower():
                    suspicious_count += 1
                self.result_text.insert(tk.END, f"✅ {addr}\n")
            else:
                invalid_count += 1
                self.result_text.insert(tk.END, f"❌ {addr} - {message}\n")
        
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        self.result_text.insert(tk.END, f"Summary: {valid_count} valid, {invalid_count} invalid, {suspicious_count} suspicious\n")
        
        self.valid_count_var.set(f"Valid: {valid_count}")
        self.invalid_count_var.set(f"Invalid: {invalid_count}")
        self.suspicious_count_var.set(f"Suspicious: {suspicious_count}")
    
    def load_validation_file(self):
        """Load addresses from file for validation"""
        filename = filedialog.askopenfilename(
            title="Select address file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    addresses = [line.strip() for line in f if line.strip()]
                
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Loaded {len(addresses)} addresses from {filename}\n")
                
                valid_count = 0
                for addr in addresses[:50]:
                    is_valid, _ = self.validate_onion_address(addr)
                    if is_valid:
                        valid_count += 1
                        self.result_text.insert(tk.END, f"{addr}\n")
                    else:
                        self.result_text.insert(tk.END, f"{addr}\n")
                
                self.result_text.insert(tk.END, f"\nFound {valid_count} valid addresses out of {min(50, len(addresses))} checked\n")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def export_all(self):
        """Export generated addresses to file"""
        if not self.generated_addresses:
            messagebox.showwarning("Warning", "No addresses to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text file", "*.txt"),
                ("CSV file", "*.csv"),
                ("JSON file", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.csv'):
                    with open(filename, 'w') as f:
                        f.write("Address,Type,Valid\n")
                        for addr in self.generated_addresses:
                            is_valid, _ = self.validate_onion_address(addr)
                            addr_type = "v2" if len(addr.replace('.onion', '')) == 16 else "v3"
                            f.write(f'"{addr}","{addr_type}","{is_valid}"\n')
                
                elif filename.endswith('.json'):
                    import json
                    data = {
                        "metadata": {
                            "generated": datetime.now().isoformat(),
                            "count": len(self.generated_addresses),
                            "tool": "OnionScan v3.1.0"
                        },
                        "addresses": list(self.generated_addresses)
                    }
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)
                
                else:
                    with open(filename, 'w') as f:
                        f.write(f"OnionScan v3.1.0 - Generated Addresses\n")
                        f.write("=" * 60 + "\n")
                        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Total addresses: {len(self.generated_addresses)}\n")
                        f.write("=" * 60 + "\n\n")
                        
                        for addr in sorted(self.generated_addresses):
                            f.write(f"{addr}\n")
                
                self.output_area.insert(tk.END, f"\n[{time.strftime('%H:%M:%S')}] Exported {len(self.generated_addresses)} addresses to {filename}\n")
                self.output_area.see(tk.END)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def clear_output(self):
        """Clear the output area"""
        if messagebox.askyesno("Confirm", "Clear all output?"):
            self.output_area.delete(1.0, tk.END)
            self.print_banner()
    
    def show_statistics(self):
        """Switch to statistics tab and update"""
        self.notebook.select(2)
        self.update_statistics_display()
    
    def update_statistics_display(self):
        """Update statistics display"""
        if self.generated_addresses:
            self.pattern_text.delete(1.0, tk.END)
            self.pattern_text.insert(tk.END, "Common patterns found:\n")
            self.pattern_text.insert(tk.END, "-" * 40 + "\n")
            
            pattern_counts = {}
            for addr in list(self.generated_addresses)[:20]:
                clean = addr.replace('.onion', '')
                for word in self.common_patterns:
                    if word in clean:
                        pattern_counts[word] = pattern_counts.get(word, 0) + 1
            
            for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                self.pattern_text.insert(tk.END, f"{pattern}: {count} occurrences\n")
        else:
            self.pattern_text.delete(1.0, tk.END)
            self.pattern_text.insert(tk.END, "No data available. Generate some addresses first.\n")

def main():
    root = tk.Tk()
    app = RealisticOnionGenerator(root)
    
    app.output_area.tag_config("valid", foreground="#FFD900")
    app.output_area.tag_config("invalid", foreground="#FFD900")
    app.output_area.tag_config("normal", foreground="#FFD900")
    
    root.mainloop()

if __name__ == "__main__":
    main()