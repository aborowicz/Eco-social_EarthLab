import torch
from torch.autograd import Variable
from torchvision import transforms, models
from utils.dataloaders.data_loader_test import ImageFolderTest
import os
from utils.model_library import *
import torch.nn as nn
import pandas as pd
from PIL import ImageFile
import argparse

parser = argparse.ArgumentParser(description='predict new images using a previously trained model')
parser.add_argument('--training_dir', type=str, help='base directory to search for classification labels')
parser.add_argument('--model_architecture', type=str, help='model architecture, must be a member of models '
                                                           'dictionary')
parser.add_argument('--hyperparameter_set', type=str, help='combination of hyperparameters used, must be a member of '
                                                           'hyperparameters dictionary')
parser.add_argument('--model_name', type=str, help='name of input model file from training, this name will also be used'
                                                   'in subsequent steps of the pipeline')
parser.add_argument('--data_dir', type=str, help='directory with images to be classified')


args = parser.parse_args()

# check for invalid inputs
if args.model_architecture not in model_archs:
    raise Exception("Unsupported architecture")

if args.training_dir not in training_sets:
    raise Exception("Invalid training set")


ImageFile.LOAD_TRUNCATED_IMAGES = True

# normalize input images
arch_input_size = model_archs[args.model_architecture]['input_size']
data_transforms = transforms.Compose([
        transforms.CenterCrop(arch_input_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# create dataloader instance
dataset = ImageFolderTest(args.data_dir, data_transforms)
batch_size = hyperparameters[args.hyperparameter_set]['batch_size_test']
num_workers = hyperparameters[args.hyperparameter_set]['num_workers_val']
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, num_workers=num_workers)


img_exts = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm']
class_names = sorted([subdir for subdir in os.listdir('./training_sets/{}/training'.format(args.training_dir))])
data_dir = args.data_dir

use_gpu = torch.cuda.is_available()

# create an image catalog to keep track of labels
classified = pd.DataFrame()

# add images to the catalog
idx = 0
for path, _, files in os.walk(data_dir):
    for filename in files:
        # extract x and y from filename and run affine transformation
        filename_lower = filename.lower()
        if not (any(filename_lower.endswith(ext) for ext in img_exts)):
            print('{} is not a valid image file.'.format(filename))
            continue

        row = {'label': None, 'file': filename}
        classified = classified.append(row, ignore_index=True)
        idx += 1


# classify images with CNN
def main():
    # create model instance
    num_classes = training_sets[args.training_dir]['num_classes']

    # loading the pretrained model and adding new classes to it
    if args.model_architecture == "Resnet18":
        model_ft = models.resnet18(num_classes=num_classes)

    elif args.model_architecture == "Resnet34":
        model_ft = models.resnet34(num_classes=num_classes)

    elif args.model_architecture == "Resnet50":
        model_ft = models.resnet50(num_classes=num_classes)

    elif args.model_architecture == "Squeezenet11":
        model_ft = models.squeezenet1_1(num_classes=num_classes)

    elif args.model_architecture == "Densenet121":
        model_ft = models.densenet121(num_classes=num_classes)

    elif args.model_architecture == "Densenet169":
        model_ft = models.densenet169(num_classes=num_classes)

    elif args.model_architecture == "Alexnet":
        model_ft = models.alexnet(num_classes=num_classes)

    else:
        model_ft = models.vgg16_bn(num_classes=num_classes)

    # check for GPU support and set model to evaluation mode
    use_gpu = torch.cuda.is_available()
    if use_gpu:
        model_ft.cuda()
    model_ft.eval()

    # load saved model weights from pt_train.py
    model_ft.load_state_dict(torch.load("./saved_models/{}/{}.tar".format(args.model_name, args.model_name)))

    # classify images in dataloader
    for data in dataloader:
        # get the inputs
        inputs, _, file_names = data

        # wrap them in Variable
        if use_gpu:
            inputs = Variable(inputs.cuda())
        else:
            inputs = Variable(inputs)

        # do a forward pass to get predictions
        outputs = model_ft(inputs)
        _, preds = torch.max(outputs.data, 1)
        for idx, label in enumerate([int(ele) for ele in preds]):
            classified.loc[classified['file'] == file_names[idx], 'label'] = class_names[label]

        classified.to_csv('./classified_images/classified.csv', index=False)


if __name__ == '__main__':
    main()
