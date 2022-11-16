import airsim
import os

client = airsim.MultirotorClient()
client.confirmConnection()

inp = ""
while inp != "end":
    responses = client.simGetImages(
        [airsim.ImageRequest("0", airsim.ImageType.Scene)]
        )
    for response in responses:
        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            airsim.write_pfm(os.path.normpath('./temp/py1.pfm'), airsim.get_pfm_array(response))
        else:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath('./temp/py1.png'), response.image_data_uint8)



    inp = input("--> ")
