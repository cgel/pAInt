from subprocess import call, Popen
import os
#interface to the program neurlaStyle
class neuralStyle:
    def __init__(self):
        #self.dir = "~/workspace/CNNMRF/"
        self.dir = "/home/cgel/workspace/CNNMRF/"
        self.content_dir = self.dir + "data/content/"
        self.result_dir = self.dir + "data/result/trans/MRF/"

    def generate(self, style_number, content_name):
        # copy the content image to the necessary place
        copy_command = "cp " + content_name + " " + self.content_dir+"content.jpg"
        call(copy_command, shell=True)


        style_name = str(style_number)
        generate_command = "qlua " + self.dir + "cnnmrf.lua "  + "-style_name " + style_name+ " -content_name content " + ""
        print(generate_command)
        #Popen(generate_command, shell=True, cwd=self.dir).wait()

        # copy back the result
        generated_list = os.listdir("generated")
        int_generated_list = [int(r.split(".")[0]) for r in generated_list] + [0]
        current_generated = max(int_generated_list) + 1
        print(current_generated)
        copy_back_command = "cp " + self.result_dir+"res_3_100.jpg " + "generated/"+str(current_generated)+".jpg"
        print(copy_back_command)
        #call(["cp", self.result_dir+"res_3_100.jpg", content_dir ])
        copy_content_command = "cp " + content_name + "contents/"+str(current_generated)+".jpg"
