import torch.optim as optim
from network import UNet
from data_loader import loaders
from train import my_train
from eval import my_eval
from visualize import my_vis
from app import my_app
import numpy as np
import ray
import sys, os
import torch
fo = open("/teamspace/studios/this_studio/Xray2CT/aritra_project/log.txt","w", encoding="utf-8")
sys.stdout = fo
print("data_loading:")
#data loading
batch_size = 2
loader_tr = loaders(batch_size, 0)
loader_vl = loaders(batch_size, 1)
print(f"loader_tr: {loader_tr}")
print(f"loader_vl: {loader_vl}")
#networks

output = UNet()

output.cuda()

#optimizer

optimizer = optim.Adam(output.parameters(), lr=0.00003, weight_decay=1e-4)

#training



no_of_epochs = 1000
no_of_batches = len(loader_tr)
no_of_batches_1 = len(loader_vl)
best_metric = 0
# Hàm lưu checkpoint
def save_checkpoint(model, optimizer, epoch, loss, filename, best_metric, 
                    metric_values, val_metric_values, loss_values, val_loss_values,
                    metric1_values, val_metric1_values, epoch_values, file_checkpoint):
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss,
        'best_metric': best_metric,
        'metric_values': metric_values,
        'val_metric_values': val_metric_values,
        'loss_values': loss_values,
        'val_loss_values': val_loss_values,
        'metric1_values': metric1_values,
        'val_metric1_values': val_metric1_values,
        'epoch_values': epoch_values
        
    }
    torch.save(checkpoint, filename)
    print(f"Checkpoint saved at epoch {epoch}")

# Hàm load checkpoint
def load_checkpoint(filepath, model, optimizer):
    checkpoint = torch.load(filepath)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_epoch = checkpoint['epoch'] + 1
    best_metric = checkpoint.get('best_metric', 0)
    
    # Lấy các giá trị lưu trữ
    metric_values = checkpoint.get('metric_values', [])
    val_metric_values = checkpoint.get('val_metric_values', [])
    loss_values = checkpoint.get('loss_values', [])
    val_loss_values = checkpoint.get('val_loss_values', [])
    metric1_values = checkpoint.get('metric1_values', [])
    val_metric1_values = checkpoint.get('val_metric1_values', [])
    epoch_values = checkpoint.get('epoch_values', [])

    return start_epoch, best_metric, metric_values, val_metric_values, loss_values, val_loss_values, metric1_values, val_metric1_values, epoch_values

def main():
    
    checkpoint_path = "/teamspace/studios/this_studio/model/checkpoint.pth"
    file_checkpoint ='/teamspace/studios/this_studio/model/checkpoint.pth'
    start_epoch = 0
    best_metric = 0
    metric_values, metric1_values, val_metric_values, val_metric1_values, epoch_values, loss_values, val_loss_values  = ([] for i in range(7))
    
    if os.path.exists(checkpoint_path):
        start_epoch, best_metric, metric_values, val_metric_values, loss_values, val_loss_values, metric1_values, val_metric1_values, epoch_values = load_checkpoint(
            checkpoint_path, output, optimizer
        )
        print(f"Loaded checkpoint from epoch {start_epoch}, best_metric = {best_metric}")
    else:
        print("No checkpoint found. Starting training from scratch.")


    print("Preparing to loop")

    for epoch in range(start_epoch, no_of_epochs):
        print(f"epoch {epoch} starting to my_train")
        epoch_loss, epoch_acc, epoch_acc1 = my_train(output, optimizer, loader_tr, no_of_batches,
                                                    no_of_epochs, epoch)
        print(f"Ending epoch {epoch} of my_train")
        print("Starting to my_eval")
        running_val_loss, running_val_metric, running_val_metric1 = my_eval(output, loader_vl,
                                                                            no_of_batches_1, no_of_epochs, epoch)

        print('epoch', epoch + 1, 'of', no_of_epochs, '-', 'train loss', ':',
            "%.3f" % round((epoch_loss), 3), '-', 'train PSNR(dB)', ':', "%.3f" % round((epoch_acc), 3), '-',
            'train SSIM', ':',
            "%.3f" % round((epoch_acc1), 3), '-', 'val loss', ':', "%.3f" % round((running_val_loss), 3), '-',
            'val PSNR(dB)', ':',
            "%.3f" % round((running_val_metric), 3), '-', 'val SSIM', ':',
            "%.3f" % round((running_val_metric1), 3))
        print("Ending to my_eval")
        metric_values.append(round(epoch_acc, 3))
        val_metric_values.append(round(running_val_metric, 3))

        loss_values.append(round(epoch_loss, 3))
        val_loss_values.append(round(running_val_loss, 3))

        metric1_values.append(round(epoch_acc1, 3))
        val_metric1_values.append(round(running_val_metric1, 3))
        
        current_metric = round(running_val_metric1, 3)

        if(current_metric>best_metric):
            best_metric_coeff = 1
            best_metric = current_metric
        else:
            best_metric_coeff = 0
        epoch_values.append(epoch + 1)
        # save checkpoint
        save_checkpoint(output, optimizer, epoch, epoch_loss, checkpoint_path, best_metric,
                            metric_values, val_metric_values, loss_values, val_loss_values,
                            metric1_values, val_metric1_values, epoch_values, file_checkpoint)
        

        my_vis(epoch_values, loss_values, val_loss_values, metric_values, val_metric_values, metric1_values,
            val_metric1_values, output, best_metric_coeff)

        vmv = np.amax(np.asarray(val_metric_values))
        vm1v = np.amax(np.asarray(val_metric1_values))
        vlv = np.amin(np.asarray(val_loss_values))

        print('Maximum Validation PSNR(dB)', ':', "%.3f" % vmv)
        print('Maximum Validation SSIM', ':', "%.3f" % vm1v)
        print('Minimum Validation Loss', ':', "%.3f" % vlv)

        np.save('/teamspace/studios/this_studio/Xray2CT/aritra_project/my_dataset_results/val_psnr_values.npy', val_metric_values)
        np.save('/teamspace/studios/this_studio/Xray2CT/aritra_project/my_dataset_results/val_ssim_values.npy', val_metric1_values)
        np.save('/teamspace/studios/this_studio/Xray2CT/aritra_project/my_dataset_results/val_loss_values.npy', val_loss_values)

        np.save('/teamspace/studios/this_studio/Xray2CT/aritra_project/my_dataset_results/psnr_values.npy', metric_values)
        np.save('/teamspace/studios/this_studio/Xray2CT/aritra_project/my_dataset_results/ssim_values.npy', metric1_values)
        np.save('/teamspace/studios/this_studio/Xray2CT/aritra_project/my_dataset_results/loss_values.npy', loss_values)


    ray.shutdown()
    print('Finished Training')
    fo.close()
    #app

    my_app()

if __name__ == "__main__":
    main()
