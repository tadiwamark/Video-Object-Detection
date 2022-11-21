import streamlit as st
import cv2
import tensorflow as tf 
import numpy as np
from keras.models import load_model
import sys
from streamlit_option_menu import option_menu

#Loading the VGG16 model
model= load_model('model.h5',compile=(False))
st.markdown('<style>body{background-color:Lime;}</style>',unsafe_allow_html=True)



#Function
def predict(frame, model):
    # Pre-process the image for model prediction
    img = cv2.resize(frame, (299, 299))
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)

    img /= 255.0

    # Predict with the VGG16 model
    prediction = model.predict(img)

    # Convert the prediction into text
    pred_text = tf.keras.applications.inception_v3.decode_predictions(prediction, top=1)
    for (i, (imagenetID, label, prob)) in enumerate(pred_text[0]):
        label  = ("{}: {:.2f}%".format(label, prob * 100))

    st.markdown(label)


def predict2(frame, model):
    # Pre-process the image for model prediction
    img = cv2.resize(frame, (299, 299))
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)

    img /= 255.0

    # Predict with the inception model
    prediction = model.predict(img)

    # Convert the prediction into text
    pred_text = tf.keras.applications.vgg16.decode_predictions(prediction, top=1)
    for (i, (imagenetID, label, prob)) in enumerate(pred_text[0]):
        pred_class = label
       

    return pred_class

def object_detection(search_key,frame, model):
    label = predict2(frame,model)
    label = label.lower()
    try:
        if label.find(search_key) > -1:
            sys.exit( st.image(frame, caption=label))
        else:
            st.text("frame not found")
             
             
           

    except:
        print('')
            
            
        

     

# Main App
def main():
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
    st.write(' ')
    
    with col2:
    st.title("Video Object Detection with CNN")
    
    with col3:
    st.write(' ')
    
    st.title("Video Object Detection with CNN")
    st.text("VGG16")

    
    choice = option_menu("Menu",["Home","Upload"],icons = ["house","cloud_upload"],menu_icon ="menu",default_index = 0,orientation = "horizontal")
    
    if choice == "Upload a video":
        st.subheader("Upload Your Short Video")

        video_file_path = st.file_uploader("accepts mp4,avi", type=["mp4", "avi"])

        if video_file_path is not None:
            path = video_file_path.name
            with open(path,mode='wb') as f: 
                f.write(video_file_path.read())         
                st.success("File Uploaded")
            cap = cv2.VideoCapture(path)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))
            
            if st.button("Detect Objects"):
                
                # Start the video prediction loop
                while cap.isOpened():
                    ret, frame = cap.read()
    
                    if not ret:
                        break
    
                    
                    predict(frame, model)
    
                    # Display the resulting frame
                    
                cap.release()
                output.release()
                cv2.destroyAllWindows()
                
            key = st.text_input('Search key')
            key = key.lower()
            
            if key is not None:
            
                if st.button("Search for an object"):
                    
                    
                    # Start the video prediction loop
                    while cap.isOpened():
                        ret, frame = cap.read()
        
                        if not ret:
                            break
        
                        # Perform object detection
                        object_detection(key,frame, model)
                        
                    cap.release()
                    output.release()
                    #cv2.destroyAllWindows()

    elif choice == "Home":
        st.subheader("Detect Objects In Video")
       
    
  
        
       

if __name__ == '__main__':
    main()
