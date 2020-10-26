# Stitching Pig Carcass IMG

## Object

Let's stitching pig carcass image printed from vcs2000.

## Code
### requirement

python3
opencv-python
numpy
### Method summary
1. Interesting points in C1, C2 images are found by SIFT algorithm.
2. Only the points in the 30 pixcel on the right side of C1 image and the left side of C2 image are filtered out.
3. Filtered points are matched using FlannBasedMatcher.
4. Transpose the image using the mathced points information.
### Simple to use code
```
python main.py --c1 C1 --c2 C2 --out .
```
The images in C1 and C2 folder must be matched by their filenames.

## Input example
**C1**

![C1](https://user-images.githubusercontent.com/71325306/97154516-4fc9a080-17b7-11eb-92d1-a02c49764e19.jpg)

**C2**

![C2](https://user-images.githubusercontent.com/71325306/97154540-5821db80-17b7-11eb-9b12-6b43057be9d5.jpg)
## Output
![C1C2](https://user-images.githubusercontent.com/71325306/97154577-65d76100-17b7-11eb-9ca5-39258ac40bd9.jpg)
