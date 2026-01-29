#!/bin/bash
echo "Running sass main.scss main.css"
sass main.scss main.css
if [ $? -eq 0 ]; then
    echo "Sass compiled successfully"
else
    echo "Sass compilation failed"
fi

# Determine python command
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "Updating theme lists using $PYTHON_CMD..."
$PYTHON_CMD checkout_announcements.py
if [ $? -eq 0 ]; then
    echo "Python script executed successfully"
else
    echo "Python script execution failed"
fi

echo "Updating people lists using $PYTHON_CMD..."
$PYTHON_CMD checkout_people.py
if [ $? -eq 0 ]; then
    echo "Python script executed successfully"
else
    echo "Python script execution failed"
fi
