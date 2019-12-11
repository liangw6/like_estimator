import torch 
from torch.utils import data
import torchvision.transforms as tt
from PIL import Image
import os
import random
import pickle

def get_train_test_partition(image_folder, split=8 / 2, seed=None):
    """returns two lists of image index to be used as train and test correspondingly
    
    Arguments:
        image_folder {[str]} -- [the folder where all images are held]
            The method scans through the directory to find partition
    
    Keyword Arguments:
        split {[int]} -- [the train / test split] (default: {8/2})
    """
    if seed is not None:
        random.seed(seed)
    train_portion = split / (split + 1)
    test_portion = 1 - train_portion
    
    n_images = len([i for i in os.listdir(image_folder) if i.endswith(".jpg")])
    n_test_images = round(test_portion * n_images)
    test_indices = set(random.sample(range(n_images), n_test_images))

    train_inx = []
    test_inx = []
    for i in range(n_images):
        if i in test_indices:
            test_inx.append(i)
        else:
            train_inx.append(i)

    # sanity check of calculation
    assert(len(test_inx) == (n_test_images))
    assert(len(train_inx) == (n_images - n_test_images))
    
    return train_inx, test_inx

class PizzaDatabase(data.Dataset):
    """
    Custom dataset with pizza images
    """
    def __init__(self, image_folder, image_ids, view_count_file_name="percentage_views_count.pkl", tt_transform=None, fit_to_size=(800,800)):
        """initialize a pizza database
        
        Arguments:
            image_folder {[string]} -- [directory where images are stored]
                WARNING: images have to have the following file format: image_0.jpg, image_1.jpg, ....
                where image_0.jpg's views counts == view_count[0]
            image_ids {[array of ints]} -- [ids of images to be used for this dataset]
                In other words, ids that is NOT part of this list will NOT be used in this dataset. This allows separating train vs. test
        
        Keyword Arguments:
            view_count_file_name {str} -- [file name for view counts] (default: {"view_count.pkl"})
            tt_transform {torch.transforms} -- transforms applied to each image. If None, will apply a default transform.
            fit_to_size {tuple} -- size that all images are fit. This parameter is only effective when tt_transform is None
        
        Raises:
            ValueError: if number of images in the directory does NOT match number of views / labels in the view_count_file
        """

        # image folder
        self._image_folder = image_folder
        self._image_ids = image_ids
        
        # view counts
        view_count_file_path = os.path.join(image_folder, view_count_file_name)
        with open(view_count_file_path, 'rb') as handle:
            retrieved_views = pickle.load(handle)
        self._views = retrieved_views

        # Sanity check, number of images == number of labels / views
        n_images = len([i for i in os.listdir(image_folder) if i.endswith(".jpg")])
        n_labels = len(self._views)
        if n_images != n_labels:
            raise ValueError("n_images {} but n_labels {}".format(n_images, n_labels))

        # store transforms to be used
        self._tt_transform = tt_transform
        if tt_transform is None:
            # default tt_transform
            self._tt_transform = tt.Compose([
                # pad to desired size with padding_value
                tt.RandomCrop(fit_to_size, pad_if_needed=True, padding_mode='constant'),
                tt.ToTensor(),
            ])

    def __len__(self):
        'Denotes the total number of samples'
        return len(self._image_ids)

    def __getitem__(self, index):
        'Generates one sample of data'

        # the index input argument is only the index into our list of available indices
        # curr_image_index is the one to access image name
        curr_image_index = self._image_ids[index]
        # Select sample
        image_path = os.path.join(self._image_folder, "image_{}.jpg".format(curr_image_index))
        pi = Image.open(image_path)
        ti = self._tt_transform(pi)
      
        # Load data and get label
        X = ti
        y = self._views[curr_image_index]

        return X, y


