from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from gym.envs.classic_control.rendering import SimpleImageViewer
from io import BytesIO
from PIL import Image
from tqdm import tqdm
import numpy as np
import random
import gym

def try_forever(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        except:
            continue

class Slitherio(gym.Env):
    def __init__(self, nickname, size=(350, 350), debug=False):
        self.nickname = nickname
        self.size = size
        self.debug = debug
        self.browser = webdriver.Chrome
        self.url = "http://slither.io/"
        self.xpaths = {
            'nickname': '/html/body/div[2]/div[4]/div[1]/input',
            'mainpage': '/html/body/div[2]',
            'scorebar': '/html/body/div[13]/span[1]/span[2]'
        }
        self.viewer = None

    def game_is_not_over(self):
        return self.browser.find_element_by_xpath(self.xpaths['mainpage']).value_of_css_property("display") == "none"

    def is_terminal(self):
        return self.browser.find_element_by_xpath(self.xpaths['mainpage']).value_of_css_property("display") != "none"

    def wait_until_can_enter_nickname(self):
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['nickname'])))

    def enter_nickame(self, nickname):
        self.wait_until_can_enter_nickname()
        field = self.browser.find_element_by_xpath(self.xpaths['nickname'])
        field.send_keys(self.nickname)
        return field

    def begin(self, field):
        self.wait_until_can_enter_nickname()
        field.send_keys(Keys.ENTER)

    def wait_until_game_has_loaded(self):
        WebDriverWait(self.browser, 1000).until(EC.invisibility_of_element((By.XPATH, self.xpaths['mainpage'])))

    def start(self):
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument('--disable-extensions')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--enable-precise-memory-info')
        options.add_argument('--ignore-ssl-errors=true --debug=true')
        options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        if not self.debug:
            options.add_argument("--headless")
        self.browser = self.browser(options = options)
        self.browser.set_window_size(*self.size)
        self.browser.get(self.url)
        self.wait_until_can_enter_nickname()
        self.field = self.enter_nickame(self.nickname)

    def reset(self):
        self.begin(self.field)
        self.wait_until_game_has_loaded()
        self.score = try_forever(self.get_score())
        return self.observe()

    def observe(self):
        canvas = self.browser.find_element_by_xpath('/html/body')
        location = canvas.location
        size = canvas.size
        png = self.browser.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        width = size['width']
        height = size['height']
        left = location['x']
        top = location['y']
        right = location['x'] + width
        bottom = location['y'] + height
        im = im.crop((left, top, right, bottom))
        im = (np.uint8(im) * 255)[:, :, :3][:, :, ::-1]
        self.last_observation = im
        return im / 255.0

    def render(self, mode='human'):
        if self.viewer is None:
            self.viewer = SimpleImageViewer()

        if self.last_observation is None:
            self.viewer.imshow(self.observe())
        else:
            self.viewer.imshow(self.last_observation)

        return None if mode == 'human' else self.last_observation

    def close(self):
        self.browser.close()
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def sample(self):
        angle = np.random.random() * 2 * np.pi
        acceleration = int(np.random.random() > 0.5)
        return angle, acceleration

    def get_score(self):
        return int(self.browser.find_element_by_xpath(self.xpaths['scorebar']).text)

    def compute_reward(self):
        new_score = try_forever(self.get_score)
        reward = new_score - self.score
        self.score = new_score
        return reward

    def step(self, angle, acceleration):
        angle *= 2 * np.pi
        x, y = np.cos(angle) * 360, np.sin(angle) * 360
        self.browser.execute_script("window.xm = %s; window.ym = %s; window.setAcceleration(%d);" % (x, y, acceleration))
        return self.observe(), self.compute_reward(), self.is_terminal(), {}
