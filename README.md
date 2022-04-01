# Using Colorizer

#### \# See available colors 
```py
from color import Colorizer
cz = Colorizer()
cz.print_all_colors()
```

#### \# Print colored text
```py
# note: cz(...) == cz.color_text(...)

print(
    cz.color_text('red', 'text'),
    cz('y', 'text'),
    cz(206, 'text', 'b'),
    cz(2, 'text', 55),
)
```


# Using ColorFormatter
```py
import logging
from color import ColorFormatter

logger = logging.getLogger("color_logger")
logger.setLevel(logging.DEBUG)
```

#### \# Initialize formatter
```py
formatter = ColorFormatter(fmt='[%(asctime)s] <%(levelname)s> %(message)s')

# change default colors of log levels as needed
formatter.set_default_colors({logging.CRITICAL:201})

# register formatter
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
```

#### \# Log levels are colored by default
```py
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message, changed default color")
```

#### \# Color can be further customized
```py
logger.info("cyan", extra={'fg':'cyan'})
logger.info("green", {'fg':'g'})
logger.info("blue/green", {'fg':'b', 'bg':'g'})
logger.info("custom pink", {'fg':201})
```