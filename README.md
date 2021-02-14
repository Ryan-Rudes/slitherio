# Slitherio

Made with Python Selenium

This connects to the internet via a Chrome browser in developer mode, navigates through the slither.io page, and can take screenshots of the current game, render them in a Pyglet window, and even allow you to remotely control the snake programatically by calling the `.step(angle, acceleration)` function, where `acceleration` is a binary value indicating whether to accelerate or not. You can run in debug mode with the approperiate argument upon initializing a `Slitherio` instance, and this will show the Chrome browser will the agent is operating. Otherwise, you can always just call `.render()` occasionally to visualize the game in a Pyglet window. Finally, you can specify the nickname of your snake with the `nickname` argument when initializing a `Slitherio` instance, and the bot will input this into the text field accordingly.
