import torch
from torch.utils.data import Dataset, DataLoader
import h5py
import os
import numpy as np


class OxfordPetDataset(Dataset):

    def __init__(self, config, split, mini_batch_size):
        root = "datasets/data_new/"
        root = root + split
        # Need to add option later for more flexibility
        self.split = split
        img_path = r'images.h5'
        mask_path = r'masks.h5'
        bbox_path = r'bboxes.h5'
        bin_path = r'binary.h5'

        self.image_dir = os.path.join(root, img_path)
        self.seg_dir = os.path.join(root, mask_path)
        self.bbox_dir = os.path.join(root, bbox_path)
        self.bin_dir = os.path.join(root, bin_path)

        self.seg_task= "Segmen" in config["Tasks"].keys()
        self.bb_task= "BB" in config["Tasks"].keys()
        self.bin_task= "Class" in config["Tasks"].keys()
        

        self.num_minibatches = self.__len__() // mini_batch_size
        #self.indices_split = np.split(np.random.shuffle(np.linspace\
            #(0, self.__len__(),self.__len__() )),self.num_minibatches)
        self.indices = np.arange(0, self.__len__() )
        np.random.shuffle(self.indices)
        self.indices_split = np.array_split(self.indices,self.num_minibatches)
        self.test =1




    def __getitem__(self,index):
        sample = {}

        _img = self._load_data(index,self.image_dir)
        sample['image'] = torch.from_numpy(_img).float()

        if self.seg_task:
            _seg = self._load_data(index,self.seg_dir)
            sample['Segmen'] = torch.from_numpy(_seg).float()

        if self.bb_task:
            _bb = self._load_data(index,self.bbox_dir)
            sample['BB'] = torch.from_numpy(_bb).float()
            #sample['bb'] = _bb 

        if self.bin_task:
            _bin = self._load_data(index,self.bin_dir)
            sample['Class'] = torch.from_numpy(_bin).float()
            # sample['bin'] = _bin 

        return sample  

    def __len__(self):

        if self.split == "train":
            return 2210
        if self.split == "val":
            return 700
        if self.split == "test":
            return 700   

    def _load_data(self,index,dir):
        with  h5py.File(dir , 'r') as file:
            key = list(file.keys())[0]
            elems = file[key][ index]
            return  elems

    def _load_segmen_random(self):
        return 1


    def _get_num_minibatch(self):
        return self.num_minibatches

    def _getindices_(self,index):
    
        return self.indices_split[index]

    
#### UTIL FUNCTS #########

def get_dataset(config,split):
    # TODO why? can't we just use the dset directly??

    dataset = OxfordPetDataset(config,split,32)
    # TODO why is batchsize fixed?
    return dataset
    #return 1

def get_dataloader(dataset, batch_size):

    dataloader = DataLoader(dataset, batch_size, shuffle=True)
    return dataloader
    #return 1

def _get_data(dataset,index):

    indices = np.sort(dataset._getindices_(index))
    return dataset.__getitem__(indices)

