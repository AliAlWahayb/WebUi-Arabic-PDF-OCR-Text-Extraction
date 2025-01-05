import arabic_reshaper
from bidi.algorithm import get_display
def display_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text) # correct its shape
    bidi_text = get_display(reshaped_text) # correct its direction
    return bidi_text


# Example usage (if running as a standalone script):
if __name__ == "__main__":
    text = "السلام عليكم"
    print(display_arabic(text))
