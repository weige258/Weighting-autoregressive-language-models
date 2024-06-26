import torch.nn

from Model import *

if torch.cuda.is_available():
    device="cuda"
else:
    device="cpu"

def encode(text):
    tensor=torch.tensor([],dtype=torch.long)
    for letter in text:
        try:
            tensor=torch.cat((tensor,torch.tensor([ord(letter)])))
        except:
            continue
    return tensor

def probability(letter_tensor):
    tensor=torch.zeros(dict_size)
    try:
        tensor[letter_tensor]=1
    except:
        pass
    return tensor
try:
    model=torch.load(f="model.pth",map_location=device).to(device)
    print("载入模型")
except:
    model=MainModel().to(device)
    print("新建模型")
loss_func=torch.nn.CrossEntropyLoss().to(device)
optimizer=torch.optim.SGD(model.parameters(),lr=1e-4)

def train(answer,question):
    input=encode(answer).to(device)
    target=input[-1].to(device)
    all_target=encode(question).to(device)
    for next in all_target:
        label=probability(next).to(device)
        output=model(input,target.unsqueeze(0))
        loss=loss_func(output,label)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        target=next

def generation(text):
    output_text=""
    input=encode(text).to(device)
    target=input[-1].to(device)
    for i in range(max_length):
        try:
            output=model(input,target.unsqueeze(0))
            index=int(torch.argmax(output))
            letter=chr(index).encode("utf-8").decode("utf-8")
            output_text+=letter
            target = torch.tensor(index).to(device)
        except:
            continue
    print(output_text)
    return output_text

