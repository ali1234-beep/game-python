class WaveManager:
    def __init__(self):
        self.start_button = pygame.Rect(50, 500, 200, 50)
        
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                self.start_wave_instantly()
                
    def start_wave_instantly(self):
        self.wave_timer = 0
        self.spawn_wave()
        
    def draw(self, screen):
        if not self.active_wave:
            pygame.draw.rect(screen, (0, 255, 0), self.start_button)
            font = pygame.font.Font(None, 36)
            text = font.render("Start Wave", True, (0, 0, 0))
            screen.blit(text, (
                self.start_button.centerx - text.get_width()//2,
                self.start_button.centery - text.get_height()//2
            ))