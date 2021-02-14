# Slitherio

Made with Python Selenium

This connects to the internet via a Chrome browser in developer mode, navigates through the slither.io page, and can take screenshots of the current game, render them in a Pyglet window, and even allow you to remotely control the snake programatically by calling the `.step(angle, acceleration)` function, where `acceleration` is a binary value indicating whether to accelerate or not. You can run in debug mode with the approperiate argument upon initializing a `Slitherio` instance, and this will show the Chrome browser will the agent is operating. Otherwise, you can always just call `.render()` occasionally to visualize the game in a Pyglet window. Finally, you can specify the nickname of your snake with the `nickname` argument when initializing a `Slitherio` instance, and the bot will input this into the text field accordingly. Also, the `size` argument is used to specify the size of the screenshots.

## Example

```python
import random

env = Slitherio(nickname = "Bot", size = (350, 350), debug = True)
env.start()

while True:
    observation = env.reset()
    terminal = False
    while not terminal:
        angle = random.random() # Specify an angle as a float between 0-1, it converts it to radians automatically
        acceleration = int(random.random() > 0.5)
        observation, reward, terminal, info = env.step(angle, acceleration)
        env.render()

env.close()
```
> <a href="https://www.youtube.com/watch?v=rnbWEs4yOrY&feature=youtu.be"><img src="https://i.ibb.co/fC4Lh84/ezgif-3-a8bab272bfcb.gif"></a>

You have to actually terminate the episode when you receive a value of `True` from `terminal`. Otherwise, there will be a problem because you cannot view the current score after the game has ended (once the scoreboard has vanished) without throwing an error.
