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

<p align="center"><img src="images/system_sx.jpg" title="PAD System scheme" alt="PAD System sheme">
</p>
<table><tr><th>Result of recognition video frames (images)/Результат распознавания изображений (кадров)</th></tr>
 <tr><td>
<img src="images\detect_ex1.png" title="Example 1 real" width="150"/>
<img src="images\detect_ex4.png" title="Example 2 spoof" width="150"/>
<img src="images\detect_ex2.png" title="Example 3 real" width="150"/>
<img src="images\detect_ex3.png" title="Example 4 real" width="150"/>
<img src="images\detect_ex6.png" title="Example 5 real" width="150"/></td></tr>
<td> ![#c5f015]===================== '#c5f015'</td>
    </table>

## Table Styling in Markdown

<style>
.heatMap {
    width: 70%;
    text-align: center;
}
.heatMap th {
background: grey;
word-wrap: break-word;
text-align: center;
}
.heatMap tr:nth-child(1) { background: red; }
.heatMap tr:nth-child(2) { background: orange; }
.heatMap tr:nth-child(3) { background: green; }
</style>

<div class="heatMap">

| Everything | in this table | is Centered |  and the table will only take up 70% of the screen width  | 
| -- | -- | -- | -- |
| This | is | a | Red Row |
| This | is | an | Orange Row |
| This | is | a | Green Row |

</div>

