# modified u-net without pooling
#import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv3D, concatenate, add, Multiply, BatchNormalization, Activation, \
                         MaxPooling3D, UpSampling3D, ELU
                         
def conv3d_bn_relu(inputs, filter_num, bn_flag=False):
    
    if bn_flag:
        conv = Conv3D(filter_num, (3,3,3), padding='same', kernel_initializer='he_normal')(inputs)
        conv = BatchNormalization()(conv)
        conv = Activation('relu')(conv)        
    else:
        conv = Conv3D(filter_num, (3,3,3), padding='same', 
                      activation='relu', 
                      kernel_initializer='he_normal')(inputs)
    return conv

def dnsurfer_3d_model(num_ch, output_ch, filter_num=64, kinit_type='he_normal'):
    
    inputs = Input((None, None, None, num_ch)) 
    loss_weights = Input((None, None, None, 1))
    
    p0 = inputs
    
    conv1 = conv3d_bn_relu(p0, filter_num)
    conv2 = conv3d_bn_relu(conv1, filter_num, bn_flag=True)
    conv3 = conv3d_bn_relu(conv2, filter_num, bn_flag=True)
    conv4 = conv3d_bn_relu(conv3, filter_num, bn_flag=True)
    conv5 = conv3d_bn_relu(conv4, filter_num, bn_flag=True)
    conv6 = conv3d_bn_relu(conv5, filter_num, bn_flag=True)
    conv7 = conv3d_bn_relu(conv6, filter_num, bn_flag=True)
    conv8 = conv3d_bn_relu(conv7, filter_num, bn_flag=True)
    conv9 = conv3d_bn_relu(conv8, filter_num, bn_flag=True)
    conv10 = conv3d_bn_relu(conv9, filter_num, bn_flag=True)
    conv11 = conv3d_bn_relu(conv10, filter_num, bn_flag=True)
    conv12 = conv3d_bn_relu(conv11, filter_num, bn_flag=True)
    conv13 = conv3d_bn_relu(conv12, filter_num, bn_flag=True)
    conv14 = conv3d_bn_relu(conv13, filter_num, bn_flag=True)
    conv15 = conv3d_bn_relu(conv14, filter_num, bn_flag=True)
    conv16 = conv3d_bn_relu(conv15, filter_num, bn_flag=True)
    conv17 = conv3d_bn_relu(conv16, filter_num, bn_flag=True)
    conv18 = conv3d_bn_relu(conv17, filter_num, bn_flag=True)
    conv19 = conv3d_bn_relu(conv18, filter_num, bn_flag=True)
    residual = Conv3D(output_ch, (3,3,3), padding='same', kernel_initializer='he_normal')(conv19)
    
    conv = concatenate([residual, loss_weights],axis=-1)
        
    model = Model(inputs=[inputs, loss_weights], outputs=conv)  
    
    return model