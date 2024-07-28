
class Color:
    white = (255, 255, 255, 255)
    grey = (127, 127, 127, 255)
    black = (0, 0, 0, 255)

    red = (255, 0, 0, 255)
    green = (0, 255, 0, 255)
    blue = (0, 0, 255, 255)

    yellow = (255, 255, 0, 255)
    magenta = (255, 0, 255, 255)
    cyan = (0, 255, 255, 255)

    @staticmethod
    def get_transparent_color(color, alpha: int):
        """ Return a color with the given transparency
        
        Args:
            color: The color to be made transparent
            alpha: The transparency of the color in range [0, 255]
        """
        if alpha > 255 or alpha < 0:
            raise ValueError("Alpha must be in range [0, 255]")
        return (color[0], color[1], color[2], alpha)
        