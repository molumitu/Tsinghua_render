# Tsinghua_render
This repo aims to render the traffic simulation.
The background image is the Tsinghua traffic scenario, which can be obtained from <https://cloud.tsinghua.edu.cn/d/92984b43b96840e6ac4e/>
Loop For each step:
  first update the states of ego vehicle and surround traffic participants
  then set the postion of ego vehicle as the center of our canvas
  Finally move corresponding iamges (represent the traffic participants) on the background image
 until simulaiton end
