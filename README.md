# Tsinghua_render
This repo aims to render the traffic simulation.<br>
The background image is the Tsinghua traffic scenario, which can be obtained from <https://cloud.tsinghua.edu.cn/d/92984b43b96840e6ac4e/><br>
Loop For each step:<br>
&emsp; update the states of ego vehicle and surround traffic participants<br>
&emsp; set the postion of ego vehicle as the center of our canvas<br>
&emsp; move corresponding iamges (represent the traffic participants) on the background image<br>
until simulaiton end<br>
