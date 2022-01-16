# [The Simple Presentation Attack Detector of Spoofing](https://github.com/AlexDavydov357/The-Simple-Detector-of-Spoofing)

## Overview / Обзор 
 <p>This repository is dedicated to the image-based Presentation Attack Detection - 
PAD - system two different kindes: (I) print attack (II) replay attack PAD. The proposed PAD system relies on the 
combination of few different color spaces and their mutual remainder when subtracted from each other (Table 1) and 
uses only a single frame to distinguish the bona fide image from an image attack or video replay, see schema on Fig. 1</p>
<table>
<tr><th>Table 1 / Таблица 1</th></tr>
<tr><td align="center">Example1 / Пример1: color space of  spoof image/ цветовое пространство поддельного изображения<br>
<img height="103" width="851" src="images/face_ex1.png" title="Example 1 color space of spoof image" alt="Example 1 color space of spoof image"/><br>
Example2 / Пример2: color space of  truth image/ цветовое пространство истинного изображения<br>
<img height="103" width="851" src="images/face_ex2.png" title="Example 2 color space of truth image" alt="Example 2 color space of truth image"/><br>
Example3 / Пример3: color space of  truth image/ цветовое пространство поддельного изображения<br>
<img height="103" width="851" src="images/face_ex3.png" title="Example 3 color space of truth image" alt="Example 3 color space of truth image"/>
</td></tr>
</table>
<p>Этот репозиторий содержит простой детектор спуфинга при распозновании лиц. Система различает два типа аттак: 1. 
напечатанное изображение 2. воспроизведение видео. Предлагаемая система PAD основана на комбинации нескольких цветовых 
пространств и их взаимной разности (Таблица 1). Для распознавания аттаки система использует всего один кадр, чтобы 
отличить живое изображение от подделки (атаки). Схем представлена на рисунке 1</p>

<p align="center"><img src="https://github.com/AlexDavydov357/The-Simple-Detector-of-Spoofing-/blob/master/images/system_sx.jpg" title="PAD System scheme" alt="PAD System sheme">
</p>
<table><tr><th>Result of recognition video frames (images)/Результат распознавания изображений (кадров)</th></tr>
 <tr><td align="center">
<img src="https://github.com/AlexDavydov357/The-Simple-Detector-of-Spoofing-/blob/master/images/detect_ex1.png"
     title="Example 1 real" width="150">
<img src="images\detect_ex4.png" title="Example 2 spoof" width="150"/>
<img src="images\detect_ex2.png" title="Example 3 real" width="150"/>
<img src="images\detect_ex3.png" title="Example 4 real" width="150"/>
<img src="images\detect_ex6.png" title="Example 5 real" width="150"/></td></tr>
<tr><td align="center"><img src="images\table_head2.png"/></td></tr>
<tr><td align="center">
<img  width="150" height="180" src="images\video_ex1.gif"/>
<img  width="150" height="180" src="images\video_ex2.gif"/>
<img  width="150" height="180" src="images\video_ex3.gif"/>
</td></tr>
<tr><td align="center"><img width="320" height="240" src="https://github.com/AlexDavydov357/The-Simple-Detector-of-Spoofing-/blob/master/images\roc_curve_1.00_.jpg"/></td></tr>
    </table>
<p>For quick inference just clone this repository, setup dependents from requirements.txt, 
and run the attack_detector.py like show below:<br>

```bash
$ git clone https://github.com/AlexDavydov357/The-Simple-Detector-of-Spoofing-.git
$ pip install -r requirements.txt
```
By default, will using your webcam, but no well result<br>

```bash
python attack_detector.py
```
Will used your IP camera, is well result, just put your RTSP, RTMP, HTTP stream address<br>

```bash
python attack_detector.py -s rtsp://192.168.1.233:554/user=admin_password=9UqCoEZs_channel=0_stream=1.sdp?real_stream
```
Will check your images<br>

```bash
python attack_detector.py -s path to images_folder
```
