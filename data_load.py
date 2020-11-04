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



def Image_wrapping(c1,c2,T):

    w = c2.shape[1] + T[0]
    h = max(c1.shape[0],c2.shape[0] + T[1])

    merge_img = np.zeros((h,w,3))
    merge_img[:c1.shape[0],:c1.shape[1],:] = c1
    
    for x in range(c2.shape[1]):
        for y in range(c2.shape[0]):
            
            x_ = x + T[0]
            y_ = y + T[1]
            
            if y_ >= 0:
                merge_img[y_,x_,:] = c2[y,x,:]
    
    padding = np.where((merge_img[:,:,0] == 0) & (merge_img[:,:,1] == 0) & (merge_img[:,:,2] == 0))
    merge_img[padding] = [64,29,26]

    return merge_img.astype(np.uint8)


def getTmatrix(target,point,thr=1):

    t = target - point

    max_inline = [0,0]
    best_diff = [999999,999999]
    best_tar = []
    best_pt=[[],[]]
    best_tar=[[],[]]
    for tx, ty in t:

        inline = [0,0]
        inline_pt = [[],[]]
        inline_tar = [[],[]]
         
        for (x_, y_), (x, y) in zip(point,target):
                
            if abs(tx) < 750:
                pass        
            
            elif abs(x_+tx - x) <= thr:
                                   
                inline[0] += 1
                inline_pt[0].append([x_,y_])
                inline_tar[0].append([x,y])
                
            if abs(ty) >= 5:
                pass
                
            elif abs(y_+ty - y) <= thr:
            
                inline[1] += 1
                inline_pt[1].append([x_,y_])
                inline_tar[1].append([x,y])

        if inline[0] == max_inline[0]:
            if abs(tx) > best_diff[0]:
                best_pt[0] = inline_pt[0]
                best_tar[0] = inline_tar[0]
                max_inline[0] = inline[0]
                best_diff[0] = abs(tx)

        elif inline[0] > max_inline[0]:
            best_pt[0] = inline_pt[0]
            best_tar[0] = inline_tar[0]
            max_inline[0] = inline[0]
            best_diff[0] = abs(tx)

        if inline[1] == max_inline[1]:
            if abs(ty) < best_diff[1]:
                best_pt[1] = inline_pt[1]
                best_tar[1] = inline_tar[1]
                max_inline[1] = inline[1]
                best_diff[1] = abs(ty)

        elif inline[1] > max_inline[1]:
            best_pt[1] = inline_pt[1]
            best_tar[1] = inline_tar[1]
            max_inline[1] = inline[1]
            best_diff[1] = abs(ty)
 
    print('{0},{1} Points were included in inline set'.format(max_inline[0],max_inline[1]))  
    if len(best_tar[0]) == 0 or len(best_tar[1]) == 0:
        return []

    best_tx = np.mean((np.array(best_tar[0]) - np.array(best_pt[0]))[:,0])
    best_ty = np.mean((np.array(best_tar[1]) - np.array(best_pt[1]))[:,1])
    return np.array([best_tx,best_ty]).round().astype(np.int)
