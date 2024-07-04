
# ImageDehazing2(server)

Utilizing Pix2Pix, a conditional generative adversarial network (GAN), to create an API for dehazing images involves training the model on hazy-clear image pairs. The API receives hazy images, processes them through the trained Pix2Pix model, and outputs dehazed versions, enhancing visibility and clarity.

# Setup Instruction

**1. Clone Repository:**

- ```git clone https://github.com/Viper910/ImageDehazingV2.git```
- ``` cd ImageDehazingV2 ```
- ``` cd server ```

**2. Create Virtual Environment:**

- ``` python -m venv venv ```
- ``` .\venv\Scripts\activate ``` this for windows 
- ``` source venv/bin/activate ``` this for mac/linux
- If you get any error while running the activate script then you can try 
- ```Set-ExecutionPolicy Unrestricted -Scope Process```
- Hit **Y** and enter


**3. Install Dependencies:**

- ``` python -m pip install -r .\requirement.txt ```

**4. Steps to train model:**

- Download the dataset https://www.kaggle.com/datasets/mohit3430/haze1k.
- Modify the directory structure of Dataset .
- Just copy the data present inside train folder dataset folder.
- The path must look like :-
  - dataset
    - input
    - target
    - test_thick
    - test_thin
    - test_moderate
- Run get inside architecture folder ```cd architecture```.
- run the train command ```python train.py```.
- After the training is over the generator model will be stored inside generator_model folder.

**5. Run Python Server:**
- Before running the python server create a folder inside static folder with name ```uploads``` (all the uploaded images will be stored here).
- ``` python server.py ```
- ```/upload``` post method to upload image 
- ```/generate/<image-id>``` get method to generate image 
- ```/static/<image-id>``` get method to get dehaze image 



