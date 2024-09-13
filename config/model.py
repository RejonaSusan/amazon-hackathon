import yolov5

model = yolov5.load('yolov5s.pt')

results = model('/Users/rejonasusan/Desktop/student_resource 3/dataset/imgs/1yw53vfQtS.jpg')

boxes = results.xyxy[0].numpy()  

print(boxes)