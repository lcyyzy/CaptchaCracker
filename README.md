# captcha_cracker
A cracker for sliding captcha of GEETEST, NetEase, Tencent and iQiyi based on OpenCV

![img](https://github.com/lcyyzy/CaptchaCracker/raw/master/img/captcha.gif)

## Overview
### Environment
macOS Mojave Version 10.14.1

### Requirement
- Python 3.6.1
- Selenium 3.11.0
- cv2 4.0.0
- PIL 1.1.7
- Chrome 76.0.3809.100
- ChromeDriver 76.0.3809.126

### Download and Installation
#### Denpendency Installation
Download ```ChromeDriver``` from https://chromedriver.chromium.org/downloads

```bash
brew install selenium-server-standalone
sudo pip install PIL
pip3 install virtualenv virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
export WORKON_HOME=$HOME/.virtualenvsexport PROJECT_HOME=$HOME/Develsource /usr/local/bin/virtualenvwrapper.sh
brew install opencv
echo /usr/local/opt/opencv/lib/python3.6/site-packages >> /usr/local/lib/python3.6/site-packages/opencv3.pth
```

#### Download
```bash
git clone https://github.com/lcyyzy/CaptchaCracker.git
```

### Run
```bash
CaptchaCracker
python cracker.py
```

## Implementation
### Get Background and Puzzle Piece
In order to prevent being cracked, the background in the sources of the front end is often cut into many small pieces and displayed after re-splicing. The first step is to get the orginal background picture and the puzzle piece.

We can get the moving coordinates of each small background pieces from the elements of the front end and perform the inverse operation to restore the original background.

![img](https://github.com/lcyyzy/CaptchaCracker/raw/master/img/fig1.png) ![img](https://github.com/lcyyzy/CaptchaCracker/raw/master/img/rightarrow.png) ![img](https://github.com/lcyyzy/CaptchaCracker/raw/master/img/origin.png)

We can get the puzzle piece from the sources directly.

![img](https://github.com/lcyyzy/CaptchaCracker/raw/master/img/puzzle.png)

### Get the Contour of Puzzle Piece and the Edge of Background
Extract the contour trajectory of the puzzle piece using ```cv2.findContours``` in the opencv and construct it into a two-dimensional matrix (operator).

![img](https://github.com/lcyyzy/CaptchaCracker/raw/master/img/shape-edge.jpg)

Process the background by ```cv2.GaussianBlur``` and the Canny edge detection operator - ```cv2.Canny``` to find the edge in the background.

![img](https://github.com/lcyyzy/CaptchaCracker/raw/master/img/origin-canny.jpg)

### Find the Position of Puzzle Piece
Use cross-correlation operation to process the edge of background and the contour operator of the puzzle piece. The position with the largest value is the result.

We mark the upper left corner of the position with a red point to show its correctness.

![img](https://github.com/lcyyzy/CaptchaCracker/raw/master/img/mark.png)






