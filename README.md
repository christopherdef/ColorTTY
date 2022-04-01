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

