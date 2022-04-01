import logging
from typing import Dict
from color import Colorizer

class ColorFormatter(logging.Formatter):
    '''
    Formatter providing color to log outputs

    Allowed keys are in `ColorFormatter.FG_KEYS` and `ColorFormatter.BG_KEYS`

    Avoid using with FileHandlers, escape characters will likely end up in the files themselves
    
    Example usage:
    ```
        logger.info("msg", extra={'color':'yellow'})
        logger.info("msg", {'fg':'green', 'bg_color':'b'})
        logger.info("msg", {'fg':'r', 'bg':206})
        logger.info("msg", {'color':201})
    ```

    Args:
        logging (logging.Logger): Logger to use this formatter
        suppress_warnings (bool): Do not print warning if colors are unusable on this OS
        escape_char (bool): Manually provided ANSI escape character for terminal colors
    '''

    FG_KEYS = ['fg_color', 'fg', 'color', 'c']
    BG_KEYS = ['bg_color', 'bg']

    DEFAULT_COLORS = {
            logging.DEBUG: 'GREY',
            logging.INFO: 'WHITE',
            logging.WARNING: 'YELLOW',
            logging.ERROR: 'RED',
            logging.CRITICAL: 'DARKRED'
        }

    def __init__(self, suppress_warnings=False, escape_char=None, *args, **kwargs):
        
        self.default_colors = ColorFormatter.DEFAULT_COLORS
        self.colorizer = Colorizer(suppress_warnings, escape_char)

        super().__init__(*args, **kwargs)

    def set_default_colors(self, defaults: Dict[int, str]):
        '''
        Example:
        ```
        # makes `log.info` calls blue, and `log.critical` calls ANSI color 206
        formatter.set_default_colors({
            logging.INFO:'BLUE', 
            logging.CRITICAL:206
            })
        ```
        '''
        self.default_colors.update(defaults)

    def format(self, record):
        import sys

        # try not to add color if piping to file
        if not sys.stdout.isatty():
            return super().format(record)
        
        fg_color = None
        bg_color = None
        
        # look for fg and bg color declarations as positional or `extra` keyword args
        candidate_locations = [vars(record), record.args]
        for loc in candidate_locations:
            if len(loc) == 0 or not isinstance(loc, dict):
                continue
            for fg_key in ColorFormatter.FG_KEYS:
                if fg_color is None:
                    fg_color = loc.get(fg_key, None)

            for bg_key in ColorFormatter.BG_KEYS:
                if bg_color is None:
                    bg_color = loc.get(bg_key, None)

        if fg_color is None:
            fg_color = self.default_colors.get(record.levelno, 'WHITE')

        return self.colorizer.color_text(fg_color, super().format(record), bg_color=bg_color)
