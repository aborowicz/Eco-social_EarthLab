# Script to store model architectures and hyperparameter combinations


# architecture definitions with input size and whether the model is used at the haulout level or single seal level
model_archs = {'Resnet18': {'input_size': 224},
               'Resnet34': {'input_size': 224},
               'Resnet50': {'input_size': 224},
               'Squeezenet11': {'input_size': 224},
               'Densenet121': {'input_size': 224},
               'Densenet169': {'input_size': 224},
               'Alexnet': {'input_size': 224},
               'VGG16': {'input_size': 224}
               }


# training sets with number of classes and size of scale bands
training_sets = {'training_set_13_MAY_18': {'num_classes': 9}}


# hyperparameter sets
hyperparameters = {'A': {'learning_rate': 1E-3, 'batch_size_train': 64, 'batch_size_val': 8, 'batch_size_test': 64,
                         'step_size': 1, 'gamma': 0.95, 'epochs': 5, 'num_workers_train': 8, 'num_workers_val': 1},
                   'B': {'learning_rate': 1E-3, 'batch_size_train': 16, 'batch_size_val': 1, 'batch_size_test': 8,
                         'step_size': 1, 'gamma': 0.95, 'epochs': 5, 'num_workers_train': 4, 'num_workers_val': 1},
                   'C': {'learning_rate': 1E-3, 'batch_size_train': 64, 'batch_size_val': 8, 'batch_size_test': 64,
                         'step_size': 1, 'gamma': 0.95, 'epochs': 30, 'num_workers_train': 16, 'num_workers_val': 8},
                   'D': {'learning_rate': 1E-3, 'batch_size_train': 32, 'batch_size_val': 16, 'batch_size_test': 16,
                         'step_size': 1, 'gamma': 0.95, 'epochs': 20, 'num_workers_train': 16, 'num_workers_val': 16},
                   'E': {'learning_rate': 1E-3, 'batch_size_train': 16, 'batch_size_val': 1, 'batch_size_test': 8,
                         'step_size': 1, 'gamma': 0.95, 'epochs': 2, 'num_workers_train': 8, 'num_workers_val': 1}
                   }





