# Again we have run this file on colab and not as a standalone file like we have added here.

import os
from options.test_options import TestOptions
from data.data_loader import CreateDataLoader
from models.models import create_model
from util.visualizer import Visualizer
from IPython.display import HTML
from base64 import b64encode
from google.colab import files

opt = TestOptions().parse(save=False)
opt.display_id = 0
opt.nThreads = 1
opt.batchSize = 1
opt.serial_batches = True
opt.no_flip = True
opt.in_the_wild = True
opt.traverse = True
opt.interp_step = 0.05

data_loader = CreateDataLoader(opt)
dataset = data_loader.load_data()
visualizer = Visualizer(opt)

opt.name = 'males_model'
model = create_model(opt)
model.eval()


uploaded = files.upload()
for filename in uploaded.keys():
  img_path = filename
  print('User uploaded file "{name}"'.format(name=filename))

data = dataset.dataset.get_item_from_path(img_path)
visuals = model.inference(data)

os.makedirs('results', exist_ok=True)
out_path = os.path.join('results', os.path.splitext(img_path)[0].replace(' ', '_') + '.mp4')
visualizer.make_video(visuals, out_path)

use_webm = False

webm_out_path

video_path = webm_out_path if use_webm else out_path
video_type = "video/webm" if use_webm else "video/mp4"
mp4 = open(video_path,'rb').read()
data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
HTML("""""".format(opt.fineSize, data_url, video_type))

files.download(out_path)
