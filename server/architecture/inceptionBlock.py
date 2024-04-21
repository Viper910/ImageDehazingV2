from tensorflow.keras import Model, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers

class InceptionBlock(layers.Layer):
    def __init__(self, f, pooling=True):
        super(InceptionBlock, self).__init__()
        
        self.f = f
        self.pooling = pooling
    
        '''===PATH1==='''
        self.conva0 = layers.Conv2D(self.f, (1, 1), activation='relu', padding='same')                     
        self.batch_norma0 = layers.BatchNormalization()
        self.conva1 = layers.Conv2D(self.f, (3, 3), activation='relu', padding='same')
        self.batch_norma1 = layers.BatchNormalization()
        self.conva2 = layers.Conv2D(self.f, (1, 3), activation='relu', padding='same')
        self.batch_norma2 = layers.BatchNormalization()
        self.poola = layers.MaxPooling2D(pool_size=(2, 2))
        self.conva3 = layers.Conv2D(self.f, (3, 1), activation='relu', padding='same')
        self.batch_norma3 = layers.BatchNormalization()
        self.concat1 = layers.Concatenate(axis=-1)
        self.poola = layers.MaxPooling2D(pool_size=(2, 2))
        
        '''===PATH2==='''
        self.convb0 = layers.Conv2D(self.f, (1, 1), activation = 'relu', padding = 'same')
        self.batch_normb0 = layers.BatchNormalization()
        self.convb1 = layers.Conv2D(self.f, (1, 3), activation='relu', padding='same')
        self.batch_normb1 = layers.BatchNormalization()
        self.convb2 = layers.Conv2D(self.f, (3, 1), activation='relu', padding='same')
        self.batch_normb2 = layers.BatchNormalization()
        self.poolb = layers.MaxPooling2D(pool_size=(2, 2))
        self.concat2 = layers.Concatenate(axis=-1)
        
        '''===PATH3==='''
        self.ppoolc = layers.MaxPooling2D(pool_size=(3,3), strides=(1, 1), padding='same')
        self.convc0 = layers.Conv2D(self.f, (1, 1), activation='relu', padding='same')
        self.batch_normc0 = layers.BatchNormalization()
        self.poolc = layers.MaxPooling2D(pool_size=(2, 2))
        
        '''===PATH4==='''
        self.convd1 = layers.Conv2D(self.f, (1, 1), activation='relu', padding='same')
        self.batch_normd1 = layers.BatchNormalization()
        self.poold = layers.MaxPooling2D(pool_size=(2, 2))
        self.concat = layers.Concatenate(axis=-1)
    
    def call(self, inputs, training=False):
        conva = self.conva0(inputs) #1x1
        conva = self.batch_norma0(conva, training=training)
        conva = self.conva1(conva)  #3x3
        conva = self.batch_norma1(conva, training=training)
        conva_con1 = self.conva2(conva) # 1x3
        conva_con1 = self.batch_norma2(conva_con1, training=training)
        conva_con2 = self.conva3(conva) # 3x1
        conva_con2 = self.batch_norma3(conva_con2, training=training)
        conva = self.concat1([conva_con1, conva_con2])
        if self.pooling:
            conva = self.poola(conva)
            
        convb = self.convb0(inputs) # 1x1
        convb = self.batch_normb0(convb, training=training)
        convb_con1 = self.convb1(convb) # 1x3
        convb_con1 = self.batch_normb1(convb_con1, training=training)
        convb_con2 = self.convb2(convb) # 3x1
        convb_con2 = self.batch_normb2(convb_con2, training=training)
        convb = self.concat([convb_con1, convb_con2])
        if self.pooling:
            convb = self.poolb(convb)
            
        convc = self.ppoolc(inputs)
        convc = self.convc0(convc)
        convc = self.batch_normc0(convc, training=training)
        if self.pooling:
            convc = self.poolc(convc)
            
        convd = self.convd1(inputs)
        convd = self.batch_normd1(convd, training=training)
        if self.pooling:
            convd = self.poold(convd)
            
        up = self.concat([conva, convb, convc, convd])
        return up