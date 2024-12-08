from torch.utils.tensorboard import SummaryWriter
writer=SummaryWriter('runs')
for i in range(8):
    writer.add_scalar('train',i,i)
writer.close()