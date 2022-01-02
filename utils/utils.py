import albumentations as A
import cv2
import matplotlib.pyplot as plt
import numpy as np
from random import shuffle
from pathlib import Path
from sklearn.metrics import auc

IMG_FORMATS = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']


# рассчет гистограммы
def calc_hist(img):
    histogram = [0] * 3
    for j in range(3):
        histr = cv2.calcHist([img], [j], None, [256], [0, 256])
        histr *= 255.0 / histr.max()
        histogram[j] = histr
    return np.array(histogram)


# preprocessing images
def image_spacer_file(file_path, width, height, augmentation=False):
    """ The function takes as inputs path to image, working width and height, as well as augmentation mode.
    The function create image copies in few colors spaces then augment data calculating difference between them. After
    that calculating them histogram. Returning а vector of  length depending of setupping image size, as well as
    current class label of the form 1 - real, 0 - spoof (fake)
       args:
       file_path (str): path to image files (should include class name)
       width, height (int): - working size of image to feed in model
       augmentation (bool): working mode, can be True/False. Used only during training model.
       return:
       hist_vector
       y_true
    """
    # target images
    dsize = (width, height)
    img = cv2.imread(file_path)

    # Создаем y_true 'real' - 1, 'spoof' - 0
    y_true = []
    class_face = file_path.split('/')[-1].split('\\')[1]
    y_true.append(1.) if class_face == 'real' else y_true.append(0.)

    if augmentation:
        # трансформация изображения
        transforms = A.Compose([A.HorizontalFlip(p=0.5),  # горизонтально отражение с вероятностью 50%
                                A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.20, rotate_limit=20, p=0.4),
                                # поворот изображения с вероятностью 75%
                                A.Affine(scale=1.25, p=0.4),  # Увеличение на 25% с вероятностью 50%
                                ])
        img = transforms(image=img)['image']  # добавляем аугментацию
        img = cv2.resize(img, dsize, interpolation=cv2.INTER_NEAREST)
    else:
        img = cv2.resize(img, dsize, interpolation=cv2.INTER_NEAREST)

    img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    img_luv = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    aaa = img_ycrcb - img_luv
    bbb = img_hsv - img_ycrcb
    ccc = img_hsv - img_luv

    bgr_hist = calc_hist(img).ravel()
    ycrcb_hist = calc_hist(img_ycrcb).ravel()
    luv_hist = calc_hist(img_luv).ravel()
    ycrcb_lab = calc_hist(img_lab).ravel()
    luv_hsv = calc_hist(img_hsv).ravel()
    aaa_d = calc_hist(aaa).ravel()
    bbb_d = calc_hist(bbb).ravel()
    ccc_d = calc_hist(ccc).ravel()

    hist_vector = np.concatenate([bgr_hist, ycrcb_hist, luv_hist, ycrcb_lab, luv_hsv, aaa_d, bbb_d, ccc_d])

    return hist_vector, np.array(y_true)


def create_data_generator(file_list, batch_size, width, height):
    shuffle(file_list)
    while True:
        for i in range(0, len(file_list), batch_size):
            img_hist = []
            labels = []
            curr_list = file_list[i:i + batch_size]
            for file in curr_list:
                x_train, y_true = image_spacer_file(file, width, height, augmentation=True)
                img_hist.append(x_train)
                labels.append(y_true)
            yield np.array(img_hist), np.array(labels)


# preprocessing images for webcam
def image_spacer_webcam(img, width, height):
    # target images
    dsize = (width, height)
    img = cv2.resize(img, dsize, interpolation=cv2.INTER_NEAREST)

    img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    img_luv = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    aaa = img_ycrcb - img_luv
    bbb = img_hsv - img_ycrcb
    ccc = img_hsv - img_luv

    bgr_hist = calc_hist(img).ravel()
    ycrcb_hist = calc_hist(img_ycrcb).ravel()
    luv_hist = calc_hist(img_luv).ravel()
    ycrcb_lab = calc_hist(img_lab).ravel()
    luv_hsv = calc_hist(img_hsv).ravel()
    aaa_d = calc_hist(aaa).ravel()
    bbb_d = calc_hist(bbb).ravel()
    ccc_d = calc_hist(ccc).ravel()

    hist_vector = np.concatenate([bgr_hist, ycrcb_hist, luv_hist, ycrcb_lab, luv_hsv, aaa_d, bbb_d, ccc_d])

    return hist_vector


def get_predict_files(model, image_path, width, height, threshold, model_name):
    name = Path(image_path).name
    x_data, y_true = image_spacer_file(image_path, width, height)
    if model_name == 'ETC':
        y_pred = np.squeeze(model.predict_proba(x_data.reshape(1, len(x_data))))[1]
    else:
        y_pred = np.squeeze(model.predict(np.expand_dims(x_data, 0)))
    if y_pred >= threshold:
        return 1, int(y_true), float(y_pred), name
    else:
        return 0, int(y_true), float(y_pred), name


def get_predict_webcam(model, img, width, height, threshold, model_name):
    x_data = image_spacer_webcam(img, width, height)
    if model_name == 'ETC':
        y_pred = np.squeeze(model.predict_proba(x_data.reshape(1, len(x_data))))[1]
    else:
        y_pred = np.squeeze(model.predict(np.expand_dims(x_data, 0)))
    if y_pred >= threshold:
        return 1
    else:
        return 0


# metrics
def confusion_matrix(y_true, y_pred, threshold):
    """
    calculates the confusion matrix

    parameters:
        y_true (list): A list with the true values as in,
                                0 - negative
                                1 - positive

        y_pred (list): A list with the predictions as in, 0 - negative 1 - positive threshold (int or float): value
        of returns: cm (list): A list with the values for TP, FN, TN, FP (true positives, false negatives,
        true negatives, false positives)
    """

    y_pred = [(1 if y >= threshold else 0) for y in
              y_pred]  # переводим y_pred к двоичному представлению используя threshold
    # binarizing y_pred values use threshold
    cm = [0, 0, 0, 0]  # tp, fn, tn, fp
    for y, y_hat in zip(y_true, y_pred):
        if y == 1:  # Pisitive если истинное значение 1
            if y_hat == 1:
                cm[0] += 1  # tp true positive (реальный образец распознано правильно)
            else:
                cm[1] += 1  # fn false negative (реальный образец ошибочно принят за атаку)
        elif y == 0:  # Actually Negative если истинное значение 0
            if y_hat == 0:
                cm[2] += 1  # tn true negative (атака распознана правильно)
            else:
                cm[3] += 1  # fp false positive (атака распознана как реальный образец)

    return cm


def calculate_metrics(y_true, y_pred, threshold):
    """
    calculates the metrics APCER, BPCER and ACER for any dataset's

    parameters:
        y_true (list):  A list with the true values as in (Список с метками для изображений типа):
                                1 - реальный образец (true sample)
                                0 - поддельный образец (fake sample)

        y_pred (list): Список с предсказаниями вида,
                                0 - атака, fake, spoof
                                1 - live

                                or или score значения вида
                                [0. ; 1.]
                                [-1.; 1.]
                                или любые другие, для них необходимо установить правильный порог.
                                or any values for them need setup right threshold for binarized it

        threshold (int or float): use to binarizing predictions используется для перевода значений y_pred к
                                  двоичному представлению
    returns:
        apcer (float) [0-1] attack presentation classification error rate
        bpcer (float) [0-1] bona fide presentation classification error rate
        acer (float) [0-1] average classification error rate
    """

    # tp, fn, tn, fp
    cm = confusion_matrix(y_true, y_pred, threshold)  # confusion matrix

    try:
        apcer = cm[1] / (cm[1] + cm[0])  # fn / (fn + tp)
    except:
        apcer = 0.0

    try:
        bpcer = cm[3] / (cm[3] + cm[2])  # fp/(fp + tn)
    except:
        bpcer = 0.0

    acer = (apcer + bpcer) / 2  # average between apcer and bpcer  HTER (Half-Total Error Rate – половина полной ошибки)

    return round(apcer, 5), round(bpcer, 5), round(acer, 5)


def compute_eer(fpr, tpr, thresholds, output_path, show_curve=False):
    roc_auc = auc(fpr, tpr)
    """ Returns equal error rate (EER) and the corresponding threshold. """
    fnr = 1 - tpr
    abs_diffs = np.abs(fpr - fnr)
    min_index = np.argmin(abs_diffs)
    eer = np.mean((fpr[min_index], fnr[min_index]))
    if show_curve:
        plt.figure()
        lw = 2
        plt.plot(
            fpr,
            tpr,
            color="darkorange",
            lw=lw,
            label="ROC curve (area = %0.2f)" % roc_auc, )
        plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Рабочая характеристка модели - ROC submission 2")
        plt.legend(loc="lower right")
        plt.savefig(output_path + 'roc_curve_%0.2f_.jpg' % roc_auc)

    return round(eer, 5), round(thresholds[min_index], 5)
