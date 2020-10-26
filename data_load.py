import numpy as np
import cv2 

def kp_filter(kp,des,thr,direct):
    kp_ = []
    des_ = []
    
    for i in range(len(kp)):
        if direct == '>=':
            include = (kp[i].pt[0] >= thr)
        elif direct == '<=':
            include = (kp[i].pt[0] <= thr)
        else:
            print('Wrong dicrection')
            return
            
        if include:

            kp_.append(kp[i])
          
            if len(des_) == 0:
                des_ = des[i].reshape((1,des.shape[1]))           
            else:
                des_ = np.concatenate([des_,des[i].reshape((1,des.shape[1]))],axis=0)
          
    return kp_,des_

def getTmatrix(target,point,thr=1):
    
    t = target - point
    
    max_inline = 0
    for tx, ty in t:
        if abs(ty) >= 10:
            continue 

        inline = 0
        inline_pt = []
        inline_tar = []
        
        for (x_, y_), (x, y) in zip(point,target):
                                                            
            if abs(x_+tx - x) <= thr and abs(y_+ty - y) <= thr:
                                    
                inline += 1
                inline_pt.append([x_,y_])
                inline_tar.append([x,y])
                                    
        if inline > max_inline:
            best = (tx,ty)
            best_pt = inline_pt
            best_tar = inline_tar
            max_inline = inline
    
    print('{0} Points were included in inline set'.format(max_inline))
    
    return(np.mean(np.array(best_tar) - np.array(best_pt),axis=0).round().astype(np.int))

def Image_wrapping(c1,c2,T):

    w = c2.shape[1] + T[0]
    h = max(c1.shape[0],c2.shape[0] + T[1])

    merge_img = np.zeros((h,w,3))
    merge_img[:c1.shape[0],:c1.shape[1],:] = c1
    
    for x in range(c2.shape[1]):
        for y in range(c2.shape[0]):
            
            x_ = x + T[0]
            y_ = y + T[1]
            
            merge_img[y_,x_,:] = c2[y,x,:]
    
    padding = np.where((merge_img[:,:,0] == 0) & (merge_img[:,:,1] == 0) & (merge_img[:,:,2] == 0))
    merge_img[padding] = [64,29,26]

    return merge_img.astype(np.uint8)