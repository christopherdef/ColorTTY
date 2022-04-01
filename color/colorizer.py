
class Colorizer():
    '''
    Utility class for turning 

    Primary use through the `color_text` method
    
    Example usage:
    ```
        c = Colorizer()
        print(
            c.color_text('red', 'text'),
            c('y', 'text'),
            c(206, 'text', 'b'),
            c(2, 'text', 55),
        )
    ```

    '''
    ESC = None
    SETUP_COMPLETE = False

    
    def __init__(self, suppress_warnings=False, escape_char=None):
        Colorizer._setup(suppress_warnings, escape_char)

    def __call__(self, *args, **kwargs):
        '''
        Mapped to `color_text`
        '''
        return self.color_text(*args, **kwargs)
            
    def color_text(self, fg_color, text, bg_color=None):
        '''
        ANSI escapes the provided text with the specified foreground and background colors
        
        `fg_color` and `bg_color` can be any:
        - name of a color in `Colorizer.NAMED_COLORS`
        - color abbreviation in `Colorizer.char2cname`
        - number 0-255
        '''
        # unable to find esc char in setup, return raw text
        if Colorizer.ESC is None:
            return text

        # accept full cnames, single characters, and integers as colors
        def try_get_color_code(c):
            c = str(c).strip().upper()
            if c.isdigit():
                return c
            else:
                if len(c) == 1:
                    c = Colorizer.char2cname.get(c)
                    
                # default: WHITE
                return Colorizer.cname2code.get(c, 15)

        # setup foreground color
        fg_code = try_get_color_code(fg_color)
        color_header = f"{Colorizer.ESC}[38;5;{fg_code}"

        # setup background color
        if bg_color is not None:
            bg_code = try_get_color_code(bg_color)
            color_header += f';48;5;{bg_code}'
        
        # terminate header
        color_header += 'm'

        # terminate color
        color_footer = f'{Colorizer.ESC}[0m'

        return f'{color_header}{text}{color_footer}'
    
    def print_all_colors(self, num_cols=8, bg_color=None):
        '''
        See all the color available in a table
        '''
        column_idx = 0
        num_cols = max(num_cols, 1)
        print()
        for c in range(256):
            column_idx = (column_idx + 1)%num_cols
            print(self.color_text(c, c, bg_color=bg_color), end='\t')
            if column_idx == 0:
                print()
        print()

    @staticmethod
    def _setup(suppress_warnings=False, escape_char=None):
        '''
        Once-per-runtime setup
        
        Sets up NAMED_COLORS and gets system's ANSI color escape
        '''
        # only setup once per runtime
        if Colorizer.SETUP_COMPLETE:
            return
        

        Colorizer.char2cname = dict(zip('R   G     Y      B    M       C    W'.split(), 
                                        'RED GREEN YELLOW BLUE MAGENTA CYAN WHITE'.split()))

        Colorizer.cname2code = dict(zip('GREY RED GREEN YELLOW BLUE MAGENTA CYAN WHITE DARKRED'.split(), 
                                        [8,   9,  10,   11,    12,  13,     14,  15,   1]))

        Colorizer.NAMED_COLORS = list(Colorizer.cname2code.keys())

        # setup ANSI color escape for different operating systems
        Colorizer.ESC = escape_char
        if Colorizer.ESC is None:
            import os
            if 'nt' in os.name:
                os.system("color")
                Colorizer.ESC = '\033'
            elif 'posix' in os.name:
                Colorizer.ESC = '\x1b'
        
        # warn user if color won't be shown
        if Colorizer.ESC is None and not suppress_warnings:
            print('WARNING: Unable to find ANSI escape character for this operating system, colors will not appear')
        
        Colorizer.SETUP_COMPLETE = True

    


