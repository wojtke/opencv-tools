### Simple OpenCV tools
Simple tools I use to make my life easier when working with OpenCV. 

Not very pythonic:
```
cap = cv.VideoCapture(0)
if not cap.isOpened():
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
```

I like this better:
```
with VideoPreview() as vid:
    for frame in Capture(0):
        vid.show(frame)
```

Maybe not everything is explicit, however it's a lot easier to read. 

Likely I'm gonna add more stuff in the future.

