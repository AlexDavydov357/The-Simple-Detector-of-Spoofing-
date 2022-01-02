from utils.utils import *
from PIL import Image
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def open_webcam(source, model, threshold, width, height, output_path, model_name):
    labels = ['Spoof', 'Real']
    # Create faces detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # open webcam
    cam = cv2.VideoCapture(source)
    if not cam.isOpened():
        print("Error opening camera")
        exit()
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    count = 0

    while True:
        success, frame = cam.read()
        if success is False:
            print('Не уадется получить кадр')
            break
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
        margin = 5
        for (x, y, w, h) in faces:
            # корректировка области лица
            y1 = int(y - h / (margin - 2.5)) if y - h / margin >= 0 else 0
            x1 = int(x - w / margin) if int(x - w / margin) >= 0 else 0
            x2 = int(x + w + w / margin)
            y2 = int(y + h + h / margin)
            roi = frame[y1:y2, x1:x2]
            if roi.sum() > 0:  # Проверяем на наличие лица в кадре
                title_position = (x, y)
                y_pred = get_predict_webcam(model, roi, width, height, threshold, model_name)
                title = labels[y_pred]
                if y_pred == 1:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cv2.putText(frame, title, title_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2,
                                cv2.LINE_AA)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, title, title_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2,
                                cv2.LINE_AA)

                cv2.imshow('my webcam', frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                name = 'full_frame%02d.jpg' % count
                image.save(output_path + name, quality=100)

            # name = 'frame_%02d.jpg' % count
            # roi.save(output_path + name, quality=100)
        count += 1

        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cam.release()
    cv2.destroyAllWindows()
