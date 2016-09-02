class PyGameDisplay:

    def __init__(self, gg2window):
        # Launch a pygame window. 
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (800,100)
        pygame.init()
        pyg_window = pygame.display.set_mode([gg2window.get_rect()[2],gg2window.get_rect()[3]])


    def run_as_thread(self, gg2window):
        t = threading.Thread(target=self.run(gg2window))
        t.daemon = True
        t.start()

    def run(self,gg2window):
        display_capture = surf.make_surface(gg2window.get_screenshot())
        display_capture =  pygame.transform.rotate(display_capture, -90)
        display_capture = pygame.transform.flip(display_capture, True, False)
        pyg_window.blit(display_capture, [0,0,gg2window.get_rect()[2],gg2window.get_rect()[3]])
        pygame.display.flip()

        

