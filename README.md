# Tsinghua_render
This repo aims to render the traffic simulation.<br>
The background image is the Tsinghua traffic scenario, which can be obtained from <https://cloud.tsinghua.edu.cn/d/92984b43b96840e6ac4e/><br>
Loop For each step:<br>
&emsp; receive the states of ego vehicle and surround traffic participants<br>
&emsp; set the postion of ego vehicle as the center of window<br>
&emsp; move images (represent the traffic participants) on the background to the corresponding positions<br>
until simulaiton end<br>
