from subprocess import call, Popen
import os
#interface to the program neurlaStyle
class neuralStyle:
    def __init__(self):
        #self.dir = "~/workspace/CNNMRF/"
        self.dir = "/home/cgel/workspace/CNNMRF/"
        self.content_dir = self.dir + "data/content/"
        self.result_dir = self.dir + "data/result/trans/MRF/"
        # call the full path so that it works when the program is called with sudo
        self.qlua_path = "/home/cgel/torch/install/bin/qlua"

    def generate(self, style_number, content_name):
        # copy the content image to the necessary place
        copy_command = "cp " + content_name + " " + self.content_dir+"content.jpg"
        call(copy_command, shell=True)


        style_name = str(style_number)
        generate_command = self.qlua_path + " " + self.dir + "cnnmrf.lua "  + "-style_name " + style_name+ " -content_name content " + ""
        Popen(generate_command, shell=True, cwd=self.dir).wait()

        # copy back the result
        generated_list = os.listdir("generated")
        int_generated_list = [int(r.split(".")[0]) for r in generated_list] + [0]
        current_generated = max(int_generated_list) + 1
        result_name = "generated/"+str(current_generated)+".jpg"
        copy_back_command = "cp " + self.result_dir+"res_3_100.jpg " + result_name
        call(copy_back_command, shell=True)
        # resize the image
        resize_command = "convert -resize 1080x1350 " + result_name + " " + result_name
        call(resize_command, shell=True)

        copy_content_command = "cp " + content_name + " contents/"+str(current_generated)+".jpg"
        call(copy_content_command, shell=True)
