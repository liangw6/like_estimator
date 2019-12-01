import torch 
from torch.utils import data
import os
from PIL import Image
import torchvision.transforms as tt

class PizzaDatabase(data.datset):
    """
    Custom dataset with pizza images
    """
    def __init__(self, image_folder, view_count_file_name="view_count.pkl", tt_transform=None, fit_to_size=(800,800)):
        """initialize a pizza database
        
        Arguments:
            image_folder {[string]} -- [directory where images are stored]
            WARNING: images have to have the following file format: image_0.jpg, image_1.jpg, ....
            where image_0.jpg's views counts == view_count[0]
        
        Keyword Arguments:
            view_count_file_name {str} -- [file name for view counts] (default: {"view_count.pkl"})
            tt_transform {torch.transforms} -- transforms applied to each image. If None, will apply a default transform.
            fit_to_size {tuple} -- size that all images are fit. This parameter is only effective when tt_transform is None
        
        Raises:
            ValueError: if number of images in the directory does NOT match number of views / labels in the view_count_file
        """
        if tt_transform is None:
            # default tt_transform
            self._tt_transform = tt.Compose([
                # pad to desired size with padding_value
                tt.RandomCrop(fit_to_size, pad_if_needed=True, padding_mode='constant'),
                tt.ToTensor(),
            ])

        # image folder
        self._image_folder = image_folder
        
        # view counts
        view_count_file_path = os.path.join(image_folder, view_count_file_name)
        with open(view_count_file_path, 'rb') as handle:
            retrieved_views = pickle.load(handle)
        self._views = retrieved_views

        # Sanity check, number of images == number of labels / views
        n_images = os.listdir(image_folder)
        n_labels = len(self._views)
        if n_images != n_labels:
            raise ValueError("n_images {} but n_labels {}".format(n_images, n_labels))

  def __len__(self):
        'Denotes the total number of samples'
        return len(self._views)

  def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample
        image_path = os.path.join(self._image_folder, "image_{}.jpg".format(index))
        pi = Image.open(image_path)
        ti = scale_transforms(pi)
      
        # Load data and get label
        X = ti
        y = self._views[index]

        return X, y