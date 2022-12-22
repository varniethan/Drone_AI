import time
import csv
import threading
import airsim
import tkinter
import os

DATA_RECORD_INTERVAL = 5
INPUT_CHANGE_WAIT = 0.5

client = airsim.MultirotorClient()
client.confirmConnection()


folderPath = "./"+input("Enter new folder name")
imagesFolderPath = folderPath+"/images"
os.mkdir(folderPath)
os.mkdir(imagesFolderPath)


#wait a bit before starting the recording
time.sleep(5)

#create UI for stop button
StopButtonRoot = tkinter.Tk()

isStillRecording = True
def stopRecording():
    global isStillRecording
    isStillRecording = False
    StopButtonRoot.destroy()
    
stopButton = tkinter.Button(StopButtonRoot, text="Stop Recording Data", command=stopRecording)
stopButton.pack()

#Open file
def startRecording():
    global isStillRecording
    with open(folderPath+"/dataset.csv", "w", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "front_image",
            "right_image",
            "left_image",
            "bottom_image",
            "initial_throttle",
            "throttle_change",
            "yaw_change"
        ])

        entryNo = 0
        
        while isStillRecording:

            entryNo += 1
            time.sleep(DATA_RECORD_INTERVAL)
            if not isStillRecording:
                break

            #get images
            imageResponses = client.simGetImages([
                airsim.ImageRequest("front_center", airsim.ImageType.Scene),
                airsim.ImageRequest("front_right", airsim.ImageType.Scene),
                airsim.ImageRequest("front_left", airsim.ImageType.Scene),
                airsim.ImageRequest("bottom_center", airsim.ImageType.Scene)
            ])

            airsim.write_file(os.path.normpath(imagesFolderPath+"/front_"+str(entryNo)+".png"), imageResponses[0].image_data_uint8)
            airsim.write_file(os.path.normpath(imagesFolderPath+"/right_"+str(entryNo)+".png"), imageResponses[1].image_data_uint8)
            airsim.write_file(os.path.normpath(imagesFolderPath+"/left_"+str(entryNo)+".png"), imageResponses[2].image_data_uint8)
            airsim.write_file(os.path.normpath(imagesFolderPath+"/bottom_"+str(entryNo)+".png"), imageResponses[3].image_data_uint8)

            #record other data
            rotorState = client.getMultirotorState()
            initialThrottle = rotorState.rc_data.throttle
            initialYaw = rotorState.rc_data.yaw

            time.sleep(INPUT_CHANGE_WAIT) #get how much changes by waiting a bit

            rotorState = client.getMultirotorState()
            throttleChange = rotorState.rc_data.throttle - initialThrottle
            yawChange = rotorState.rc_data.yaw - initialYaw

            #write to csv
            writer.writerow([
                imagesFolderPath+"/front_"+str(entryNo)+".png",
                imagesFolderPath+"/right_"+str(entryNo)+".png",
                imagesFolderPath+"/left_"+str(entryNo)+".png",
                imagesFolderPath+"/bottom_"+str(entryNo)+".png",
                initialThrottle,
                throttleChange,
                yawChange
            ])

            print("Written entry "+str(entryNo)+" to csv file")


#Start recording thread and tkinter main loop
buttonThread = threading.Thread(target=startRecording)
buttonThread.start()     
StopButtonRoot.mainloop()

print("Ended recording data")
