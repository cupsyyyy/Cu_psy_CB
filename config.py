
class Config:
    def __init__(self):
        # --- General Settings ---

        self.enableaim = True
        self.enabletb = False
        self.offsetX = -2
        self.offsetY = 3

        self.color = "purple"

        
        # --- Mouse / MAKCU ---
        self.selected_mouse_button = 1
        self.selected_tb_btn = 1
        self.selected_2_tb = 2
        self.in_game_sens = 0.235
        self.mouse_dpi = 800
        # --- Aimbot Mode ---
        self.mode = "Normal"    

        self.fovsize = 100
        self.tbfovsize = 5 
        self.tbdelay = 0.5
        # --- Normal Aim ---
        self.normal_x_speed = 3
        self.normal_y_speed = 3

        self.normalsmooth = 30
        self.normalsmoothfov = 30
    

config = Config()