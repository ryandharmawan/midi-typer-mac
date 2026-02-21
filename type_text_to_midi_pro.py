import tkinter as tk
from tkinter import messagebox, font as tkfont
from midiutil import MIDIFile

# Database Font 5x5 - Optimized
FONT = {
    'A': [(0,[1,2,3]), (1,[0,4]), (2,[0,1,2,3,4]), (3,[0,4]), (4,[0,4])],
    'B': [(0,[0,1,2,3]), (1,[0,4]), (2,[0,1,2,3]), (3,[0,4]), (4,[0,1,2,3])],
    'C': [(0,[1,2,3,4]), (1,[0]), (2,[0]), (3,[0]), (4,[1,2,3,4])],
    'D': [(0,[0,1,2,3]), (1,[0,4]), (2,[0,4]), (3,[0,4]), (4,[0,1,2,3])],
    'E': [(0,[0,1,2,3,4]), (1,[0]), (2,[0,1,2,3]), (3,[0]), (4,[0,1,2,3,4])],
    'F': [(0,[0,1,2,3,4]), (1,[0]), (2,[0,1,2,3]), (3,[0]), (4,[0])],
    'G': [(0,[1,2,3,4]), (1,[0]), (2,[0,2,3,4]), (3,[0,4]), (4,[1,2,3,4])],
    'H': [(0,[0,4]), (1,[0,4]), (2,[0,1,2,3,4]), (3,[0,4]), (4,[0,4])],
    'I': [(0,[0,1,2]), (1,[1]), (2,[1]), (3,[1]), (4,[0,1,2])],
    'J': [(0,[4]), (1,[4]), (2,[4]), (3,[0,4]), (4,[1,2,3])],
    'K': [(0,[0,4]), (1,[0,3]), (2,[0,1,2]), (3,[0,3]), (4,[0,4])],
    'L': [(0,[0]), (1,[0]), (2,[0]), (3,[0]), (4,[0,1,2,3,4])],
    'M': [(0,[0,4]), (1,[0,1,3,4]), (2,[0,2,4]), (3,[0,4]), (4,[0,4])],
    'N': [(0,[0,4]), (1,[0,1,4]), (2,[0,2,4]), (3,[0,3,4]), (4,[0,4])],
    'O': [(0,[1,2,3]), (1,[0,4]), (2,[0,4]), (3,[0,4]), (4,[1,2,3])],
    'P': [(0,[0,1,2,3]), (1,[0,4]), (2,[0,1,2,3]), (3,[0]), (4,[0])],
    'Q': [(0,[1,2,3]), (1,[0,4]), (2,[0,4,2]), (3,[0,3]), (4,[1,2,4])],
    'R': [(0,[0,1,2,3]), (1,[0,4]), (2,[0,1,2,3]), (3,[0,3]), (4,[0,4])],
    'S': [(0,[1,2,3,4]), (1,[0]), (2,[1,2,3]), (3,[4]), (4,[0,1,2,3])],
    'T': [(0,[0,1,2,3,4]), (1,[2]), (2,[2]), (3,[2]), (4,[2])],
    'U': [(0,[0,4]), (1,[0,4]), (2,[0,4]), (3,[0,4]), (4,[1,2,3])],
    'V': [(0,[0,4]), (1,[0,4]), (2,[0,4]), (3,[1,3]), (4,[2])],
    'W': [(0,[0,4]), (1,[0,4]), (2,[0,2,4]), (3,[0,1,3,4]), (4,[0,4])],
    'X': [(0,[0,4]), (1,[1,3]), (2,[2]), (3,[1,3]), (4,[0,4])],
    'Y': [(0,[0,4]), (1,[1,3]), (2,[2]), (3,[2]), (4,[2])],
    'Z': [(0,[0,1,2,3,4]), (1,[3]), (2,[2]), (3,[1]), (4,[0,1,2,3,4])],
}

class ModernMidiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Type Text To Midi")
        self.root.geometry("520x780")
        self.root.configure(bg="#1A1B1E")  # Dark theme premium

        # Definisi Font Modern
        self.header_font = tkfont.Font(family="Segoe UI", size=24, weight="bold")
        self.label_font = tkfont.Font(family="Segoe UI", size=10)
        self.button_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")

        # Header Section
        tk.Label(root, text="Type Text To Midi", font=self.header_font, 
                 bg="#1A1B1E", fg="#00FF9C").pack(pady=(30, 10))
        
        tk.Label(root, text="Enter your marker text below", font=self.label_font,
                 bg="#1A1B1E", fg="#9BA1A6").pack()

        # Input Box Section
        self.entry_var = tk.StringVar()
        self.entry_var.trace_add("write", self.update_preview)
        
        self.entry = tk.Entry(root, textvariable=self.entry_var, font=("Segoe UI", 18), 
                              width=25, bg="#2C2E33", fg="#FFFFFF", borderwidth=0, 
                              insertbackground="white", justify='center')
        self.entry.pack(pady=20, ipady=8)
        self.entry.focus_set()

        # Preview Section
        tk.Label(root, text="LIVE PREVIEW", font=self.label_font, bg="#1A1B1E", fg="#636669").pack(pady=(10, 5))
        self.preview_canvas = tk.Canvas(root, width=460, height=120, bg="#000000", 
                                        highlightthickness=1, highlightbackground="#3F4248")
        self.preview_canvas.pack(pady=5)

        # Options Container
        self.options_frame = tk.Frame(root, bg="#1A1B1E")
        self.options_frame.pack(pady=20, fill="x", padx=40)

        self.weight = self.create_modern_opt("Weight", ["Tiny", "Regular", "Bold"], "Bold")
        self.spacing = self.create_modern_opt("Spacing", ["Loose", "Dense"], "Dense")
        self.width_opt = self.create_modern_opt("Width", ["Narrow", "Medium", "Wide", "Very Wide"], "Very Wide")

        # Download Button
        self.dl_btn = tk.Button(root, text="GENERATE MIDI FILE", command=self.generate, 
                                bg="#00FF9C", fg="#000000", font=self.button_font, 
                                activebackground="#00D985", cursor="hand2", 
                                relief="flat", borderwidth=0, padx=40, pady=12)
        self.dl_btn.pack(pady=(20, 30))

    def create_modern_opt(self, label, options, default):
        container = tk.Frame(self.options_frame, bg="#1A1B1E")
        container.pack(pady=8, fill="x")
        
        tk.Label(container, text=label.upper(), font=("Segoe UI", 8, "bold"), 
                 bg="#1A1B1E", fg="#636669").pack(side="left")
        
        var = tk.StringVar(value=default)
        radio_frame = tk.Frame(container, bg="#1A1B1E")
        radio_frame.pack(side="right")
        
        for o in options:
            rb = tk.Radiobutton(radio_frame, text=o, variable=var, value=o, 
                                 bg="#1A1B1E", fg="#9BA1A6", selectcolor="#2C2E33",
                                 activebackground="#1A1B1E", activeforeground="#00FF9C",
                                 font=("Segoe UI", 9), command=self.update_preview)
            rb.pack(side="left", padx=5)
        return var

    def update_preview(self, *args):
        self.preview_canvas.delete("all")
        text = self.entry_var.get().upper()
        x = 20
        for char in text:
            if char in FONT:
                for row, cols in FONT[char]:
                    for col in cols:
                        # Draw preview with neon green color
                        self.preview_canvas.create_rectangle(
                            x + (col*4), 30 + (row*10), 
                            x + (col*4) + 3, 30 + (row*10) + 8, 
                            fill="#00FF9C", outline=""
                        )
                x += 16 if char == 'I' else 28
            elif char == " ":
                x += 18

    def generate(self):
        text = self.entry_var.get().upper().strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please type something before generating.")
            return
            
        midi = MIDIFile(1)
        midi.addTempo(0, 0, 120)

        w_map = {"Narrow": 1.0, "Medium": 2.0, "Wide": 4.0, "Very Wide": 8.0}
        w_scale = w_map[self.width_opt.get()]
        
        base_note = 72
        x_pos = 0

        for char in text:
            if char in FONT:
                char_w_scale = w_scale * 0.6 if char == 'I' else w_scale
                for row, cols in FONT[char]:
                    pitch = base_note - (row * 2)
                    cols.sort()
                    groups = []
                    current_group = [cols[0]]
                    for i in range(1, len(cols)):
                        if cols[i] == cols[i-1] + 1:
                            current_group.append(cols[i])
                        else:
                            groups.append(current_group)
                            current_group = [cols[i]]
                    groups.append(current_group)

                    for group in groups:
                        start_col = group[0]
                        duration = len(group) * char_w_scale
                        time = x_pos + (start_col * char_w_scale)
                        midi.addNote(0, 0, pitch, time, duration, 100)
                        if self.weight.get() == "Bold":
                            midi.addNote(0, 0, pitch - 1, time, duration, 100)
                
                gap_factor = 4 if char == 'I' else 6
                if self.spacing.get() == "Loose": gap_factor += 4
                x_pos += gap_factor * char_w_scale
                
            elif char == " ":
                x_pos += 8 * w_scale

        filename = f"{text.replace(' ', '_')}.mid"
        with open(filename, "wb") as f:
            midi.writeFile(f)
        messagebox.showinfo("Success", f"MIDI created: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMidiApp(root)
    root.mainloop()