from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

code = """def hello():
    print("Hello world")
"""
with open("test_code.png", "wb") as f:
    f.write(highlight(code, PythonLexer(), ImageFormatter(font_size=24, line_numbers=True)))
