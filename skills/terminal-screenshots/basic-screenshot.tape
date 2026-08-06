# Basic Screenshot Example
# Captures a simple terminal screenshot

Output screenshot.png

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

# Hide setup commands
Hide
Type "clear"
Enter
Sleep 500ms
Show

# Your commands here
Type "echo 'Hello from VHS!'"
Enter
Sleep 500ms

Type "ls -la"
Enter
Sleep 1s

# Capture the screenshot
Screenshot screenshot.png
