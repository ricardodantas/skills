# Demo Recording Example
# Creates an animated GIF showing terminal usage

Output demo.gif

# Recommended settings for clean rendering
Set Width 1200
Set Height 700
Set FontSize 14
Set FontFamily "monospace"
Set LetterSpacing 0
Set Theme "Dracula"
Set Padding 10
Set WindowBar Colorful
Set WindowBarSize 40
Set TypingSpeed 50ms

# Clean start (hidden)
Hide
Type "clear"
Enter
Sleep 500ms
Show

# Demo sequence
Type "echo 'Welcome to the demo!'"
Sleep 300ms
Enter
Sleep 1s

Type "date"
Enter
Sleep 1s

Type "echo 'Creating a file...'"
Enter
Sleep 500ms

Type "echo 'Hello World' > demo.txt"
Enter
Sleep 500ms

Type "cat demo.txt"
Enter
Sleep 1s

Type "echo 'Done!'"
Enter
Sleep 2s
