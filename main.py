import os
import tqdm
import argparse
import cv2
from data_load import *
#python main.py --c1 C1 --c2 C2 --out joint2


##parser
parser = argparse.ArgumentParser()
parser.add_argument("--c1")
parser.add_argument("--c2")
parser.add_argument("--out",default='joint')
args = parser.parse_args()

##data load
img_list = [i.split('C1')[0].rstrip() for i in os.listdir(args.c1)]

#make SIFT point discriptor
sift = cv2.SIFT_create()
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

for img in tqdm.tqdm(img_list):
    c1 = cv2.imread(args.c1+'\\'+img+' C1.tif')
    c2 = cv2.imread(args.c2+'\\'+img+' C2.tif')
    
    #remove bar by inpainting
    c1_bar = np.zeros(c1.shape[:2]).astype(np.uint8)
    c2_bar = np.zeros(c2.shape[:2]).astype(np.uint8)

    c1_bar[:,390:430] = 1
    c2_bar[:,380:420] = 1

    c1 = cv2.inpaint(c1,c1_bar,5,cv2.INPAINT_TELEA) 
    c2 = cv2.inpaint(c2,c2_bar,5,cv2.INPAINT_TELEA) 
   
    #find interesting points
    kp1, des1 = sift.detectAndCompute(c1,None)
    kp2, des2 = sift.detectAndCompute(c2,None)

    kp1_, des1_ = kp_filter(kp1,des1,c1.shape[1] - 30,'>=')
    kp2_, des2_ = kp_filter(kp2,des2,30,'<=')
    
    #match points
    matches = flann.knnMatch(des1_,des2_,k=2)

    good = []
    for m,n in matches:
        if m.distance < n.distance:
            good.append(m)
    print('{0} Points were mathced'.format(len(good)))  

    c1_pts = np.float32([kp1_[m.queryIdx].pt for m in good])
    c2_pts = np.float32([kp2_[m.trainIdx].pt for m in good])
    
    #make transposition matrix T
    T = getTmatrix(c1_pts,c2_pts)
    if len(T) == 0:
        print("{0} dosen't have match points".format(img))
        continue
        
    #wrapping
    merge_img = Image_wrapping(c1,c2,T)
    cv2.imwrite('{0}\\{1}.tif'.format(args.out,img+'_C1C2'),merge_img)
